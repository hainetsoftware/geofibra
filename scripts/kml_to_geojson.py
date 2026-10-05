#!/usr/bin/env python3
"""
kml_to_geojson.py - Parser KML e generatore GeoJSON / data.js per la rete FTTH di Collesalvetti.
Supporta Snapshot 3, calcolo distanze Haversine, aree poligonali e metadati ordinanze.
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
    elif "aiaccia" in nl or "aiaccia" in dl:
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
        color = "#00ff9d"
        frazione = "Collesalvetti"
    elif "sanità" in nl or "sanita" in nl:
        category = "rete_sanita"
        icon = "hospital"
        color = "#bf55ec"
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
    elif "cantiere 2" in nl:
        category = "cantiere_programmato"
        icon = "traffic-cone"
        color = "#ffd700"  # Gold per cantiere 2 Stagno
        frazione = "Stagno"
    elif "cantiere 1 non eseguito" in nl:
        category = "cantiere_non_eseguito"
        icon = "traffic-cone"
        color = "#e67e22"
        frazione = "Collesalvetti"
    elif "cantiere 1 eseguito" in nl:
        category = "cantiere_eseguito"
        icon = "traffic-cone"
        color = "#27ae60"
        frazione = "Collesalvetti"
    elif "cantiere 1" in nl:
        category = "cantiere_imminente"
        icon = "traffic-cone"
        color = "#ff8c00"
        frazione = "Collesalvetti"
    elif "cantiere 3" in nl:
        category = "cantiere"
        icon = "traffic-cone"
        color = "#f39c12"
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
    elif "coperta" in nl:
        category = "copertura_ok"
        icon = "polygon-ok"
        color = "#10b981"

    return category, frazione, icon, color

def parse_kml(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {"kml": "http://www.opengis.net/kml/2.2", "gx": "http://www.google.com/kml/ext/2.2"}
    
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

        # Arricchimento Cantieri da Ordinanze Ufficiali Albo Pretorio
        cantiere_info = None
        if "cantiere 2" in name.lower():
            cantiere_info = {
                "codice_ordinanza": "Ordinanza P.M. n. 95 del 10/09/2026 (Reg. Gen. 102)",
                "data_ordinanza": "10/09/2026",
                "inizio_lavori": "2026-09-21T08:00:00+02:00",
                "fine_lavori": "2026-10-16T18:00:00+02:00",
                "inizio_lavori_effettivo": "2026-10-05T08:00:00+02:00",
                "fine_lavori_effettivo": "2026-10-17T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Otto Marzo",
                    "Via Romita",
                    "Via De Gasperi",
                    "Via Machiavelli",
                    "Via XXV Aprile",
                    "Piazza Di Vittorio"
                ],
                "file_pdf": "ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf",
                "stato_base": "programmato",
                "note_slittamento": "Slittato al 05/10 - 17/10 da rilievo sul campo"
            }
            if not clean_desc:
                clean_desc = "Nuovo cantiere FTTH FiberCop Stagno (Ord. 102/2026 del 10/09/2026, slittato al 05/10 - 17/10). Vie: Via Otto Marzo, Via Romita, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio."
        elif "cantiere 1" in name.lower():
            stato_cantiere = "eseguito" if ("eseguito" in name.lower() and "non eseguito" not in name.lower()) else ("non_eseguito" if "non eseguito" in name.lower() else "imminente")
            cantiere_info = {
                "codice_ordinanza": "Ordinanza P.M. n. 88 del 02/09/2026 (Reg. Gen. 95)",
                "data_ordinanza": "02/09/2026",
                "inizio_lavori": "2026-09-14T08:00:00+02:00",
                "fine_lavori": "2026-10-02T18:00:00+02:00",
                "orario_giornaliero": "08:00 - 18:00 feriali",
                "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
                "vie_interessate": [
                    "Via Nenni",
                    "Via Roma (rotatoria Via Nenni)",
                    "Via del Valico a Pisa",
                    "Via di Cerretello"
                ],
                "file_pdf": "ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf",
                "stato_base": stato_cantiere
            }
            if not clean_desc:
                clean_desc = f"Cantiere FTTH FiberCop Collesalvetti (Ord. 95/2026 del 02/09/2026 - stato: {stato_cantiere}). Vie: Via Nenni, Via Roma, Via del Valico a Pisa, Via di Cerretello."

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
                "cantiere": cantiere_info
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "title": "Rete FTTH & Tracker Cantieri - Comune di Collesalvetti",
            "author": "Mappatura Originale Cittadina integrata con Albo Pretorio",
            "total_features": len(features),
            "generated_at": "2026-10-04",
            "source_snapshot": "Snapshot 3",
            "source_kml": "data/snapshots/rilievo_snapshot3.kml",
            "timezone": "Europe/Rome"
        },
        "features": features
    }
    return geojson

def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    kml_path = "data/snapshots/rilievo_snapshot3.kml"
    data = parse_kml(kml_path)
    
    with open("data/network_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    js_content = f"// Generato automaticamente da {kml_path} con dati Ordinanze Albo Pretorio (Snapshot 3)\nwindow.FTTH_NETWORK_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    with open("js/data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Successfully processed {len(data['features'])} features from {kml_path} into data/network_data.json and js/data.js")

    # Conteggi derivati (apparati, km, frazioni): unica fonte data/stats.json
    import compute_stats
    compute_stats.main()

if __name__ == "__main__":
    main()
