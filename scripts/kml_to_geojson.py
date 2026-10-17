#!/usr/bin/env python3
"""
kml_to_geojson.py - Parser KML e generatore GeoJSON / data.js per la rete FTTH di Collesalvetti.
Supporta Snapshot 5 (17/10/2026), calcolo distanze Haversine, aree poligonali,
metadati ordinanze comunali e tag di stato/tracciamento standardizzati.
"""

import xml.etree.ElementTree as ET
import json
import re
import math
import os

def haversine(coord1, coord2):
    lon1, lat1 = coord1[0], coord1[1]
    lon2, lat2 = coord2[0], coord2[1]
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def polygon_area_m2(coords):
    if len(coords) < 3:
        return 0
    R = 6371000
    area = 0.0
    for i in range(len(coords)):
        j = (i + 1) % len(coords)
        xi = math.radians(coords[i][0])
        yi = math.radians(coords[i][1])
        xj = math.radians(coords[j][0])
        yj = math.radians(coords[j][1])
        area += (xj - xi) * (2 + math.sin(yi) + math.sin(yj))
    area = abs(area * R * R / 2.0)
    return area

def clean_html(text):
    if not text:
        return ""
    text = text.replace("&nbsp;", " ")
    text = re.sub(r'<div>', '\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return "\n".join(lines)

def extract_kml_styles(root, ns):
    styles = {}
    for cs in root.findall(".//gx:CascadingStyle", ns):
        cid = cs.get("{http://www.opengis.net/kml/2.2}id") or cs.get("id") or cs.get("kml:id")
        ls = cs.find(".//kml:LineStyle", ns)
        l_color = ls.find("kml:color", ns).text.strip() if ls is not None and ls.find("kml:color", ns) is not None else None
        styles[cid] = {"line_color": l_color}
    for sm in root.findall(".//kml:StyleMap", ns):
        smid = sm.get("{http://www.opengis.net/kml/2.2}id") or sm.get("id") or sm.get("kml:id")
        pairs = {}
        for p in sm.findall("kml:Pair", ns):
            key = p.find("kml:key", ns).text if p.find("kml:key", ns) is not None else ""
            url = p.find("kml:styleUrl", ns).text if p.find("kml:styleUrl", ns) is not None else ""
            pairs[key] = url
        styles[smid] = {"pairs": pairs}
    return styles

def categorize(name, geom_type, desc):
    n = name.strip()
    nl = n.lower()
    dl = desc.lower() if desc else ""
    
    frazione = "Altro"
    if n.startswith("C ") or "collesalvetti" in nl:
        frazione = "Collesalvetti"
    elif n.startswith("V ") or "vicarello" in nl:
        frazione = "Vicarello"
    elif n.startswith("S ") or "stagno" in nl:
        frazione = "Stagno"
    elif n.startswith("G ") or "guasticce" in nl:
        frazione = "Guasticce"
    elif "aiaccia" in nl or "aiaccia" in dl or "umbria" in nl or "umbria" in dl:
        frazione = "Stagno"

    category = "altro"
    icon = "box"
    color = "#888888"

    if "centrale comunale" in nl:
        category = "centrale_comunale"
        icon = "building-tower"
        color = "#e60000"
        frazione = "Collesalvetti"
    elif "centrale feeder" in nl:
        category = "centrale_feeder"
        icon = "building-tower"
        color = "#b22222"
        frazione = "Altro"
    elif "centrale di frazione" in nl:
        category = "centrale_frazione"
        icon = "building-small"
        color = "#ff6600"
    elif "arlo" in nl:
        category = "arlo"
        icon = "optical-cabinet"
        color = "#00f0ff"
    elif "arl" in nl:
        category = "arl"
        icon = "copper-cabinet"
        color = "#ff3366"
    elif "corrugati" in nl:
        category = "infrastruttura"
        icon = "conduit"
        color = "#ffd700"
    elif "scuole" in nl:
        category = "rete_scuole"
        icon = "school"
        color = "#303f9f"  # Sincronizzato con stile KML #ff9f3f30 -> #303f9f
        frazione = "Collesalvetti"
    elif "sanità" in nl or "sanita" in nl:
        category = "rete_sanita"
        icon = "hospital"
        color = "#303f9f"  # Sincronizzato con stile KML #ff9f3f30 -> #303f9f
        frazione = "Collesalvetti"
    elif "infratel" in nl:
        category = "infratel"
        icon = "infratel"
        color = "#ffaa00"
    elif "backbone" in nl:
        category = "tratta_backbone"
        icon = "fiber-cable"
        color = "#9b59b6"
        frazione = "Stagno"
    elif "cantiere 2 eseguito" in nl:
        category = "cantiere_eseguito"
        icon = "traffic-cone"
        color = "#27ae60"
        frazione = "Stagno"
    elif "cantiere 2" in nl:
        category = "cantiere_programmato"
        icon = "traffic-cone"
        color = "#ffd700"  # Oro per Cantiere 2 Stagno in completamento
        frazione = "Stagno"
    elif "cantiere 1 non eseguito" in nl:
        category = "cantiere_non_eseguito"
        icon = "traffic-cone"
        color = "#e67e22"
        frazione = "Collesalvetti"
    elif "cantiere 1 eseguito" in nl or "cantiere 1 aggiunto" in nl:
        category = "cantiere_eseguito"
        icon = "traffic-cone"
        color = "#27ae60"  # Verde per tratte completate
        frazione = "Collesalvetti"
    elif "cantiere 1" in nl:
        category = "cantiere_imminente"
        icon = "traffic-cone"
        color = "#ff8c00"
        frazione = "Collesalvetti"
    elif "cantiere 4" in nl:
        category = "cantiere_programmato"
        icon = "traffic-cone"
        color = "#f39c12"  # Arancio per Cantiere 4 Stagno pianificato
        frazione = "Stagno"
    elif "cantiere 3" in nl:
        category = "cantiere_programmato"
        icon = "traffic-cone"
        color = "#f39c12"  # Arancio per Cantiere 3 Stagno autorizzato
        frazione = "Stagno"
    elif "cantiere" in nl:
        category = "cantiere"
        icon = "traffic-cone"
        color = "#ff8c00"
        if frazione == "Altro":
            frazione = "Collesalvetti"
    elif "tratta stagno" in nl:
        category = "tratta_stagno"
        icon = "fiber-cable"
        color = "#00c3ff"
        frazione = "Stagno"
    elif "non coperta" in nl:
        category = "copertura_no"
        icon = "polygon-no"
        color = "#ef4444"
        if frazione == "Altro" and ("stagno" in nl or "095490c3ee4270e4b838" in nl):
            frazione = "Stagno"
    elif "coperta" in nl:
        category = "copertura_ok"
        icon = "polygon-ok"
        color = "#10b981"
        if frazione == "Altro" and ("stagno" in nl or "0f2da583d541c062fa84" in nl):
            frazione = "Stagno"

    return category, frazione, icon, color

def parse_kml(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {"kml": "http://www.opengis.net/kml/2.2", "gx": "http://www.google.com/kml/ext/2.2"}
    
    kml_styles = extract_kml_styles(root, ns)
    placemarks = root.findall(".//kml:Placemark", ns)
    features = []
    
    for idx, p in enumerate(placemarks):
        pid = p.get("id", f"pm_{idx}")
        name_el = p.find("kml:name", ns)
        name = name_el.text.strip() if name_el is not None and name_el.text else f"Elemento #{idx+1}"
        
        desc_el = p.find("kml:description", ns)
        raw_desc = desc_el.text if desc_el is not None and desc_el.text else ""
        clean_desc = clean_html(raw_desc)
        
        look_at = None
        look_el = p.find("kml:LookAt", ns)
        if look_el is not None:
            look_at = {}
            for tag in ["longitude", "latitude", "altitude", "heading", "tilt", "range"]:
                tel = look_el.find(f"kml:{tag}", ns)
                if tel is not None and tel.text:
                    look_at[tag] = float(tel.text)

        geom = None
        geom_type = None
        length_m = 0
        area_m2 = 0
        
        point_el = p.find("kml:Point", ns)
        line_el = p.find("kml:LineString", ns)
        poly_el = p.find("kml:Polygon", ns)
        
        if point_el is not None:
            geom_type = "Point"
            coords_text = point_el.find("kml:coordinates", ns).text.strip()
            parts = [float(x) for x in coords_text.split(",") if x.strip()]
            lon, lat = parts[0], parts[1]
            ele = parts[2] if len(parts) > 2 else 0
            geom = {
                "type": "Point",
                "coordinates": [lon, lat, ele]
            }
        elif line_el is not None:
            geom_type = "LineString"
            coords_text = line_el.find("kml:coordinates", ns).text.strip()
            pts = []
            for item in coords_text.split():
                if not item.strip(): continue
                parts = [float(x) for x in item.split(",") if x.strip()]
                pts.append([parts[0], parts[1], parts[2] if len(parts) > 2 else 0])
            geom = {
                "type": "LineString",
                "coordinates": pts
            }
            for i in range(len(pts) - 1):
                length_m += haversine(pts[i], pts[i+1])
        elif poly_el is not None:
            geom_type = "Polygon"
            coords_text = poly_el.find(".//kml:LinearRing/kml:coordinates", ns).text.strip()
            pts = []
            for item in coords_text.split():
                if not item.strip(): continue
                parts = [float(x) for x in item.split(",") if x.strip()]
                pts.append([parts[0], parts[1], parts[2] if len(parts) > 2 else 0])
            geom = {
                "type": "Polygon",
                "coordinates": [pts]
            }
            area_m2 = polygon_area_m2(pts)
            
        category, frazione, icon, color = categorize(name, geom_type, clean_desc)

        # Sincronizzazione dinamica dello stile da KML (es. colore LineStyle)
        style_el = p.find("kml:styleUrl", ns)
        if style_el is not None and style_el.text:
            surl = style_el.text.strip().replace("#", "")
            if surl in kml_styles:
                info = kml_styles[surl]
                target_norm = info.get("pairs", {}).get("normal", "").replace("#", "")
                if target_norm in kml_styles and kml_styles[target_norm].get("line_color"):
                    lc = kml_styles[target_norm]["line_color"]
                    if len(lc) == 8:
                        r, g, b = lc[6:8], lc[4:6], lc[2:4]
                        color = f"#{r}{g}{b}"
        
        # Gestione specifica delle Centrali
        if category == "centrale_comunale":
            name = "Centrale Comunale (Collesalvetti)"
            frazione = "Collesalvetti"
        elif category == "centrale_feeder":
            name = "Centrale Feeder (Livorno Nord)"
            frazione = "Altro"
        elif category == "centrale_frazione" and geom_type == "Point":
            lon, lat = geom["coordinates"][0], geom["coordinates"][1]
            if 43.605 < lat < 43.615 and 10.465 < lon < 10.475:
                frazione = "Vicarello"
                name = "Centrale di Frazione (Vicarello)"
            elif 43.590 < lat < 43.605 and 10.400 < lon < 10.415:
                frazione = "Guasticce"
                name = "Centrale di Frazione (Guasticce)"
            elif 43.580 < lat < 43.595 and 10.340 < lon < 10.360:
                frazione = "Stagno"
                name = "Centrale di Frazione (Stagno)"
            elif 43.570 < lat < 43.585 and 10.430 < lon < 10.445:
                frazione = "Nugola"
                name = "Centrale di Frazione (Nugola)"
            elif 43.532 < lat < 43.545 and 10.435 < lon < 10.450:
                frazione = "Parrana San Martino"
                name = "Centrale di Frazione (Parrana San Martino)"
            elif lat < 43.532:
                frazione = "Parrana San Giusto"
                name = "Centrale di Frazione (Parrana San Giusto)"

        # Nomi standardizzati e arricchiti per ARLO
        if name == "C [] ARLO":
            name = "C [] ARLO (Futuro ARLO 01)"
        elif name == "S [] ARLO":
            name = "S [] ARLO (Senza etichetta - Affiancato ad ARL 04)"

        # Poligoni Copertura Stagno (Snapshot 5)
        if "stagno" in name.lower() and geom_type == "Polygon":
            frazione = "Stagno"
            if category == "copertura_ok":
                clean_desc = "Area Coperta Stagno: estesa verso sud e ovest per includere il comparto di Cantiere 3 e Cantiere 4 (Snapshot 5 - 17/10/2026)."
            elif category == "copertura_no":
                clean_desc = "Area NON Coperta Stagno: ridotta a stretta fascia orientale (10.3547 - 10.3576, Snapshot 5 - 17/10/2026)."

        # Metadata di tracciamento standardizzati (status, ordinanza, operatore, data)
        status_code = "attivo"
        status_label = "Attivo"
        ordinanza_str = None
        operatore_str = "FiberCop"
        data_rilevamento = "2026-10-17"

        if category == "arlo":
            operatore_str = "FiberCop"
            if frazione == "Collesalvetti":
                status_code = "installato"
                status_label = "Installato (Opere civili completate - In attesa di soffiaggio fibra/PTE)"
                ordinanza_str = "Ordinanza P.M. n. 88 del 02/09/2026 (Reg. Gen. 95)"
                if not clean_desc or "Primo ARLO" not in clean_desc:
                    clean_desc = "Primo armadio ottico del capoluogo (C [] ARLO, futuro ARLO 01), situato nell'aiuola/marciapiede della rotatoria tra Via Roma, Via Nenni e Via Piero Ciampi. Plinto gettato, cabinet montato, 4 pozzetti di smistamento FiberCop posati a corona della rotatoria e raccordati a cavidotti TIM preesistenti. Stato: Installato (Opere civili completate - In attesa di soffiaggio fibra/PTE)."
            elif frazione == "Stagno":
                status_code = "infrastrutturato"
                status_label = "Infrastrutturati / In fase di cablaggio e predisposizione secondaria"
                ordinanza_str = "Ordinanza P.M. n. 95/2026 (Reg. Gen. 102/104/2026)"
                if "S []" in name:
                    clean_desc = "Armadio ottico FiberCop posato in affiancamento al rame S [04] ARL ([10.353902, 43.589311]) su Via Romita / angolo Via XXV Aprile (privo di etichetta numerica, futuro ARLO 04 - 3° ARLO censito a Stagno). Rilevato nel walk-in dell'11/10/2026. In zona 6 pozzetti in fase di getto/chiusura finale nell'area del Cantiere 2. Stato: Infrastrutturati / In fase di cablaggio e predisposizione secondaria."
                elif not clean_desc:
                    clean_desc = f"Armadio ottico FiberCop {name} a Stagno. Stato: Infrastrutturati / In fase di cablaggio e predisposizione secondaria."
        elif category == "arl":
            operatore_str = "TIM / FiberCop"
            status_code = "attivo_rame"
            status_label = "Attivo (Rete Rame / FTTC)"
        elif category.startswith("centrale"):
            operatore_str = "TIM / FiberCop"
            status_code = "attivo"
            status_label = "Attivo (Centrale TLC)"
        elif category == "infratel":
            operatore_str = "Infratel / Open Fiber"
            status_code = "completato"
            status_label = "Completato (Infrastruttura BUL Infratel)"
        elif category in ["rete_scuole", "rete_sanita"]:
            operatore_str = "Fastweb / FiberCop"
            status_code = "completato"
            status_label = "Completato (Piano PA Connessa)"
        elif category == "tratta_backbone":
            operatore_str = "FiberCop"
            status_code = "completato"
            status_label = "Completato (Dorsale Fibra SP555)"
            ordinanza_str = "Autorizzazione Provinciale SP555 (Luglio 2026)"
        elif category == "tratta_stagno":
            operatore_str = "FiberCop"
            status_code = "completato"
            status_label = "Completato (Posa Fibra Maggio-Giugno 2026 - Ripristino definitivo manto stradale Ord. 112/2026)"

        # Arricchimento Cantieri da Ordinanze Ufficiali Albo Pretorio
        cantiere_info = None
        if "cantiere 4" in name.lower():
            status_code = "planned"
            status_label = "Pianificato / Avvio programmato (26/10 - 20/11)"
            ordinanza_str = "110/2026"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": "Ordinanza P.M. n. 110/2026 (Autorizzazione Tecnica n. 26/2026)",
                "data_ordinanza": "14/10/2026",
                "inizio_lavori": "2026-10-26T08:00:00+02:00",
                "fine_lavori": "2026-11-20T18:00:00+02:00",
                "inizio_lavori_effettivo": "2026-10-26T08:00:00+02:00",
                "fine_lavori_effettivo": "2026-11-20T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Marx",
                    "Via Curiel (lato sud)",
                    "Via Gobetti",
                    "Via Don Verità",
                    "Via F.lli Cervi",
                    "Via La Malfa",
                    "Via Verga",
                    "Via Berlinguer"
                ],
                "file_pdf": "ordinanze/ordinanza_110_2026_stagno_cantiere4.pdf",
                "stato_base": "planned",
                "note_slittamento": "Nuova espansione comparto ovest Stagno (26/10 - 20/11/2026). Ordinanza PM n. 110/2026, Aut. Tecnica n. 26/2026."
            }
            clean_desc = "Cantiere 4 Stagno (Ordinanza PM n. 110/2026, Autorizzazione Tecnica n. 26/2026). Finestra: 26/10/2026 - 20/11/2026. Vie: Via Marx, Via Curiel (lato sud), Via Gobetti, Via Don Verità, Via F.lli Cervi, Via La Malfa, Via Verga, Via Berlinguer. Stato: Pianificato."
        elif "cantiere 2 eseguito" in name.lower():
            status_code = "completato"
            status_label = "Completato (Posa condotte ultimata)"
            ordinanza_str = "Ordinanza P.M. n. 95/2026 (Reg. Gen. 102/104/2026) + Proroga Ord. n. 111 del 16/10/2026"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": ordinanza_str,
                "data_ordinanza": "10/09/2026",
                "inizio_lavori": "2026-09-21T08:00:00+02:00",
                "fine_lavori": "2026-10-23T18:00:00+02:00",
                "inizio_lavori_effettivo": "2026-10-05T08:00:00+02:00",
                "fine_lavori_effettivo": "2026-10-23T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Romita sud",
                    "Via XXV Aprile"
                ],
                "file_pdf": "ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf",
                "stato_base": "eseguito",
                "note_slittamento": "Tratta verificata come completata nell'ultimo walk-in su Via Romita sud e Via XXV Aprile (292,9 m). Posa condotte ultimata."
            }
            clean_desc = "Tratta completata Cantiere 2 Stagno (Via Romita sud / Via XXV Aprile, 292,9 m). Posa condotte ultimata al walk-in 11/10/2026. Ord. 104/2026 prorogata con Ord. 111/2026."
        elif "cantiere 2" in name.lower():
            status_code = "in_completamento"
            status_label = "In completamento (Proroga al 23/10 Ord. 111/2026 - Posa condotte ultimata, 6 pozzetti in chiusura)"
            ordinanza_str = "Ordinanza P.M. n. 95/2026 (Reg. Gen. 102/104/2026) + Proroga Ord. n. 111 del 16/10/2026"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": ordinanza_str,
                "data_ordinanza": "16/10/2026",
                "inizio_lavori": "2026-09-21T08:00:00+02:00",
                "fine_lavori": "2026-10-23T18:00:00+02:00",
                "inizio_lavori_effettivo": "2026-10-05T08:00:00+02:00",
                "fine_lavori_effettivo": "2026-10-23T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Romita sud",
                    "Via De Gasperi",
                    "Via Machiavelli",
                    "Via XXV Aprile",
                    "Piazza Di Vittorio",
                    "Via Don Verità",
                    "Via 8 Marzo"
                ],
                "file_pdf": "ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf",
                "stato_base": "in_completamento",
                "note_slittamento": "Finestra originaria: 05/10/2026 - 17/10/2026. Prorogata con Ordinanza n. 111 del 16/10/2026 al 23/10/2026 (estensione di 5 giorni lavorativi per completamento minitrincee secondarie e pozzetti in calcestruzzo attorno al nuovo ARLO)."
            }
            clean_desc = "Cantiere 2 Stagno (Ord. 104/2026 + Proroga Ord. 111 del 16/10/2026). Nuova scadenza: 23/10/2026. Vie: Via Romita sud, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio, Via Don Verità, Via 8 Marzo. Stato: In completamento (Posa condotte completata, 6 pozzetti in fase di getto/chiusura finale attorno ad ARLO)."
        elif "cantiere 3" in name.lower():
            status_code = "autorizzato"
            status_label = "Autorizzato / Avvio programmato (19/10 - 23/10)"
            ordinanza_str = "Ordinanza P.M. n. 105/2026 + Concessione Suolo n. 77/2026"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": ordinanza_str,
                "data_ordinanza": "09/10/2026",
                "inizio_lavori": "2026-10-19T08:00:00+02:00",
                "fine_lavori": "2026-10-23T18:00:00+02:00",
                "inizio_lavori_effettivo": "2026-10-19T08:00:00+02:00",
                "fine_lavori_effettivo": "2026-10-23T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali (5 giorni, occupazione 60 mq)",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Aiaccia",
                    "Via Umbria"
                ],
                "file_pdf": "ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf",
                "stato_base": "programmato",
                "note_slittamento": "Finestra temporale: 19/10/2026 - 23/10/2026 (5 giorni feriali, occupazione 60 mq). Stato: Autorizzato / Avvio programmato. Nota: Innesto sud di Via Aiaccia verso la direttrice provinciale come punto di raccordo con la tratta dorsale SP555 autorizzata a luglio 2026."
            }
            clean_desc = "Cantiere 3 Stagno (Ord. 105/2026 + Concessione Suolo 77/2026). Finestra: 19/10/2026 - 23/10/2026 (5 giorni feriali, occupazione 60 mq). Vie: Via Aiaccia e Via Umbria. Stato: Autorizzato / Avvio programmato. Punto di raccordo: innesto sud Via Aiaccia con dorsale SP555."
        elif "cantiere 1 aggiunto" in name.lower():
            status_code = "completato"
            status_label = "Completato (Anello raccordo rotatoria + 4 pozzetti)"
            ordinanza_str = "Ordinanza P.M. n. 88 del 02/09/2026 (Reg. Gen. 95)"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": ordinanza_str,
                "data_ordinanza": "02/09/2026",
                "inizio_lavori": "2026-09-14T08:00:00+02:00",
                "fine_lavori": "2026-10-02T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Roma (rotatoria Via Nenni / Via Ciampi)"
                ],
                "file_pdf": "ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf",
                "stato_base": "eseguito",
                "note_slittamento": "Anello di raccordo rotatoria (71,8 m) eseguito con minitrincea sigillata (microtubi Fender 4x10/14), 4 pozzetti FiberCop e riuso cavidotti TIM preesistenti. Posato ARLO 01."
            }
            clean_desc = "Anello di raccordo rotatoria Via Roma / Via Nenni / Via Ciampi (71,8 m). Opere civili completate: minitrincea sigillata (microtubi Fender 4x10/14), 4 pozzetti FiberCop e riuso cavidotti TIM. Posato ARLO 01. Ord. 88/2026."
        elif "cantiere 1 eseguito" in name.lower():
            status_code = "completato"
            status_label = "Completato (Minitrincea sigillata + riuso TIM)"
            ordinanza_str = "Ordinanza P.M. n. 88 del 02/09/2026 (Reg. Gen. 95)"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": ordinanza_str,
                "data_ordinanza": "02/09/2026",
                "inizio_lavori": "2026-09-14T08:00:00+02:00",
                "fine_lavori": "2026-10-02T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via del Valico a Pisa",
                    "Via Peppino Impastato",
                    "Via di Cerretello"
                ],
                "file_pdf": "ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf",
                "stato_base": "eseguito",
                "note_slittamento": "Tratta Eseguita (Sud-Est): Via del Valico a Pisa, Via Peppino Impastato, Via di Cerretello. Tipologia di posa: minitrincea sigillata (microtubi Fender 4x10/14) + riuso cavidotti storici TIM."
            }
            clean_desc = "Tratta Eseguita Sud-Est (Via del Valico a Pisa, Via Peppino Impastato, Via di Cerretello). Minitrincea sigillata (microtubi Fender 4x10/14) e riuso cavidotti TIM. Ord. 88/2026."
        elif "cantiere 1 non eseguito" in name.lower():
            status_code = "in_attesa_proroga"
            status_label = "In attesa proroga viaria (Termini Ord. 88 scaduti il 02/10)"
            ordinanza_str = "Ordinanza P.M. n. 88 del 02/09/2026 (Reg. Gen. 95)"
            operatore_str = "FiberCop"
            cantiere_info = {
                "codice_ordinanza": ordinanza_str,
                "data_ordinanza": "02/09/2026",
                "inizio_lavori": "2026-09-14T08:00:00+02:00",
                "fine_lavori": "2026-10-02T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Nenni"
                ],
                "file_pdf": "ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf",
                "stato_base": "non_eseguito",
                "note_slittamento": "Termini Ordinanza 88/2026 scaduti il 02/10; in attesa di nuova ordinanza viaria / proroga per il comparto Via Nenni (marcature blu a terra)."
            }
            clean_desc = "Tratta Non Eseguita Nord-Ovest (Via Nenni). Marcature blu a terra. Termini Ordinanza 88/2026 scaduti il 02/10; in attesa di nuova ordinanza viaria / proroga per il comparto Via Nenni."

        start_date = None
        end_date = None
        streets = None
        if "cantiere 4" in name.lower():
            start_date = "2026-10-26"
            end_date = "2026-11-20"
            streets = [
                "Via Marx",
                "Via Curiel (lato sud)",
                "Via Gobetti",
                "Via Don Verità",
                "Via F.lli Cervi",
                "Via La Malfa",
                "Via Verga",
                "Via Berlinguer"
            ]
        elif cantiere_info:
            start_date = cantiere_info["inizio_lavori"][:10]
            end_date = cantiere_info["fine_lavori"][:10]
            streets = cantiere_info["vie_interessate"]

        feature = {
            "type": "Feature",
            "id": pid,
            "geometry": geom,
            "properties": {
                "id": pid,
                "name": name,
                "category": category,
                "frazione": frazione,
                "geom_type": geom_type,
                "description": clean_desc,
                "raw_description": raw_desc,
                "icon": icon,
                "color": color,
                "length_m": round(length_m, 1),
                "length_km": round(length_m / 1000.0, 3),
                "area_m2": round(area_m2, 1),
                "area_km2": round(area_m2 / 1000000.0, 4),
                "lookAt": look_at,
                "cantiere": cantiere_info,
                "status": status_code,
                "status_label": status_label,
                "ordinanza": ordinanza_str,
                "operatore": operatore_str,
                "data_rilevamento": data_rilevamento,
                "start_date": start_date,
                "end_date": end_date,
                "streets": streets
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "title": "Geo Fibra - Rete FTTH & Tracker Cantieri - Comune di Collesalvetti",
            "author": "Mappatura Originale Cittadina integrata con Albo Pretorio",
            "total_features": len(features),
            "generated_at": "2026-10-17",
            "source_snapshot": "Snapshot 5",
            "source_kml": "data/snapshots/rilievo_snapshot5.kml",
            "timezone": "Europe/Rome"
        },
        "features": features
    }
    return geojson

def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    kml_path = "data/snapshots/rilievo_snapshot5.kml"
    if not os.path.exists(kml_path):
        kml_path = "FTTH Collesalvetti_snapshot5.kml"
    data = parse_kml(kml_path)
    
    with open("data/network_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    js_content = f"// Generato automaticamente da {kml_path} con dati Ordinanze Albo Pretorio (Snapshot 5 - 17/10/2026)\nwindow.FTTH_NETWORK_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    with open("js/data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Successfully processed {len(data['features'])} features from {kml_path} into data/network_data.json and js/data.js")

    # Conteggi derivati (apparati, km, frazioni): unica fonte data/stats.json
    import compute_stats
    compute_stats.main()

if __name__ == "__main__":
    main()
