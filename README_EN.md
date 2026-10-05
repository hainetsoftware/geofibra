# 🌐 GeoFibra Collesalvetti
### *Civic FTTH Network Observatory & Municipal Works Tracker in Collesalvetti (Tuscany, Italy)*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GIS: Leaflet 1.9.4](https://img.shields.io/badge/GIS-Leaflet%201.9.4-brightgreen.svg)](https://leafletjs.com/)
[![Data: Snapshot 3](https://img.shields.io/badge/Data-Snapshot%203%20(04%2F10%2F2026)-orange.svg)](#-official-data--metrics-snapshot-3)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Active-success.svg)](#-deployment-on-github-pages)

---

**GeoFibra Collesalvetti** is an open-source civic platform and technical observatory mapping the optical fiber telecommunications rollout (**FTTH FiberCop / Wholesale**), tracking municipal street excavation decrees in real-time, and hosting a comprehensive technical and popular encyclopedia on ultrabroadband networking in Italy.

The initiative provides transparency for local citizens regarding street excavations, traffic restrictions, asphalt restoration timelines, and true connectivity availability across the municipality of Collesalvetti and its outlying fractions.

> [!IMPORTANT]
> **Device Support Notice:**
> - **GIS Map & Works Tracker:** Built specifically for **Desktop computers and Tablets** ($\ge$ 768 px). On mobile smartphones (< 768 px), an explanatory blocking screen informs the user of the resolution requirements needed to read dense geospatial vectors, preventing Leaflet scripts and datasets from loading.
> - **Technical Wiki:** Fully responsive and optimized for **all devices, including smartphones**, featuring dedicated horizontally scrollable tables.

---

## 📑 Table of Contents

1. [Key Features](#-key-features)
2. [Official Data & Metrics (Snapshot 3)](#-official-data--metrics-snapshot-3)
3. [Municipal Decrees & Works Tracker](#-municipal-decrees--works-tracker)
4. [The Technical & Educational Wiki](#-the-technical--educational-wiki)
5. [Repository Architecture](#-repository-architecture)
6. [Data Pipeline & Reproducibility](#-data-pipeline--reproducibility)
7. [Local Quick Start](#-local-quick-start)
8. [GitHub Pages Deployment & Repository Renaming](#-github-pages-deployment--repository-renaming)
9. [Disclaimer & License](#-disclaimer--license)

---

## 🌟 Key Features

### 1. 🗺️ High-Precision GIS Cartography (Desktop / Tablet)
- **Multi-layer raster engine:** Instant switching between *OpenStreetMap*, *Esri World Imagery (HD Satellite)*, and *Esri Dark Canvas*.
- **Strict geographic bounding:** View restricted to the Tuscany regional perimeter (`TOSCANA_BOUNDS`) to prevent unintended navigation drift.
- **Audited geospatial assets:** Trench traces, primary feeder lines, optical cabinets (ARLO), copper cross-connects (ARL), telecom central offices, and underground junction boxes with metric dimensions and Street View links.

### 2. 🚧 Live Works & Police Decrees Tracker (`Europe/Rome`)
- **Direct Municipal Gazette Integration:** Tracks official police decrees issued by the Municipality of Collesalvetti for FTTH FiberCop roadworks.
- **Accurate working-hours status computation:**
  - `PROGRAMMATO`: prior to formal decree start date.
  - `CANTIERE ATTIVO ORA`: strictly active during authorized working hours (**08:00 – 18:00 on weekdays**).
  - `NON LAVORATIVO`: on Sundays and national public holidays during decree validity, with clear non-working day notifications.
  - `FUORI ORARIO`: outside 08:00–18:00 on weekdays.
  - `LAVORI CONCLUSI`: following expiration of authorized dates.
- **Clear separation between official decrees and field survey findings:** field survey postponements (`slittamento_osservato`) are highlighted separately.

### 3. 📖 Technical Telecom Wiki (`wiki.html`)
- 11 structured articles written in accessible yet rigorous Italian.
- Comparative tables with physical, optical, and regulatory standards (ITU-T G.652, G.657, G.984, G.9807.1, AGCOM broadband labeling).
- Lightweight standalone client-side Markdown rendering engine (`marked.min.js`), instant client-side search, and formal bibliography cards.

---

## 📊 Official Data & Metrics (Snapshot 3)

All metrics are deterministically computed from the official geospatial survey **Snapshot 3 (04/10/2026)**:

| Category | Quantity | Details / Notes |
|---|:---:|---|
| **Total Geospatial Features** | **63** | 34 point elements, 25 line traces, 4 area polygons |
| **Total Mapped Route Length** | **21.716 km** | Cumulative length of microtrenches and backbone lines |

<!-- AUTO-STATS:BEGIN equipment -->
Equipment = a surveyed network point (ARL/ARLO cabinet or central office). Lines, polygons and infrastructure points are not equipment. Of the 34 points in the snapshot, 33 are equipment (32 inside the municipality + 1 outside it) and 1 is an infrastructure point that is not counted.

| Equipment type | GIS category | Quantity | Notes |
|---|---|:---:|---|
| **Copper cabinet (ARL)** | `arl` | **23** | |
| **Optical cabinet (ARLO)** | `arlo` | **2** | |
| *Total cabinets (ARL + ARLO)* | | *25* | |
| **Municipal central office** | `centrale_comunale` | **1** | |
| **Fraction central offices** | `centrale_frazione` | **6** | |
| **Total equipment within the municipality** | | **32** | |
| Equipment outside the municipality (not included in the total): Centrale Feeder (Livorno Nord) | `centrale_feeder` | 1 | outside the municipal territory |
| Non-equipment points (excluded from the count): Coppie di corrugati scoperti | `infrastruttura` | 1 | infrastructure point, not equipment |
<!-- AUTO-STATS:END equipment -->

### Route Length and Apparatus by Fraction

<!-- AUTO-STATS:BEGIN frazioni -->
| Fraction | Equipment | ARLO | ARL | Central offices | Routes (km) | Share % km |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Stagno** | 8 | 2 | 5 | 1 | 8.431 km | 38.8% |
| **Collesalvetti** | 8 | 0 | 7 | 1 | 3.290 km | 15.2% |
| **Vicarello** | 9 | 0 | 8 | 1 | 0.000 km | 0.0% |
| **Guasticce** | 4 | 0 | 3 | 1 | 0.000 km | 0.0% |
| **Nugola** | 1 | 0 | 0 | 1 | 0.000 km | 0.0% |
| **Parrana San Martino** | 1 | 0 | 0 | 1 | 0.000 km | 0.0% |
| **Parrana San Giusto** | 1 | 0 | 0 | 1 | 0.000 km | 0.0% |
| **Other / unassigned** | 0 | 0 | 0 | 0 | 9.995 km | 46.0% |
| **Total** | 32 | 2 | 23 | 7 | 21.716 km | 100.0% |

*Equipment is counted per fraction inside the municipality only; route km also include the INFRATEL BUL backbone and routes with no fraction (`Altro`).*
<!-- AUTO-STATS:END frazioni -->


---

## 📋 Municipal Works & Decrees Registry

Documented with `data/ordinanze.json` as the single source of truth, distinguishing both Police Sector numbers (P.M.) and General Register numbers (Reg. Gen.):

1. **Cantiere 2 - Stagno (FTTH Rollout):**
   - **Decree:** Ordinanza P.M. n. 95 del 10/09/2026 (**Reg. Gen. 102**)
   - **Authorized period:** 21/09/2026 – 16/10/2026 (weekdays 08:00 – 18:00)
   - **Field survey finding:** Observed postponement starting 05/10/2026 through 17/10/2026.
   - **Streets:** Via Otto Marzo, Via Romita, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio.
2. **Cantiere 1 - Collesalvetti Center:**
   - **Decree:** Ordinanza P.M. n. 88 del 02/09/2026 (**Reg. Gen. 95**)
   - **Authorized period:** 14/09/2026 – 02/10/2026. *Expired.*
   - **Field survey finding (03/10/2026):** 2 routes completed, 5 routes unexecuted (blue spray marks only).
3. **Road Resurfacing - Stagno:**
   - **Decree:** Ordinanza P.M. n. 70 del 16/07/2026 (**Reg. Gen. 75**)
   - **Authorized period:** 03/08/2026 – 13/08/2026. *Formally and physically completed.*
4. **Routes with pending ordinance linkage:**
   - **Cantiere 3 Via Aiaccia (Stagno):** 4 line traces totaling 3.475 km (field note 19/10 - 23/10).
   - **Opera Backbone:** 519 m interurban route towards Livorno.

---

## 📚 Technical Wiki Articles

Accessible on both desktop and mobile at [`wiki.html`](wiki.html):

| Article | File | Overview |
|---|---|---|
| **1. How FTTH Works** | `wiki/ftth-come-funziona.md` | Total internal reflection, attenuation, passive optical network (PON) topology. |
| **2. Technologies Compared** | `wiki/tecnologie-a-confronto.md` | FTTH, FTTC, FWA, and ADSL comparison table with AGCOM quality badges. |
| **3. PON Standards** | `wiki/standard-pon.md` | GPON (G.984), XGS-PON (G.9807.1), wavelength allocation, WDM1r coexistence. |
| **4. Equipment on the Ground** | `wiki/apparati-sul-territorio.md` | Visual guide to OLT, Feeder, ARLO, manholes, IP68 splice closures, and building PTE/ROE. |
| **5. Fibers and Connectors** | `wiki/fibre-e-connettori.md` | G.652.D vs G.657 bend-insensitive fibers, SC/APC vs SC/UPC, CEI 86-46 color coding. |
| **6. Wholesale & Public Plans** | `wiki/operatori-e-piani-pubblici.md` | FiberCop, Open Fiber, White/Gray/Black market zones, PNRR Piano Italia a 1 Giga. |
| **7. Anatomy of a Worksite** | `wiki/anatomia-di-un-cantiere.md` | Permit processes, microtrenching, No-Dig (HDD), and the 3 mandatory asphalt restoration stages. |
| **8. Completion to Activation** | `wiki/dalla-fine-dei-lavori-allattivazione.md` | Fiber blowing, OTDR testing, wholesale database provisioning, home delivery install. |
| **9. Technical Glossary** | `wiki/glossario.md` | 40+ rigorous definitions of telecom acronyms, protocols, and devices. |
| **10. Citizen & Condo FAQ** | `wiki/faq.md` | Condominium rights (CCE art. 91), street spray markings, number portability, costs. |
| **11. Local Network in Collesalvetti** | `wiki/collesalvetti.md` | Audited data and fraction breakdown derived from Snapshot 3 (63 features, 21.72 km). |

---

## 🏛️ Repository Architecture

```
geofibra/
├── index.html                   # GIS Cartography (Desktop/Tablet) + Mobile Blocker
├── wiki.html                    # Standalone Wiki Reader (Desktop & Mobile)
├── start_server.py              # Cross-platform Python local HTTP server
├── css/
│   ├── app.css                  # Core GIS styling
│   └── wiki.css                 # Typography and horizontally scrollable tables
├── data/
│   ├── network_data.json        # Unified GeoJSON FeatureCollection (Snapshot 3, 63 features)
│   ├── ordinanze.json           # Single source of truth for municipal decrees
│   ├── rete_ftth_collesalvetti.xlsx # Native Microsoft Excel export
│   ├── rete_ftth_collesalvetti_*.csv # Standard and Italian CSV exports
│   └── snapshots/               # Historical KML archives and CHANGELOG_DATI.md
├── js/
│   ├── data.js                  # Exposes window.FTTH_NETWORK_DATA
│   ├── cantieri_tracker.js      # Working hours calculation engine (Europe/Rome)
│   ├── map.js                   # Leaflet map instance and popups
│   ├── telemetry.js             # Network counters and equipment search
│   └── main.js                  # Application initialization
├── docs/
│   └── HANDOFF_REDESIGN.md      # UI/UX design handoff guide and architectural invariants
├── vendor/
│   └── marked.min.js            # Pinned client-side Markdown parser (v11.1.1)
├── wiki/
│   ├── index.json               # Structured catalog of 11 articles
│   ├── articles_data.js         # Offline fallback bundle for file:// execution
│   └── *.md                     # Markdown article files
├── ordinanze/                   # Official municipal PDF decrees
└── scripts/
    ├── kml_to_geojson.py        # KML to GeoJSON parser (Haversine & polygon metrics)
    └── export_sheets.py         # CSV & Excel spreadsheet export pipeline
```

---

## ⚙️ Data Pipeline & Reproducibility

All datasets are deterministically regenerated from the primary KML survey via Python:

```bash
# 1. Regenerate data/network_data.json and js/data.js from current KML
python scripts/kml_to_geojson.py

# 2. Regenerate CSV files and Excel workbook (data/rete_ftth_collesalvetti.*)
python scripts/export_sheets.py
```

Step 1 also runs `scripts/compute_stats.py`, which writes `data/stats.json` and `js/stats.js`: the **single source of counts** (equipment, features, km) read by the site statistics panel. To realign the auto-generated Markdown blocks (marked with `<!-- AUTO-STATS:BEGIN ... -->`) and `wiki/articles_data.js`:

```bash
# 3. Regenerate the statistics blocks of README, README_EN and wiki/collesalvetti.md and the wiki bundle
python3 scripts/sync_docs.py

# 4. Check consistency (statistics and Excel export integrity tests)
python3 -m unittest tests.test_stats -v
python3 -m unittest tests.test_xlsx_export -v
```

Definition of *equipment* and methodology: `docs/APPARATI_RECOUNT.md`. Full order: `kml_to_geojson.py` → `export_sheets.py` → `sync_docs.py` → tests.

---

## 🚀 Local Quick Start

No Node.js or build steps required. Launch with standard Python:

```bash
python start_server.py
```

The server opens your default browser at `http://localhost:8080`.

---

## 🌐 Deployment on GitHub Pages & Renaming

Hosted as a static website on **GitHub Pages**.

### Repository Renaming Checklist:
1. In GitHub: `Settings` $\rightarrow$ `General` $\rightarrow$ `Repository name` $\rightarrow$ change to **`geofibra`**.
2. Update repository description:
   > *"Civic FTTH network observatory & municipal works tracker in Collesalvetti (LI) with technical ultrabroadband wiki"*
3. Update topics: `ftth`, `fibercop`, `open-fiber`, `leaflet`, `gis`, `collesalvetti`, `open-data`, `civic-tech`.
4. Ensure GitHub Pages is set to **Deploy from a branch** $\rightarrow$ `main` / root.
5. Update your local git remote:
   ```bash
   git remote set-url origin https://github.com/hainetsoftware/geofibra.git
   ```

---

## ⚖️ Disclaimer & License

This project is an independent, non-profit civic initiative. It is not affiliated with or endorsed by FiberCop, TIM, Fastweb, Open Fiber, or the Municipality of Collesalvetti.

Source code is released under the **MIT License**. Geospatial data and technical articles are published under open civic terms.
