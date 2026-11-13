# Manuale di Handoff Tecnico per il Redesign UI/UX

Questo documento descrive i vincoli della dashboard di Geo Fibra e i punti da verificare quando si modifica l’interfaccia.

---

## 1. Vincoli Architetturali Non Negoziabili

1. **Sito Statico Puro su GitHub Pages:**
   - Nessun ambiente Node.js obbligatorio a runtime, nessun bundler obbligatorio (zero npm, vite o webpack).
   - Il sito deve funzionare servendo file statici da qualunque web server o aprendo i file direttamente su GitHub Pages.
   - Eventuali librerie terze devono essere rigorosamente **vendorizzate in locale** (come `vendor/marked.min.js`) oppure richiamate da CDN con versione esplicitamente fissata e hash di integrità.
2. **Percorsi Relativi Obbligatori:**
   - Non utilizzare mai percorsi assoluti con slash iniziale (es. non usare mai `/css/` o `/data/`).
   - Usare sempre percorsi relativi (`css/app.css`, `data/network_data.json`) perché il repository subirà un cambio di nome e l'URL di GitHub Pages cambierà path radice.
3. **Desktop e tablet per la mappa GIS.** Da 768 px si caricano Leaflet, dati geografici e tracker. Su smartphone la schermata iniziale offre Archivio Atti e Wiki.
4. **Wiki su tutti i dispositivi.** Conservare la leggibilità degli articoli e lo scorrimento orizzontale delle tabelle in `.table-wrapper`.

---

## 2. Struttura dei File e Architettura JavaScript

Attualmente il progetto impiega JavaScript vanilla modulare senza router ad hash né moduli ES, per garantire compatibilità immediata:

```
├── index.html                   # Dashboard GIS e accesso mobile ad Archivio e Wiki
├── wiki.html                    # Lettore autonomo della Wiki Tecnica (Desktop + Mobile)
├── css/
│   ├── app.css                  # Palette e componenti della dashboard
│   └── wiki.css                 # Foglio stile dedicato alla lettura dei markdown
├── data/
│   ├── network_data.json        # GeoJSON FeatureCollection del rilievo corrente
│   ├── ordinanze.json           # Dati del tracker e finestre autorizzate
│   ├── rete_ftth_collesalvetti.xlsx # Foglio elettronico ufficiale di export
│   └── kml_snapshots/               # Storico versionato dei rilievi KML e CHANGELOG_DATI.md
├── js/
│   ├── data.js                  # Assegna window.FTTH_NETWORK_DATA (sincrono con network_data.json)
│   ├── stats.js                 # Assegna window.FTTH_STATS (specchio di data/stats.json, generato)
│   ├── cantieri_tracker.js      # Calcolo orari feriali Europe/Rome e modale cantieri
│   ├── map.js                   # Inizializzazione Leaflet, sfondi, geometrie e selezione
│   ├── telemetry.js             # Statistiche, risultati e scheda di dettaglio
│   └── main.js                  # Pannello, ricerca, filtri e coordinamento UI
├── vendor/
│   └── marked.min.js            # Parser Markdown autonomo (v11.1.1)
├── wiki/
│   ├── index.json               # Indice catalogo delle 11 voci
│   ├── articles_data.js         # Fallback offline dei markdown per esecuzione diretta
│   └── *.md                     # I file Markdown delle 11 voci tecniche e divulgative
└── scripts/
    ├── kml_to_geojson.py        # Pipeline rigenerazione GeoJSON da KML (poi lancia compute_stats.py)
    ├── compute_stats.py         # Conteggi apparati/feature/km -> data/stats.json, js/stats.js
    ├── sync_docs.py             # Blocchi statistici dei Markdown e bundle wiki da stats.json
    └── export_sheets.py         # Pipeline rigenerazione CSV e XLSX da GeoJSON
```

---

## 3. Controlli della dashboard

