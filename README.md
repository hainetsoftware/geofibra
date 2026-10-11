# 🌐 GeoFibra Collesalvetti
### *Osservatorio Civico della Rete FTTH e Registro Cantieri nel Comune di Collesalvetti (LI)*

[![Licenza: MIT](https://img.shields.io/badge/Licenza-MIT-blue.svg)](LICENSE)
[![GIS: Leaflet 1.9.4](https://img.shields.io/badge/GIS-Leaflet%201.9.4-brightgreen.svg)](https://leafletjs.com/)
[![Dati: Snapshot 4](https://img.shields.io/badge/Dati-Snapshot%204%20(11%2F10%2F2026)-orange.svg)](#-dati-e-statistiche-ufficiali-snapshot-4)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Attivo-success.svg)](#-pubblicazione-su-github-pages)

---

**GeoFibra Collesalvetti** è una piattaforma civica e documentale open source che mappa l'infrastruttura di telecomunicazioni in fibra ottica (**FTTH FiberCop / Wholesale**), monitora in tempo reale le **ordinanze municipali di scavo** e offre un'**enciclopedia tecnica e divulgativa** sulla banda ultralarga in Italia.

Il progetto nasce per garantire trasparenza sull'avanzamento dei lavori stradali, sui tempi di ripristino dell'asfalto e sullo stato reale della connettività a Collesalvetti e nelle sue frazioni.

> [!IMPORTANT]
> **Dispositivi supportati:**
> - **Mappa GIS e Tracker Cantieri:** Sviluppati per **computer desktop e tablet** ($\ge$ 768 px). Su smartphone un blocco a tutto schermo motiva l'esigenza di una risoluzione grafica adeguata per la lettura dei tracciati ad alta densità e non carica le librerie cartografiche né i dati geografici.
> - **Wiki Tecnica:** Pienamente accessibile e ottimizzata per la lettura su **qualsiasi dispositivo**, compresi smartphone (con tabelle a scorrimento orizzontale dedicate).

---

## 📑 Indice

1. [Caratteristiche del Portale](#-caratteristiche-del-portale)
2. [Dati e Statistiche Ufficiali (Snapshot 4)](#-dati-e-statistiche-ufficiali-snapshot-4)
3. [Registro Cantieri e Ordinanze di Polizia Municipale](#-registro-cantieri-e-ordinanze-di-polizia-municipale)
4. [La Wiki Tecnica e Divulgativa](#-la-wiki-tecnica-e-divulgativa)
5. [Architettura del Repository](#-architettura-del-repository)
6. [Pipeline Dati e Riproducibilità](#-pipeline-dati-e-riproducibilit%C3%A0)
7. [Avvio Rapido Locale](#-avvio-rapido-locale)
8. [Pubblicazione su GitHub Pages e Ridenominazione](#-pubblicazione-su-github-pages-e-ridenominazione)
9. [Dichiarazione d'Indipendenza e Licenza](#-dichiarazione-dindipendenza-e-licenza)

---

## 🌟 Caratteristiche del Portale

### 1. 🗺️ Mappa Cartografica GIS ad Alta Precisione (Desktop/Tablet)
- **Visualizzazione multilivello:** commutazione istantanea tra *OpenStreetMap*, ortofoto *Satellite HD (Esri)* e visuale ad alto contrasto *Cyber Dark*.
- **Vincolo geografico:** navigazione limitata al perimetro toscano (`TOSCANA_BOUNDS`) per impedire disorientamenti fuori zona.
- **Tracciati e apparati vettoriali:** minitrincee, dorsali primarie, armadi ARLO, ARL rame, centrali e pozzetti con popup completi di quote metriche, note di rilievo e link a Google Street View.
- **Filtro interattivo cantieri:** selezione rapida per visualizzare tratte completate, cantieri in completamento (C2), autorizzati (C3) o in attesa di proroga (C1).

### 2. 🚧 Tracker Ordinanze e Cantieri Stradali (Tempo Reale Europe/Rome)
- **Incrocio con l'Albo Pretorio:** collegamento diretto agli atti di disciplina della circolazione emessi dal Comune di Collesalvetti.
- **Calcolo dinamico dello stato lavorativo:**
  - `PROGRAMMATO`: prima dell'inizio formale dell'atto.
  - `IN COMPLETAMENTO`: cantieri con condotte posate e pozzetti in chiusura finale (es. Cantiere 2 Stagno).
  - `CANTIERE ATTIVO ORA`: solo ed esclusivamente nei **giorni feriali** e nella fascia autorizzata (**08:00 – 18:00**).
  - `NON LAVORATIVO`: di domenica o nei giorni festivi con ordinanza vigente, con avviso esplicito di sospensione dei lavori.
  - `FUORI ORARIO`: nelle ore serali e notturne feriali.
  - `LAVORI CONCLUSI`: alla scadenza dei termini autorizzati.
- **Distinzione tra atto formale e rilievo di campo:** evidenziazione separata di eventuali posticipi osservati sul terreno (`slittamento_osservato`).

### 3. 📖 Enciclopedia Tecnica della Fibra Ottica (`wiki.html`)
- 11 voci di approfondimento scritte in italiano chiaro e rigoroso.
- Tabelle comparative con parametri fisici e normativi conformi a standard ITU-T, AGCOM e MIMIT.
- Motore di rendering autonomo leggero (`marked.min.js`), ricerca istantanea e box fonti strutturato.

---

## 📊 Dati e Statistiche Ufficiali (Snapshot 4)

Tutti i conteggi sono calcolati deterministicamente sul rilievo geospaziale **Snapshot 4 dell'11/10/2026**:

| Categoria Elemento | Quantità | Dettaglio / Note |
|---|:---:|---|
| **Feature Geospaziali Totali** | **68** | 37 punti, 27 linee, 4 poligoni di perimetro |
| **Estensione Tracciati Rete** | **21,780 km** | Somma metrica di tutte le tratte stradali e dorsali (+64 m da rotatoria e nuove tratte) |
| **Armadi Ottici ARLO (FiberCop)** | **4** | 1 nel capoluogo (`C [] ARLO`, futuro ARLO 01) + 3 a Stagno (`S [27]`, `S [28]`, `S []` su Via Romita) |
| **Armadi Rame ARL (TIM)** | **24** | 7 a Collesalvetti, 8 a Vicarello, 6 a Stagno, 3 a Guasticce |
| **Centrali di Commutazione TLC** | **8** | 1 comunale (Collesalvetti), 6 di frazione + 1 Feeder (Livorno) |
| **Tasso Avanzamento Comunale** | **62,8%** | Stagno all'86,4%, Collesalvetti al 41,5% |

### Ripartizione Chilometrica e Apparati per Frazione

| Frazione | Tratte (km) | Quota % | ARLO Fibra | ARL Rame | Centrali TLC | Avanzamento |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Stagno** | **11,525 km** | 52,9% | 3 | 6 | 1 | **86,4%** |
| **Collesalvetti (Capoluogo)** | **6,516 km** | 29,9% | 1 | 7 | 1 | **41,5%** |
| **Vicarello** | **3,122 km** | 14,3% | 0 | 8 | 1 | **35,0%** |
| **Guasticce** | **0,399 km** | 1,8% | 0 | 3 | 1 | **20,0%** |
| **Altro / Intercomunale** | **0,519 km** | 2,4% | 0 | 0 | 1 | - |
| **Totale Territoriale** | **21,780 km** | **100,0%** | **4** | **24** | **8** | **62,8%** |

---

## 📋 Registro Cantieri e Ordinanze di Polizia Municipale

Questo osservatorio adotta come unica fonte di verità documentale `data/ordinanze.json`, citando sia il numero interno di settore della Polizia Municipale (P.M.) sia il Registro Generale (Reg. Gen.):

1. **Cantiere 2 - Stagno (Nuova Espansione FTTH):**
   - **Atto:** Ordinanza P.M. n. 95/2026 (**Reg. Gen. 102/104/2026**)
   - **Periodo ufficiale:** 21/09/2026 – 17/10/2026 (feriali 08:00 – 18:00)
   - **Rilievo di campo:** Finestra effettiva 05/10 - 17/10. Stato *In completamento* (posa condotte completata, 6 pozzetti in chiusura, tratta via Romita/XXV Aprile verificata come completata per 292,9 m). Nuovo ARLO posato adiacente a S [04] ARL (privo di etichetta numerica, 3° ARLO censito a Stagno).
   - **Vie:** Via Romita sud, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio, Via Don Verità, Via 8 Marzo.
2. **Cantiere 3 - Stagno (Via Aiaccia / Via Umbria):**
   - **Atto:** Ordinanza P.M. n. 105/2026 (**Reg. Gen. 105**) + Concessione Suolo n. 77/2026 (60 mq)
   - **Periodo ufficiale:** 19/10/2026 – 23/10/2026 (5 giorni feriali, 08:00 – 18:00)
   - **Stato:** *Autorizzato / Avvio programmato*. Raccordo con dorsale provinciale SP555.
3. **Cantiere 1 - Collesalvetti Centro:**
   - **Atto:** Ordinanza P.M. n. 88 del 02/09/2026 (**Reg. Gen. 95**)
   - **Periodo ufficiale:** 14/09/2026 – 02/10/2026. *Termini scaduti.*
   - **Rilievo di campo (11/10/2026):** Tratte Sud-Est e anello rotatoria (71,8 m) eseguite con minitrincea sigillata (Fender 4x10/14), 4 pozzetti FiberCop e primo ARLO cittadino (`C [] ARLO`, futuro ARLO 01). Tratte Nord-Ovest (Via Nenni) non eseguite (soli segni spray blu su asfalto, in attesa di proroga).
4. **Ripristino Manto Stradale - Stagno:**
   - **Atto:** Ordinanza P.M. n. 70 del 16/07/2026 (**Reg. Gen. 75**)
   - **Periodo ufficiale:** 03/08/2026 – 13/08/2026. *Lavori conclusi.*
   - **Vie:** Via Marx, Via Guerrazzi, Via La Malfa.
5. **Tratte senza ordinanza comunale ordinaria:**
   - **Opera sulla Backbone:** Tratta interurbana di 519 metri verso Livorno lungo la provinciale SP555.

---

## 📚 La Wiki Tecnica e Divulgativa

Accessibile da desktop e da smartphone all'indirizzo [`wiki.html`](wiki.html):

| Voce | File | Argomento Trattato |
|---|---|---|
| **1. Come Funziona la Fibra FTTH** | `wiki/ftth-come-funziona.md` | Riflessione totale interna, attenuazione in dB/km, architettura albero PON. |
| **2. Tecnologie a Confronto** | `wiki/tecnologie-a-confronto.md` | Tabella comparativa FTTH, FTTC, FWA, ADSL e bollini AGCOM (Verde, Giallo, Rosso). |
| **3. Standard PON** | `wiki/standard-pon.md` | GPON (G.984), XGS-PON (G.9807.1), lunghezze d'onda e filtro di coesistenza WDM1r. |
| **4. Apparati sul Territorio** | `wiki/apparati-sul-territorio.md` | Come riconoscere OLT, Feeder, ARLO, pozzetti rompitratta, muffole IP68 e PTE/ROE. |
| **5. Fibre e Connettori** | `wiki/fibre-e-connettori.md` | Fibre G.652.D vs G.657, connettori verdi SC/APC vs blu SC/UPC, codice colori CEI 86-46. |
| **6. Operatori e Piani Pubblici** | `wiki/operatori-e-piani-pubblici.md` | Wholesale FiberCop e Open Fiber, Aree Bianche/Grigie/Nere, PNRR Piano Italia a 1 Giga. |
| **7. Anatomia di un Cantiere** | `wiki/anatomia-di-un-cantiere.md` | Iter SUAP/PM, minitrincea, No-Dig e le tre fasi obbligatorie del ripristino asfalto. |
| **8. Fine Lavori e Attivazione** | `wiki/dalla-fine-dei-lavori-allattivazione.md` | Soffiaggio cavi, collaudo riflettometrico OTDR, vendibilità wholesale e delivery utente. |
| **9. Glossario Tecnico** | `wiki/glossario.md` | Oltre 40 lemmi e definizioni rigorose di acronimi, protocolli e apparati. |
| **10. Domande Frequenti (FAQ)** | `wiki/faq.md` | Diritti condominiali (art. 91 CCE), segni spray su asfalto, portabilità e costi. |
| **11. La Rete a Collesalvetti** | `wiki/collesalvetti.md` | Dati territoriali ufficiali di Collesalvetti derivati da Snapshot 3 (63 feature, 21,72 km). |

---

## 🏛️ Architettura del Repository

```
geofibra/
├── index.html                   # Applicazione cartografica GIS (Desktop/Tablet) + Blocco Mobile
├── wiki.html                    # Portale documentale autonomo Wiki (Desktop & Mobile)
├── start_server.py              # Launcher server locale Python multi-piattaforma
├── css/
│   ├── app.css                  # Stili principali per la mappa e i pannelli
│   └── wiki.css                 # Stili per la lettura prose e tabelle a scorrimento
├── data/
│   ├── network_data.json        # GeoJSON FeatureCollection consolidato (Snapshot 3, 63 feature)
│   ├── ordinanze.json           # Fonte di verita' ordinanze e prescrizioni viabilita'
│   ├── rete_ftth_collesalvetti.xlsx # Export Microsoft Excel nativo completo
│   ├── rete_ftth_collesalvetti_*.csv # Export CSV standard e per Excel italiano
│   └── snapshots/               # Archivio KML storici e CHANGELOG_DATI.md
├── js/
│   ├── data.js                  # Assegnazione window.FTTH_NETWORK_DATA
│   ├── cantieri_tracker.js      # Motore calcolo orari Europe/Rome e modale ordinanze
│   ├── map.js                   # Istanza Leaflet, livelli Esri/OSM e popup informativi
│   ├── telemetry.js             # Telemetria, contatori e barra ricerca apparati
│   └── main.js                  # Coordinamento eventi e avvio applicazione
├── docs/
│   └── HANDOFF_REDESIGN.md      # Manuale di architettura per il futuro redesign grafico
├── vendor/
│   └── marked.min.js            # Parser Markdown leggero client-side (v11.1.1 pinned)
├── wiki/
│   ├── index.json               # Catalogo strutturato delle 11 voci
│   ├── articles_data.js         # Fallback dati per esecuzione offline su file://
│   └── *.md                     # I file Markdown delle singole voci
├── ordinanze/                   # File PDF originali delle ordinanze di Polizia Municipale
└── scripts/
    ├── kml_to_geojson.py        # Pipeline di conversione KML -> GeoJSON (Haversine & aree)
    └── export_sheets.py         # Pipeline di generazione fogli CSV e XLSX
```

---

## ⚙️ Pipeline Dati e Riproducibilità

I dati del progetto sono rigenerabili deterministicamente dal rilievo KML sorgente mediante due comandi Python privi di dipendenze pesanti:

```bash
# 1. Rigenera data/network_data.json e js/data.js dal KML corrente
python scripts/kml_to_geojson.py

# 2. Rigenera i file CSV e il foglio Excel (data/rete_ftth_collesalvetti.*)
python scripts/export_sheets.py
```

---

## 🚀 Avvio Rapido Locale

Il sito non richiede Node.js né procedure di build. È possibile avviarlo con Python standard:

```bash
python start_server.py
```

Lo script individuerà una porta TCP libera (default `8080`), aprirà automaticamente il browser predefinito all'indirizzo `http://localhost:8080` e servirà i file con i corretti MIME types.

---

## 🌐 Pubblicazione su GitHub Pages e Ridenominazione

Il portale è ospitato come sito statico su **GitHub Pages**.

### Checklist per la ridenominazione del repository:
1. Accedi a GitHub: `Settings` $\rightarrow$ `General` $\rightarrow$ `Repository name` $\rightarrow$ rinomina in **`geofibra`**.
2. Aggiorna la descrizione del repository:
   > *"Osservatorio civico della rete FTTH e registro cantieri nel Comune di Collesalvetti (LI) con wiki tecnica sulla banda ultralarga"*
3. Topic consigliati: `ftth`, `fibercop`, `open-fiber`, `leaflet`, `gis`, `collesalvetti`, `open-data`, `civic-tech`.
4. Verifica che GitHub Pages rimanga impostato su **Deploy from a branch** $\rightarrow$ `main` / root.
5. Aggiorna il puntamento remoto nel tuo terminale locale:
   ```bash
   git remote set-url origin https://github.com/hainetsoftware/geofibra.git
   ```

---

## ⚖️ Dichiarazione d'Indipendenza e Licenza

Questo progetto è un'iniziativa informativa e civica indipendente, senza fini di lucro. Non è sponsorizzato né affiliato ad alcuno degli operatori di rete citati (FiberCop, Telecom Italia, Fastweb, Open Fiber) né al Comune di Collesalvetti.

Il codice sorgente è distribuito con licenza **MIT**. I dati geospaziali e i testi della Wiki sono rilasciati per finalità civiche con licenza aperta.
