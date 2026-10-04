# Manuale di Handoff Tecnico per il Redesign UI/UX

Questo documento costituisce la guida operativa e il contratto architetturale per il designer / ingegnere frontend che si occuperà del futuro redesign dell'interfaccia utente del portale.

---

## 1. Vincoli Architetturali Non Negoziabili

1. **Sito Statico Puro su GitHub Pages:**
   - Nessun ambiente Node.js obbligatorio a runtime, nessun bundler obbligatorio (zero npm, vite o webpack).
   - Il sito deve funzionare servendo file statici da qualunque web server o aprendo i file direttamente su GitHub Pages.
   - Eventuali librerie terze devono essere rigorosamente **vendorizzate in locale** (come `vendor/marked.min.js`) oppure richiamate da CDN con versione esplicitamente fissata e hash di integrità.
2. **Percorsi Relativi Obbligatori:**
   - Non utilizzare mai percorsi assoluti con slash iniziale (es. non usare mai `/css/` o `/data/`).
   - Usare sempre percorsi relativi (`css/app.css`, `data/network_data.json`) perché il repository subirà un cambio di nome e l'URL di GitHub Pages cambierà path radice.
3. **Dispositivi Ammessi: Desktop e Tablet Only per la Mappa GIS:**
   - La mappa Leaflet, l'HUD di telemetria e il tracker dei cantieri sono rigorosamente riservati a schermi con larghezza $\ge$ **768 pixel**.
   - Su schermi di smartphone (< 768 px), la mappa e i dati geografici **non devono essere scaricati né inizializzati**. Viene mostrato il blocco a tutto schermo (`#mobile-blocker`) la cui unica interazione consentita è il link verso la Wiki (`wiki.html`).
4. **Wiki Mobile-Friendly:**
   - La documentazione tecnica e divulgativa (`wiki.html`) è l'unica sezione accessibile da smartphone e deve rimanere pienamente fruibile (con font leggibili e tabelle racchiuse in `.table-wrapper` per lo scroll orizzontale).

---

## 2. Struttura dei File e Architettura JavaScript

Attualmente il progetto impiega JavaScript vanilla modulare senza router ad hash né moduli ES, per garantire compatibilità immediata:

```
├── index.html                   # Pagina principale GIS (Desktop/Tablet) + Blocco Mobile
├── wiki.html                    # Lettore autonomo della Wiki Tecnica (Desktop + Mobile)
├── css/
│   ├── app.css                  # Foglio stile principale (stili cyber, animazioni pulse)
│   └── wiki.css                 # Foglio stile dedicato alla lettura dei markdown
├── data/
│   ├── network_data.json        # GeoJSON FeatureCollection rigenerato da Snapshot 3 (63 feature)
│   ├── ordinanze.json           # Fonte unica di verità per atti e cantieri comunali
│   ├── rete_ftth_collesalvetti.xlsx # Foglio elettronico ufficiale di export
│   └── snapshots/               # Storico versionato dei rilievi KML e CHANGELOG_DATI.md
├── js/
│   ├── data.js                  # Assegna window.FTTH_NETWORK_DATA (sincrono con network_data.json)
│   ├── cantieri_tracker.js      # Calcolo orari feriali Europe/Rome e modale cantieri
│   ├── map.js                   # Inizializzazione Leaflet, layer tiles, confini toscani, popup
│   ├── telemetry.js             # Calcolo statistiche rete, filtri e ricerca apparati
│   └── main.js                  # Punto d'ingresso e coordinamento eventi UI
├── vendor/
│   └── marked.min.js            # Parser Markdown autonomo (v11.1.1)
├── wiki/
│   ├── index.json               # Indice catalogo delle 11 voci
│   ├── articles_data.js         # Fallback offline dei markdown per esecuzione diretta
│   └── *.md                     # I file Markdown delle 11 voci tecniche e divulgative
└── scripts/
    ├── kml_to_geojson.py        # Pipeline rigenerazione GeoJSON da KML
    └── export_sheets.py         # Pipeline rigenerazione CSV e XLSX da GeoJSON
```

---

## 3. Elementi DOM Critici (ID e Classi da NON Rompere)

Il codice JavaScript esistente effettua query dirette su specifici ID del documento. Nel ridisegnare la grafica, questi ID **devono essere preservati**:

### A. Mappa e Livelli Cartografici (`js/map.js`)
- `#map`: Contenitore della mappa Leaflet.
- `.layer-btn`: Pulsanti di commutazione dei layer cartografici. Ciascun pulsante deve avere l'attributo `data-layer` impostato su `topo`, `satellite` o `dark`.
- `.active-layer`: Classe applicata dal JS al pulsante del layer correntemente selezionato.

