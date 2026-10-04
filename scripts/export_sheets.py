#!/usr/bin/env python3
import json
import csv
import zipfile
import xml.sax.saxutils as saxutils

def escape_xml(s):
    return saxutils.escape(str(s))

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

def export_xlsx(headers, rows, filepath):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="Rete FTTH & Cantieri" sheetId="1" r:id="rId1"/>
    </sheets>
</workbook>"""

    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="2">
        <font><name val="Calibri"/><sz val="11"/></font>
        <font><name val="Calibri"/><sz val="11"/><b/><color rgb="FFFFFFFF"/></font>
    </fonts>
    <fills count="3">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF0F4C81"/></patternFill></fill>
    </fills>
    <borders count="1">
        <border><left/><right/><top/><bottom/></border>
    </borders>
    <cellStyleXfs count="1">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
    </cellStyleXfs>
    <cellXfs count="2">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
    </cellXfs>
</styleSheet>"""

    sheet_rows_xml = []
    hdr_cells = []
    for c_idx, h in enumerate(headers, 1):
        cell_ref = f"{col_letter(c_idx)}1"
        hdr_cells.append(f'<c r="{cell_ref}" s="1" t="inlineStr"><is><t>{escape_xml(h)}</t></is></c>')
    sheet_rows_xml.append(f'<row r="1">{"".join(hdr_cells)}</row>')

    for r_idx, row in enumerate(rows, 2):
        row_cells = []
        for c_idx, val in enumerate(row, 1):
            cell_ref = f"{col_letter(c_idx)}{r_idx}"
            val_str = str(val) if val != "" else ""
            if val_str == "":
                continue
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                row_cells.append(f'<c r="{cell_ref}"><v>{val}</v></c>')
            else:
                row_cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{escape_xml(val_str)}</t></is></c>')
        sheet_rows_xml.append(f'<row r="{r_idx}">{"".join(row_cells)}</row>')

    sheet1_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetData>
        {"".join(sheet_rows_xml)}
    </sheetData>
</worksheet>"""

    with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/styles.xml", styles_xml)
        zf.writestr("xl/worksheets/sheet1.xml", sheet1_xml)

    print(f"Exported XLSX: {filepath}")

def main():
    data = load_data()
    headers, rows = build_rows(data)
    
    export_csv(headers, rows, "data/rete_ftth_collesalvetti_excel_it.csv", delimiter=";", encoding="utf-8-sig")
    export_csv(headers, rows, "data/rete_ftth_collesalvetti_standard.csv", delimiter=",", encoding="utf-8")
    export_xlsx(headers, rows, "data/rete_ftth_collesalvetti.xlsx")

if __name__ == "__main__":
    main()
