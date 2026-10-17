// Generato automaticamente da scripts/compute_stats.py (data/stats.json). Non modificare a mano.
window.FTTH_STATS = {
  "equipment": {
    "by_category_municipal": {
      "arl": 24,
      "arlo": 4,
      "centrale_comunale": 1,
      "centrale_frazione": 6
    },
    "by_frazione_municipal": {
      "Collesalvetti": {
        "arl": 7,
        "arlo": 1,
        "centrali": 1,
        "totale": 9
      },
      "Guasticce": {
        "arl": 3,
        "arlo": 0,
        "centrali": 1,
        "totale": 4
      },
      "Nugola": {
        "arl": 0,
        "arlo": 0,
        "centrali": 1,
        "totale": 1
      },
      "Parrana San Giusto": {
        "arl": 0,
        "arlo": 0,
        "centrali": 1,
        "totale": 1
      },
      "Parrana San Martino": {
        "arl": 0,
        "arlo": 0,
        "centrali": 1,
        "totale": 1
      },
      "Stagno": {
        "arl": 6,
        "arlo": 3,
        "centrali": 1,
        "totale": 10
      },
      "Vicarello": {
        "arl": 8,
        "arlo": 0,
        "centrali": 1,
        "totale": 9
      }
    },
    "by_operator": null,
    "by_operator_note": "Il dato operatore non e' presente nel KML/GeoJSON: nessuna ripartizione prodotta.",
    "cabinets_municipal": 28,
    "centrali_municipal": 7,
    "definition": "Point con category in arl, arlo, centrale_comunale, centrale_frazione, centrale_feeder",
    "excluded_points": [
      {
        "category": "infrastruttura",
        "name": "Coppie di corrugati scoperti"
      }
    ],
    "external": [
      {
        "category": "centrale_feeder",
        "name": "Centrale Feeder (Livorno Nord)"
      }
    ],
    "total_all": 36,
    "total_external": 1,
    "total_municipal": 35
  },
  "features": {
    "by_category": {
      "arl": 24,
      "arlo": 4,
      "cantiere_eseguito": 4,
      "cantiere_non_eseguito": 5,
      "cantiere_programmato": 10,
      "centrale_comunale": 1,
      "centrale_feeder": 1,
      "centrale_frazione": 6,
      "copertura_no": 2,
      "copertura_ok": 2,
      "infrastruttura": 1,
      "infratel": 2,
      "rete_sanita": 1,
      "rete_scuole": 1,
      "tratta_backbone": 1,
      "tratta_stagno": 6
    },
    "lines": 30,
    "points": 37,
    "polygons": 4,
    "total": 71
  },
  "length_km": {
    "by_frazione": {
      "Altro": 9.995,
      "Collesalvetti": 3.3,
      "Stagno": 10.545
    },
    "total": 23.84
  },
  "methodology_version": "1.0",
  "snapshot": {
    "date": "2026-10-17",
    "id": "Snapshot 5",
    "source_kml": "data/snapshots/rilievo_snapshot5.kml"
  }
};