### B. Telemetria e Statistiche di Rete (`js/telemetry.js`)
- `#stat-tot`: Contatore numerico totale apparati/elementi.
- `#stat-km`: Lunghezza complessiva delle tratte (in chilometri).
- `#stat-arl`: Conteggio armadi rame ARL.
- `#stat-arlo`: Conteggio armadi ottici ARLO.
- `#stat-centrali`: Conteggio centrali TLC.
- `#stat-cantieri`: Conteggio tratte/cantieri rilevati.
- `#frazioni-nav`: Contenitore dove vengono iniettati dinamicamente i bottoni per centrare la mappa sulle frazioni.
- `#frazioni-stats`: Contenitore delle barre di distribuzione percentuale per frazione.
- `#search-elements`: Campo di input per la ricerca testuale rapida.
- `#elements-list`: Contenitore in cui viene renderizzata la lista filtrabile degli apparati.

### C. Registro Cantieri e Ordinanze (`js/cantieri_tracker.js` & `js/main.js`)
- `#btn-open-cantieri`: Pulsante che apre il modale delle ordinanze.
- `#btn-close-cantieri`: Pulsante che chiude il modale delle ordinanze.
- `#modal-cantieri`: Contenitore del modale (il JS alterna le classi `hidden` e `flex`).
- `#cantieri-count-badge`: Badge nella barra di navigazione con il conteggio delle ordinanze in corso o future.
- `#cantieri-live-clock`: Elemento in cui viene iniettato ogni secondo l'orario ufficiale di Roma (`Europe/Rome`).
- `#cantieri-list-container`: Griglia/contenitore in cui vengono generate le schede delle ordinanze.

### D. Blocco Mobile (`index.html`)
- `#mobile-blocker`: Schermata di blocco visualizzata su schermi < 768px.
- `#desktop-app-container`: Contenitore dell'intera applicazione desktop/tablet.

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
- `file_pdf`: percorso relativo al documento PDF originale presente nella cartella `ordinanze/`.
- `coordinate_centro`: array `[lat, lng]` per l'inquadramento con `flyTo`.

---

## 5. Logica del Calcolo di Stato del Cantiere

La funzione `calculateCantiereStatus(cantiere, currentDate)` in `js/cantieri_tracker.js` garantisce che:
1. Venga sempre utilizzato il fuso orario **Europe/Rome** (evitando bug nel passaggio tra ora solare ed estiva).
2. Nei giorni festivi e di **domenica** il cantiere **non risulti mai come "attivo ora"**, bensì restituisca l'etichetta `ORDINANZA IN CORSO (NON LAVORATIVO)` con il messaggio esplicito:
   > *"Oggi non è un giorno lavorativo (feriali 08:00 - 18:00)"*
3. Dal lunedì al sabato, ma **fuori dalla fascia oraria 08:00 – 18:00**, restituisca `ORDINANZA IN CORSO (FUORI ORARIO)`.
4. Solo ed esclusivamente nei giorni feriali tra le 08:00 e le 18:00 venga mostrato `CANTIERE ATTIVO ORA`.

---

## 6. Mappa degli Stili Sparsi nel Codice da Riordinare

Durante il redesign estetico (passaggio a una grafica sobria e civica), chi interverrà dovrà tenere presente che alcuni stili attuali sono generati direttamente all'interno del codice JavaScript:

1. **Card dei Cantieri (`js/cantieri_tracker.js`):**
   - L'HTML generato dentro `renderCantieriModal()` contiene classi Tailwind inline come `glass-panel`, `border-cyber-border/50`, `text-cyber-neon`, ecc.
2. **Popup della Mappa (`js/map.js`):**
   - La funzione `onEachFeature` costruisce l'HTML del popup Leaflet includendo proprietà inline `style="background: ${props.color}33; color: ${props.color}"`.
3. **Marker Personalizzati Leaflet (`js/map.js`):**
   - La funzione `getIconHtml` genera icone SVG inline con colori hardcoded e stili `background: rgba(10, 13, 20, 0.85); border: 1px solid ${color}`.
4. **Telemetria e Barre Frazioni (`js/telemetry.js`):**
   - Le barre di percentuale usano `style="width: ${pct}%"` con colore di sfondo `bg-cyber-neon`.
5. **Configurazione Tailwind (`index.html` e `wiki.html`):**
   - Contiene il blocco `<script> tailwind.config = ... </script>` con la palette personalizzata `cyber`.

---

## 7. Cosa NON va Modificato o Rotto

- **Non inventare ordinanze o date:** Cantiere 3 (Via Aiaccia) e Opera sulla Backbone non hanno atti reperiti; devono rimanere etichettati come *"da collegare a un'ordinanza"*.
- **Non alterare i numeri di Snapshot 3:** I dati ufficiali della rete sono 63 feature, 21,716 km, 34 apparati. Qualsiasi modifica deve passare dalla rigenerazione deterministica tramite `scripts/kml_to_geojson.py`.
- **Non rimuovere la doppia numerazione delle ordinanze:** Polizia Municipale e Registro Generale del Comune sono due numerazioni distinte e necessarie per la trasparenza civica.
