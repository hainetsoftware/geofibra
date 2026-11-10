# AGENTS.md — Contributor & AI Agent Specification for Geo Fibra

## 1. Project Overview & Scope

- **Project name** — Geo Fibra, formerly FiberPulse.
- **Objective** — Track the FTTH FiberCop / FlashFiber rollout and index historical roadwork ordinances for Comune di Collesalvetti. The survey covers Stagno, Collesalvetti capoluogo, Vicarello, and neighboring provincial corridors SP4, SP555, and SR206.
- **Core stack** — Static HTML, CSS, and JavaScript with Leaflet and GeoJSON. Python 3 scripts convert survey data and generate application bundles, statistics, and spreadsheet exports.

## 2. Directory Structure

- `data/kml_snapshots/` holds raw chronological KML exports from Google Earth and `CHANGELOG_DATI.md`. Preserve the original files and Placemark IDs.
- `data/wholesale/` holds official FiberCop / TIM wholesale CSV reports.
- `data/ordinanze/` holds municipal and provincial roadwork ordinance PDFs from 2020 onward. Index each new PDF in `data/ordinanze/ordinanze.json` using a stable record ID, an issuing authority, ISO dates, and a filename relative to the archive.
- `data/ordinanze.json` is the map's ordinance tracker dataset. Its PDF paths are relative to the site root. Keep its offline fallback in `js/cantieri_tracker.js` in sync.
- `data/network_data.json` and `js/data.js` are the generated GeoJSON and browser bundle. `data/stats.json` and `js/stats.js` hold derived counts and lengths.
- `index.html`, `js/`, and `css/` contain the application, including the map panes, inspection popups, ordinance drawer, and layer filters. `wiki/` contains articles and the generated offline wiki bundle.
- `scripts/` contains the data pipeline. `tests/` checks source KML, generated outputs, documentation, and exports.

## 3. Data Entities & Lifecycle

### Cabinet classifications

- `ARLO 384` — Full-size optical cabinet, approximately 1.55 m tall or 1.70 m with the concrete plinth. Primary model in Stagno and Collesalvetti.
- `ARLO 192` — Compact optical cabinet for constrained footprints.
- `ARL [XX]` — Pre-existing TIM copper distribution cabinet.

### Worksite lifecycle

- `planned` — Authorized by ordinance and awaiting physical works.
- `executive_design` — Spray markings on tarmac, conduit validation, or Fender reels staged on site. Use `staged_for_digging` in `cantiere.stato_base` when field observations confirm staging for excavation.
- `civil_works_done` — Microtrenching complete, subducts installed, and temporary white mortar applied.
- `splicing_blowing` — Cable blowing into subducts, PTE installation, and optical fusion splicing.
- `completed` — Wholesale CRO marked `ATTIVO` by FiberCop, with pre-order availability indicated by “In arrivo” where observed.

Keep field evidence, ordinance validity, and wholesale availability separate. The lifecycle above describes the domain. The current parser and UI also use legacy codes such as `completato` for civil works. Check existing filters and exports before changing emitted codes.

## 4. Map UX & Event Priority Rules

- Background coverage polygons (`Area Coperta` and `Area NON Coperta`) use `polygonsPane` at z-index 350 with non-bubbling click events.
- Trench routes use `linesPane` at z-index 450. Use non-bubbling click events and stop propagation with `L.DomEvent.stopPropagation(e)`.
- Cabinet pins (ARLO, ARL, and centrali) use `markersPane` at z-index 600.
- When a trench overlaps a coverage polygon, clicking the trench must open the trench's inspection popup. Clicking exposed coverage opens the polygon popup.
- Executive-design routes use `#007cf5`. Google Earth can regenerate or share managed style IDs across categories. Classify the route before applying the category palette.

## 5. Development Workflow

1. Archive the new KML under `data/kml_snapshots/`. Compare it to the previous snapshot by Placemark ID, geometry, name, and style. Record additions, removals, geometry changes, and field observations in `CHANGELOG_DATI.md`.
2. Cross-reference trench features with `data/ordinanze/ordinanze.json` and the source PDF. Record the authorization window separately from survey dates and observed progress.
3. Enrich ARLO pins with verified wholesale metadata from `data/wholesale/`. Preserve the Element ID (`LIVOITA...`), ACL code, and availability date.
4. Update the parser's default source and survey date when promoting a new snapshot. Run the pipeline from the repository root and commit source changes alongside their generated outputs.

   ```bash
   python3 scripts/kml_to_geojson.py
   python3 scripts/export_sheets.py
   python3 scripts/sync_docs.py
   python3 scripts/sync_docs.py --check
   python3 -m unittest discover -v
   ```

5. Start the application with `python3 start_server.py`. Check the executive-design filter, ordinance PDF links, and trench inspection where routes overlap coverage polygons. The Python pipeline and tests are the current pre-commit checks. If a future frontend migration introduces a package build, run `npm run build` before committing.
