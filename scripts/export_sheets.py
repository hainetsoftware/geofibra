#!/usr/bin/env python3
import json
import csv
import zipfile
import os
import re
import xml.sax.saxutils as saxutils

def escape_xml(s):
    return saxutils.escape(str(s))

def sanitize_cell(val):
    """Sanitizza i valori delle celle per la scrittura in XML/OOXML.
    - None -> stringa vuota
    - Numeri -> lasciati int o float
    - Stringhe -> rimozione caratteri di controllo, protezione da formule iniettate (=, +, -, @)
    - Taglio a max 32.767 caratteri (limite Excel)
    """
    if val is None or val == "":
        return ""
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return val
    s = str(val)
    # Rimuove caratteri di controllo non permessi in XML (tranne \t, \n, \r)
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
    # Protezione spreadsheet injection: prefissa con apostrofo se inizia con formule
    if s and s[0] in ('=', '+', '-', '@'):
        s = "'" + s
    if len(s) > 32767:
        s = s[:32767]
    return s

def get_type_label(category):
    mapping = {
        'arl': 'ARL (Rame)',
        'arlo': 'ARLO (Ottico FiberCop)',
        'centrale_comunale': 'Centrale Telecom (Sede OLT)',
        'centrale_frazione': 'Centrale di Frazione',
        'centrale_feeder': 'Centrale Feeder (Interconnessione Esterna)',
        'cantiere': 'Cantiere Fibra Ottica',
        'cantiere_imminente': 'Cantiere FTTH (Attivazione Imminente)',
        'cantiere_eseguito': 'Cantiere FTTH (Tratta Eseguita)',
        'cantiere_non_eseguito': 'Cantiere FTTH (Tratta Non Eseguita)',
        'cantiere_programmato': 'Cantiere FTTH (Nuova Ordinanza Programmata)',
        'tratta_stagno': 'Tratta Fibra Posa',
        'tratta_backbone': 'Dorsale / Backbone Fibra',
        'rete_scuole': 'Tratta Scuole Connesse',
        'rete_sanita': 'Tratta Sanità Connesse',
        'infratel': 'Infrastruttura Infratel BUL',
        'infrastruttura': 'Infrastruttura / Corrugati',
        'copertura_ok': 'Area Coperta FTTH',
        'copertura_no': 'Area NON Coperta'
    }
    return mapping.get(category, category.replace('_', ' ').capitalize())

