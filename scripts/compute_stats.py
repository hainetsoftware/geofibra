#!/usr/bin/env python3
"""
compute_stats.py - Unica fonte dei conteggi (apparati, feature, km) della rete.

Legge data/network_data.json e scrive:
  - data/stats.json   (deterministico, chiavi ordinate)
  - js/stats.js       (stessi dati come window.FTTH_STATS, per l'uso da file:// e GitHub Pages
                       senza fetch, con lo stesso schema di js/data.js)

Metodologia (versione METHODOLOGY_VERSION): vedi docs/APPARATI_RECOUNT.md.
  - Apparato = feature di tipo Point con category in EQUIPMENT_CATEGORIES.
  - Linee (tratte/cantieri), poligoni (aree rilevate) e punti "infrastruttura"
    NON sono apparati.
  - Gli apparati in OUTSIDE_CATEGORIES (Centrale Feeder, Livorno) sono riportati
    a parte e mai sommati ai totali comunali.

Uso (dalla radice del repository):  python3 scripts/compute_stats.py
"""

import json
import os
from collections import Counter

METHODOLOGY_VERSION = "1.0"

EQUIPMENT_CATEGORIES = (
    "arl",
    "arlo",
    "centrale_comunale",
    "centrale_frazione",
    "centrale_feeder",
)
CABINET_CATEGORIES = ("arl", "arlo")
CENTRALE_CATEGORIES = ("centrale_comunale", "centrale_frazione", "centrale_feeder")
# Apparati situati fuori dal territorio comunale (Centrale Feeder, Livorno Nord).
OUTSIDE_CATEGORIES = ("centrale_feeder",)

DATA_PATH = "data/network_data.json"
STATS_JSON = "data/stats.json"
STATS_JS = "js/stats.js"


def is_equipment(feature):
    return (
        feature["geometry"]["type"] == "Point"
        and feature["properties"]["category"] in EQUIPMENT_CATEGORIES
    )


def is_outside(feature):
    return feature["properties"]["category"] in OUTSIDE_CATEGORIES


def sorted_dict(counter):
    return {k: counter[k] for k in sorted(counter)}


def compute(data):
    feats = data["features"]
    geom = Counter(f["geometry"]["type"] for f in feats)

    equipment = [f for f in feats if is_equipment(f)]
    municipal = [f for f in equipment if not is_outside(f)]
    external = [f for f in equipment if is_outside(f)]
    other_points = [
        f for f in feats
        if f["geometry"]["type"] == "Point" and not is_equipment(f)
    ]

    by_category_municipal = Counter(f["properties"]["category"] for f in municipal)
    by_frazione = Counter(f["properties"]["frazione"] for f in municipal)

    frazione_detail = {}
    for fr in by_frazione:
        sub = [f for f in municipal if f["properties"]["frazione"] == fr]
        frazione_detail[fr] = {
            "arl": sum(1 for f in sub if f["properties"]["category"] == "arl"),
            "arlo": sum(1 for f in sub if f["properties"]["category"] == "arlo"),
            "centrali": sum(1 for f in sub if f["properties"]["category"] in CENTRALE_CATEGORIES),
            "totale": len(sub),
        }

    # Somma dei length_km per feature (3 decimali), come mostrato dal sito e dai documenti.
    length_km = {}
    for f in feats:
        p = f["properties"]
        length_km[p["frazione"]] = length_km.get(p["frazione"], 0.0) + (p.get("length_km") or 0.0)
    total_length_km = sum(length_km.values())

    meta = data.get("metadata", {})
    stats = {
        "methodology_version": METHODOLOGY_VERSION,
        "snapshot": {
            "id": meta.get("source_snapshot"),
            "date": meta.get("generated_at"),
            "source_kml": meta.get("source_kml"),
        },
        "features": {
            "total": len(feats),
            "points": geom.get("Point", 0),
            "lines": geom.get("LineString", 0),
            "polygons": geom.get("Polygon", 0),
            "by_category": sorted_dict(Counter(f["properties"]["category"] for f in feats)),
        },
        "length_km": {
            "total": round(total_length_km, 3),
            "by_frazione": {k: round(v, 3) for k, v in sorted(length_km.items()) if v},
        },
        "equipment": {
            "definition": "Point con category in " + ", ".join(EQUIPMENT_CATEGORIES),
            "total_municipal": len(municipal),
            "total_external": len(external),
            "total_all": len(equipment),
            "cabinets_municipal": sum(by_category_municipal[c] for c in CABINET_CATEGORIES),
            "centrali_municipal": sum(
                by_category_municipal[c] for c in CENTRALE_CATEGORIES
            ),
            "by_category_municipal": sorted_dict(by_category_municipal),
            "by_frazione_municipal": {k: frazione_detail[k] for k in sorted(frazione_detail)},
            "external": sorted(
                [{"name": f["properties"]["name"], "category": f["properties"]["category"]}
                 for f in external],
                key=lambda x: x["name"],
            ),
            "excluded_points": sorted(
                [{"name": f["properties"]["name"], "category": f["properties"]["category"]}
                 for f in other_points],
                key=lambda x: x["name"],
            ),
            "by_operator": None,
            "by_operator_note": "Il dato operatore non e' presente nel KML/GeoJSON: nessuna ripartizione prodotta.",
        },
    }
    return stats


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    stats = compute(data)
    text = json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    with open(STATS_JSON, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    with open(STATS_JS, "w", encoding="utf-8") as f:
        f.write(
            f"// Generato automaticamente da scripts/compute_stats.py (data/stats.json). Non modificare a mano.\n"
            f"window.FTTH_STATS = {text};\n"
        )
    eq = stats["equipment"]
    print(
        f"Stats: {stats['features']['total']} feature, "
        f"{eq['total_municipal']} apparati comunali (+{eq['total_external']} esterni) "
        f"-> {STATS_JSON}, {STATS_JS}"
    )


if __name__ == "__main__":
    main()