- `#map` è la superficie Leaflet. `#map-basemap` seleziona lo sfondo e `#toggle-map-sidebar` espande o richiude il pannello.
- `#search-elements`, `#frazioni-nav` e `.cantiere-filter-btn` alimentano la lista `#elements-list` e le geometrie visibili. I conteggi dei pulsanti tengono conto della ricerca e della frazione.
- `#map-inspection` mostra l’elemento selezionato. Il rilievo, l’ordinanza e i dati wholesale hanno sezioni dedicate. Se un atto collegato rimanda alla stessa geometria, il ritorno conserva selezione, filtri e inquadratura.
- `#telemetry-panel` contiene statistiche comunali da `window.FTTH_STATS`, conteggi per frazione, note del rilievo e download Excel.
- `#modal-cantieri`, `#archivio-atti` e `#archivio-pdf` sono dialoghi nativi. I relativi controlli restano utilizzabili da tastiera.
- Le zone di copertura, le tratte e i marker mantengono i rispettivi livelli Leaflet. Verificare che una tratta selezionabile abbia precedenza quando si sovrappone a una zona di copertura.

---

## 4. Contratto dei Dati (Data Contracts)

### A. Contratto Geospaziale (`data/network_data.json` e `js/data.js`)
Struttura GeoJSON standard conforme a RFC 7946:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "ARLO_01_Stagno",
      "geometry": { "type": "Point", "coordinates": [10.3541, 43.5932] },
      "properties": {
        "id": "ARLO_01_Stagno",
        "name": "ARLO 01 Stagno",
        "category": "arlo",
        "frazione": "Stagno",
        "geom_type": "Point",
        "description": "...",
        "icon": "optical-cabinet",
        "color": "#00f0ff",
        "length_m": 0,
        "length_km": 0,
        "area_m2": 0,
        "area_km2": 0,
        "cantiere": null
      }
    }
  ]
}
```

### B. Contratto Ordinanze Comunali (`data/ordinanze.json`)
Ogni record dell'array delle ordinanze contiene:
- `id` (stringa univoca, es. `cantiere-2-stagno`).
- `titolo`, `frazione`, `richiedente`, `oggetto`.
- `atto_tipo`, `atto_numero` (Polizia Municipale), `atto_registro_generale` (Registro Generale del Comune).
- `codice_atto_completo` (stringa formale con entrambi i numeri di atto).
- `data_emissione` (ISO `YYYY-MM-DD`).
- `periodo_ordinanza`: oggetto con `inizio` e `fine` (ISO 8601 con offset fuso orario), `fascia_oraria` ("08:00 - 18:00") e `giorni` ("feriali").
- `slittamento_osservato`: eventuale oggetto con `nota_campo`, `inizio_stimato` e `fine_stimata` derivati da sopralluoghi sul terreno. Se assente, vale `null`.
- `vie_interessate`: array di oggetti `{ "via": "...", "prescrizione": "..." }`.
- `file_pdf`: percorso relativo al documento PDF originale presente nella cartella `data/ordinanze/`.
- `coordinate_centro`: array `[lat, lng]` per l'inquadramento con `flyTo`.

---

## 5. Stati e palette

Il tracker usa `calculateCantiereStatus` e il fuso `Europe/Rome` per applicare le finestre autorizzate, con domeniche e festività escluse. L’indicazione della fascia oraria si riferisce all’atto. I riscontri di campo descrivono il progresso dell’opera.

## 6. Componenti e cartografia

La dashboard usa la palette chiara di FWA Map Italia in `css/app.css`. Le emoji affiancano le etichette dei controlli. I colori delle tratte mantengono il significato del rilievo, incluso il giallo per gli scavi da avviare. La cartografia iniziale usa OpenStreetMap. La Wiki conserva il proprio foglio di stile in questa fase.

## 7. Cosa NON va Modificato o Rotto

- **Non inventare ordinanze o date:** Consultare l’indice corrente per distinguere gli atti collegati dalle corrispondenze per strada.
- **Conteggi di Snapshot 7:** I dati ufficiali della rete sono 76 feature, 24,673 km, 36 apparati comunali (+1 esterno; 39 è il numero dei *punti*, non degli apparati). I conteggi sono in `data/stats.json` (generato da `scripts/compute_stats.py`). Qualsiasi modifica deve passare dalla rigenerazione deterministica tramite `scripts/kml_to_geojson.py`.
- **Non rompere il pulsante di download Excel:** In `index.html` il pulsante di download ha selettore `a[href="data/rete_ftth_collesalvetti.xlsx"][download]` nella vista Dati del rilievo e punta al percorso relativo `data/rete_ftth_collesalvetti.xlsx`.
- **Non rimuovere la doppia numerazione delle ordinanze:** Polizia Municipale e Registro Generale del Comune sono due numerazioni distinte e necessarie per la trasparenza civica.