def load_data():
    with open("data/network_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_stats():
    if os.path.exists("data/stats.json"):
        with open("data/stats.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def build_rows(data):
    headers = [
        "ID",
        "Nome Apparato",
        "Tipologia",
        "Frazione",
        "Tipo Geometria",
        "Stato / Attivazione Cantiere",
        "Periodo Lavori (Inizio - Fine)",
        "Vie Coinvolte",
        "Riferimento Ordinanza Comunale",
        "Latitudine",
        "Longitudine",
        "Quota (m s.l.m.)",
        "Lunghezza (m)",
        "Lunghezza (km)",
        "Superficie (m²)",
        "Superficie (km²)",
        "Note Tecniche e Dettagli sul Campo",
        "Link Google Maps",
        "Link Ordinanza PDF"
    ]
    
    rows = []
    for f in data["features"]:
        p = f["properties"]
        geom = f["geometry"]
        g_type = geom["type"]
        
        lat = ""
        lon = ""
        ele = ""
        maps_link = ""
        
        if g_type == "Point":
            coords = geom["coordinates"]
            lon = round(coords[0], 6)
            lat = round(coords[1], 6)
            ele = round(coords[2], 1) if len(coords) > 2 else ""
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        elif g_type == "LineString":
            first_pt = geom["coordinates"][0]
            lon = round(first_pt[0], 6)
            lat = round(first_pt[1], 6)
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        elif g_type == "Polygon":
            first_pt = geom["coordinates"][0][0]
            lon = round(first_pt[0], 6)
            lat = round(first_pt[1], 6)
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            
        c = p.get("cantiere")
        c_status = ""
        c_period = ""
        c_streets = ""
        c_ordinanza = ""
        c_pdf = ""
        
        if c:
            c_status = c.get("stato_base", "").upper()
            c_period = f"{c.get('inizio_lavori', '')[:10]} -> {c.get('fine_lavori', '')[:10]}"
            c_streets = ", ".join(c.get("vie_interessate", []))
            c_ordinanza = c.get("codice_ordinanza", "")
            c_pdf = c.get("file_pdf", "")
        elif "cantiere" in p["category"]:
            c_status = "DA COLLEGARE A ORDINANZA"
            
        row = [
            p["id"],
            p["name"],
            get_type_label(p["category"]),
            p["frazione"],
            g_type,
            c_status,
            c_period,
            c_streets,
            c_ordinanza,
            lat,
            lon,
            ele,
            p["length_m"] if p["length_m"] > 0 else "",
            p["length_km"] if p["length_km"] > 0 else "",
            p["area_m2"] if p["area_m2"] > 0 else "",
            p["area_km2"] if p["area_km2"] > 0 else "",
            p["description"].replace("\n", " | "),
            maps_link,
            c_pdf
        ]
        rows.append(row)
    return headers, rows

def export_csv(headers, rows, filepath, delimiter=";", encoding="utf-8-sig"):
    with open(filepath, "w", newline="", encoding=encoding) as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Exported CSV: {filepath}")

def col_letter(col_idx):
    res = ""
    while col_idx > 0:
        col_idx, rem = divmod(col_idx - 1, 26)
        res = chr(65 + rem) + res
    return res

def build_sheet1_xml(headers, rows):
    cols_xml = """    <cols>
        <col min="1" max="1" width="24" customWidth="1"/>
        <col min="2" max="2" width="35" customWidth="1"/>
        <col min="3" max="3" width="35" customWidth="1"/>
        <col min="4" max="4" width="20" customWidth="1"/>
        <col min="5" max="5" width="16" customWidth="1"/>
        <col min="6" max="6" width="30" customWidth="1"/>
        <col min="7" max="7" width="28" customWidth="1"/>
        <col min="8" max="8" width="40" customWidth="1"/>
        <col min="9" max="9" width="45" customWidth="1"/>
        <col min="10" max="11" width="14" customWidth="1"/>
        <col min="12" max="12" width="16" customWidth="1"/>
        <col min="13" max="14" width="16" customWidth="1"/>
        <col min="15" max="16" width="16" customWidth="1"/>
        <col min="17" max="17" width="50" customWidth="1"/>
        <col min="18" max="19" width="45" customWidth="1"/>
    </cols>"""

    sheet_rows_xml = []
    hdr_cells = []
    for c_idx, h in enumerate(headers, 1):
        cell_ref = f"{col_letter(c_idx)}1"
        hdr_cells.append(f'<c r="{cell_ref}" s="1" t="inlineStr"><is><t>{escape_xml(h)}</t></is></c>')
    sheet_rows_xml.append(f'<row r="1">{"".join(hdr_cells)}</row>')

    for r_idx, row in enumerate(rows, 2):
        row_cells = []
        for c_idx, raw_val in enumerate(row, 1):
            cell_ref = f"{col_letter(c_idx)}{r_idx}"
            val = sanitize_cell(raw_val)
            if val == "":
                continue
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                if c_idx == 12:
                    style_id = 3  # Quota (0.0)
                elif c_idx in (14, 16):
                    style_id = 4  # Lunghezza km / Area km2 (0.000)
                else:
                    style_id = 2  # Generale numerico con bordo
                row_cells.append(f'<c r="{cell_ref}" s="{style_id}"><v>{val}</v></c>')
            else:
                row_cells.append(f'<c r="{cell_ref}" s="2" t="inlineStr"><is><t>{escape_xml(str(val))}</t></is></c>')
        sheet_rows_xml.append(f'<row r="{r_idx}">{"".join(row_cells)}</row>')

    last_col = col_letter(len(headers))
    last_row = len(rows) + 1
    autofilter_range = f"A1:{last_col}{last_row}"

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetViews>
        <sheetView workbookViewId="0">
            <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
        </sheetView>
    </sheetViews>
{cols_xml}
    <sheetData>
        {"".join(sheet_rows_xml)}
    </sheetData>
    <autoFilter ref="{autofilter_range}"/>
</worksheet>"""

def build_info_sheet_xml(net_data, stats_data):
    features = net_data.get("features", [])
    total_features = len(features)
    points = sum(1 for f in features if f["geometry"]["type"] == "Point")
    lines = sum(1 for f in features if f["geometry"]["type"] == "LineString")
    polys = sum(1 for f in features if f["geometry"]["type"] == "Polygon")
    
    total_km = round(sum(f["properties"].get("length_km", 0) for f in features), 3)
    
    snap_id = stats_data.get("snapshot", {}).get("id", "Snapshot 3") if stats_data else "Snapshot 3"
    snap_date = stats_data.get("snapshot", {}).get("date", "2026-10-04") if stats_data else "2026-10-04"
    eq_municipal = stats_data.get("equipment", {}).get("total_municipal", "N/D") if stats_data else "32"
    eq_external = stats_data.get("equipment", {}).get("total_external", "N/D") if stats_data else "1"
    cab_municipal = stats_data.get("equipment", {}).get("cabinets_municipal", "N/D") if stats_data else "25"
    cen_municipal = stats_data.get("equipment", {}).get("centrali_municipal", "N/D") if stats_data else "7"
    
    info_rows = [
        ("METADATI ESPORTAZIONE GEOFIBRA", ""),
        ("Progetto", "GeoFibra Collesalvetti - Osservatorio Civico FTTH"),
        ("Comune", "Collesalvetti (LI), Toscana, Italia"),
        ("Rilievo sorgente", f"{snap_id} ({snap_date})"),
        ("Sorgente dati KML", "data/snapshots/rilievo_snapshot3.kml"),
        ("Data generazione dataset", "2026-10-04"),
        ("", ""),
        ("CONTEGGI GEOSPAZIALI", ""),
        ("Totale feature rilevate", total_features),
        ("Elementi puntiformi (Point)", points),
        ("Tratte lineari (LineString)", lines),
        ("Aree poligonali (Polygon)", polys),
        ("Estensione totale rete (km)", total_km),
        ("", ""),
        ("CONTEGGI APPARATI (Metodologia V1.0)", ""),
        ("Armadi comunali (ARL + ARLO)", cab_municipal),
        ("Centrali comunali (Telecom Sede OLT + Frazione)", cen_municipal),
        ("Totale apparati nel territorio comunale", eq_municipal),
        ("Apparati di raccordo esterno (Feeder)", eq_external),
        ("", ""),
        ("NOTE LEGALI E METODOLOGICHE", ""),
        ("Avvertenza", "I dati derivano da rilievi civici sul campo e ordinanze comunali di viabilita'."),
        ("Natura del dato", "Non costituiscono dato ufficiale di copertura degli operatori TLC (FiberCop / Open Fiber / Infratel)."),
        ("Licenza e consultazione", "Progetto open data / civico: consultabile liberamente.")
    ]
    
    rows_xml = []
    for r_idx, (k, v) in enumerate(info_rows, 1):
        if not k and not v:
            continue
        v_clean = sanitize_cell(v)
        c_k = f'<c r="A{r_idx}" s="6" t="inlineStr"><is><t>{escape_xml(k)}</t></is></c>'
        if isinstance(v_clean, (int, float)):
            c_v = f'<c r="B{r_idx}" s="2"><v>{v_clean}</v></c>'
        else:
            v_str = str(v_clean)
            c_v = f'<c r="B{r_idx}" s="2" t="inlineStr"><is><t>{escape_xml(v_str)}</t></is></c>' if v_str else ""
        rows_xml.append(f'<row r="{r_idx}">{c_k}{c_v}</row>')
        
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <cols>
        <col min="1" max="1" width="45" customWidth="1"/>
        <col min="2" max="2" width="75" customWidth="1"/>
    </cols>
    <sheetData>
        {"".join(rows_xml)}
    </sheetData>
</worksheet>"""

def export_xlsx(headers, rows, filepath, net_data=None, stats_data=None):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="Rete FTTH &amp; Cantieri" sheetId="1" r:id="rId1"/>
        <sheet name="INFO &amp; Metodologia" sheetId="2" r:id="rId2"/>
    </sheets>
</workbook>"""

    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <numFmts count="3">
        <numFmt numFmtId="164" formatCode="0.000"/>
        <numFmt numFmtId="165" formatCode="0.0"/>
        <numFmt numFmtId="166" formatCode="yyyy-mm-dd"/>
    </numFmts>
    <fonts count="3">
        <font><name val="Calibri"/><sz val="11"/></font>
        <font><name val="Calibri"/><sz val="11"/><b/><color rgb="FFFFFFFF"/></font>
        <font><name val="Calibri"/><sz val="11"/><b/><color rgb="FF0F4C81"/></font>
    </fonts>
    <fills count="4">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF0F4C81"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFF0F4F8"/></patternFill></fill>
    </fills>
    <borders count="2">
        <border><left/><right/><top/><bottom/></border>
        <border>
            <left style="thin"><color rgb="FFD0D7DE"/></left>
            <right style="thin"><color rgb="FFD0D7DE"/></right>
            <top style="thin"><color rgb="FFD0D7DE"/></top>
            <bottom style="thin"><color rgb="FFD0D7DE"/></bottom>
        </border>
    </borders>
    <cellStyleXfs count="1">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
    </cellStyleXfs>
    <cellXfs count="7">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/>
        <xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
        <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="2" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1"/>
    </cellXfs>
</styleSheet>"""

    sheet1_xml = build_sheet1_xml(headers, rows)
    sheet2_xml = build_info_sheet_xml(net_data or {}, stats_data or {})

    with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/styles.xml", styles_xml)
        zf.writestr("xl/worksheets/sheet1.xml", sheet1_xml)
        zf.writestr("xl/worksheets/sheet2.xml", sheet2_xml)

    print(f"Exported XLSX: {filepath}")

def main():
    data = load_data()
    stats = load_stats()
    headers, rows = build_rows(data)
    
    export_csv(headers, rows, "data/rete_ftth_collesalvetti_excel_it.csv", delimiter=";", encoding="utf-8-sig")
    export_csv(headers, rows, "data/rete_ftth_collesalvetti_standard.csv", delimiter=",", encoding="utf-8")
    export_xlsx(headers, rows, "data/rete_ftth_collesalvetti.xlsx", net_data=data, stats_data=stats)

if __name__ == "__main__":
    main()
