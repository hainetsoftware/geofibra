# Ricalcolo degli apparati (Snapshot 3)

Branch `fix/equipment-recount`. Fonte: `data/snapshots/rilievo_snapshot3.kml` → `scripts/kml_to_geojson.py` → `data/network_data.json` / `js/data.js` → `scripts/compute_stats.py` → `data/stats.json` / `js/stats.js`. Versione metodologia: **1.0**. Tutti i numeri qui sotto sono riproducibili con i comandi della sezione 7.

## 1. Definizione di «apparato»

Un **apparato** è una feature di tipo `Point` la cui `category` è una di:

| `category` | Significato | Apparato? |
|---|---|---|
| `arl` | Armadio ripartilinea (rame) | sì |
| `arlo` | Armadio ripartilinea ottico | sì |
| `centrale_comunale` | Centrale Comunale (Collesalvetti) | sì |
| `centrale_frazione` | Centrali di frazione | sì |
| `centrale_feeder` | Centrale Feeder (Livorno Nord) | sì, ma **esterna al Comune**: riportata a parte, mai sommata ai totali comunali |
| `infrastruttura` (Point) | «Coppie di corrugati scoperti» | **no**: osservazione di infrastruttura, non un apparato (scelta conservativa, vedi §6) |
| tutte le `LineString` (tratte, cantieri, INFRATEL, scuole, sanità, backbone) | percorsi | no |
| tutti i `Polygon` (`copertura_ok`, `copertura_no`) | aree rilevate | no |

Regola «fuori Comune»: `category` in `OUTSIDE_CATEGORIES` (`scripts/compute_stats.py`), cioè la sola Centrale Feeder. Non si usa `frazione == "Altro"` perché il punto `Coppie di corrugati scoperti` ha `frazione = Altro` pur trovandosi a Stagno (difetto, §5).

Il dato **operatore non esiste** nel KML né nel GeoJSON: nessuna ripartizione per operatore è stata prodotta (`by_operator: null`). Le diciture «FiberCop» / «TIM» presenti nei vecchi documenti non erano ricavabili dai dati.

## 2. Tabelle finali

### Controllo di quadratura

| | Valore |
|---|:---:|
| Punti | 34 |
| Linee | 25 |
| Poligoni | 4 |
| **Totale feature** (34 + 25 + 4) | **63** |
| Km tratte (somma `length_km` per feature) | 21,716 |

### Per tipo

| Tipo | Quantità |
|---|:---:|
| ARL | 23 |
| ARLO | 2 |
| *Totale armadi* | *25* |
| Centrale Comunale | 1 |
| Centrali di frazione | 6 |
| **Totale apparati nel territorio comunale** | **32** |
| Centrale Feeder (Livorno Nord), esterna | 1 |
| **Totale apparati incluso l'esterno** | 33 |
| Punto di infrastruttura (non apparato) | 1 |
| **Totale punti** (33 + 1) | **34** |

### Per frazione (solo territorio comunale)

| Frazione | Apparati | ARL | ARLO | Centrali |
|---|:---:|:---:|:---:|:---:|
| Vicarello | 9 | 8 | 0 | 1 |
| Collesalvetti | 8 | 7 | 0 | 1 |
| Stagno | 8 | 5 | 2 | 1 |
| Guasticce | 4 | 3 | 0 | 1 |
| Nugola | 1 | 0 | 0 | 1 |
| Parrana San Giusto | 1 | 0 | 0 | 1 |
| Parrana San Martino | 1 | 0 | 0 | 1 |
| **Totale** | **32** | **23** | **2** | **7** |

### Dentro / fuori Comune

| | Apparati |
|---|:---:|
| Dentro il Comune | 32 |
| Fuori dal Comune (Centrale Feeder, Livorno Nord) | 1 |

### Per operatore

Non disponibile (il dato non è nel KML).

### Chilometri per frazione

Stagno 8,431 km, Collesalvetti 3,290 km, «Altro / non attribuito» 9,995 km (dorsale INFRATEL BUL, che il convertitore non assegna ad alcuna frazione). Vicarello e Guasticce non hanno tratte nei dati.

### Storico (stessa definizione, conteggio diretto dal KML)

| | Snapshot 1 | Snapshot 2 | Snapshot 3 |
|---|:---:|:---:|:---:|
| Punti | 31 | 31 | 34 |
| Apparati comunali (ARL + ARLO + centrali) | 30 | 30 | 32 |
| di cui ARL / ARLO | 22 / 1 | 22 / 1 | 23 / 2 |

Le voci rinominate sono verificate: `S [0?] ARLO` esiste in Snapshot 1 e 2 ed è assente in Snapshot 3, dove compaiono `S [28] ARLO` (ex `[0?]`, secondo il CHANGELOG) e `S [27] ARLO` (nuovo). Il KML non permette di provare che `S [28]` sia *lo stesso* armadio di `S [0?]` (vedi §6).

## 3. Cause radice (statistiche del sito)

Prima, `js/telemetry.js` (`updateTelemetry`) produceva:

| Valore mostrato | Come veniva prodotto | Causa |
|---|---|---|
| `TOT. APPARATI` = 63 | `features.length` | conteggiava **tutte le feature** (anche 25 linee e 4 poligoni) come apparati |
| `CENTRALI XGS-PON` = 8 | `category.includes('centrale')` | includeva la Centrale Feeder (fuori Comune) e usava un filtro per sottostringa; l'etichetta «XGS-PON» non è nei dati |
| `Distribuzione per Frazione` (24/19/9/4/1/1/1) | `frazCounts[frazione]++` per ogni feature | contava linee e poligoni, non apparati, e mischiava il significato con «elem.» |
| `ARL RAME` 23, `ARLO FIBRA` 2 | filtro per categoria | già corretti |

Il pannello quindi non era sbagliato per ARL/ARLO, ma il totale e le frazioni sì, e **nessun valore era condiviso** con i documenti.

## 4. Prima → dopo di ogni cifra corretta

«Riga» = riga nel file prima della modifica (commit `84ffaff`, `main`).

### Sito

| File:riga | Prima | Dopo | Causa |
|---|---|---|---|
| `js/telemetry.js:12` → `#stat-tot` | 63 | **32** | contava tutte le feature |
| `js/telemetry.js:26` → `#stat-centrali` | 8 | **7** | includeva la Centrale Feeder esterna |
| `js/telemetry.js:30,73` → «per Frazione» | Stagno 24, Collesalvetti 19, Vicarello 9, Guasticce 4, Nugola/Parrana 1+1+1 «elem.» | Vicarello 9, Collesalvetti 8, Stagno 8, Guasticce 4, 1+1+1 «app.» | contava linee e poligoni |
| `index.html:159` | «CENTRALI XGS-PON» | «CENTRALI TLC» | etichetta ingannevole |
| `index.html:170` | «Distribuzione per Frazione» | «Apparati per Frazione» | ora riflette ciò che si conta |

### Documenti

| File:riga | Prima | Dopo | Causa |
|---|---|---|---|
| `README.md:68` | ARLO 21 | **2** | cifra scritta a mano, mai coerente con alcuno snapshot (S1–S3: 1–2 ARLO) |
| `README.md:69` | ARL 8 | **23** | idem (S1–S3: 22–23 ARL) |
| `README.md:70` | Centrali 3 (Collesalvetti, Vicarello, Feeder) | **7** comunali + 1 esterna | omesse 5 centrali di frazione, Feeder sommata al Comune |
| `README.md:71` | «Pozzetti» 2 | rimosso (1 punto `infrastruttura`, non apparato) | categoria `infrastruttura` descritta come pozzetti, con conteggio sbagliato |
| `README.md:77-82` | Stagno 13 ARLO/4 ARL, Collesalvetti 6/3, Vicarello 2/1; totale 21/8/3; km 11,232 / 6,444 / 3,122 / 0,399 / 0,519 | tabella generata dai dati (Stagno 2/5, Collesalvetti 0/7, Vicarello 0/8; totale 2/23/7; km 8,431 / 3,290 / 0 / 0 / «Altro» 9,995) | cifre non riproducibili dai dati; km per frazione non corrispondevano a nessuna aggregazione |
| `README_EN.md:68-71, 77-82` | identiche al README italiano | idem, in inglese | idem |
| `wiki/collesalvetti.md:10` | «34 apparati» | «32 apparati nel territorio comunale (+1 esterno)» | 34 = numero di punti |
| `wiki/collesalvetti.md:37` | Feature Snapshot 1 = 47 | **46** | non coincideva col KML (46 placemark) |
| `wiki/collesalvetti.md:38` | «Elementi Puntuali (Apparati)» 34, «+3 apparati» | «punti censiti» 34, «+3 punti»; nuova riga «di cui apparati» 30 / 30 / 32 | punti ≠ apparati |
| `wiki/collesalvetti.md:39` | Linee Snapshot 1 = 12 | **11** | non coincideva col KML |
| `wiki/collesalvetti.md:41` | 12,070 km (S1) | **12,073 km** | come da `CHANGELOG_DATI.md` e KML |
| `wiki/collesalvetti.md:46-55` | «I 34 elementi…»: ARLO 21, ARL 8, centrali 3, pozzetti 2, totale 34 | blocco generato: ARL 23, ARLO 2, centrali 1+6, totale 32, Feeder 1 esterna, infrastruttura 1 | vedi sopra; la colonna «Operatore» e «4,1 km dal confine» non sono nei dati e sono stati tolti |
| `wiki/collesalvetti.md:61` | «Stagno oltre la metà dell'infrastruttura» | frase neutra | falso: Stagno 38,8% dei km |
| `wiki/collesalvetti.md:63-70` | tabella frazioni (13/4/0…, km) | blocco generato | come README |
| `wiki/articles_data.js` | copia del vecchio markdown | rigenerata da `scripts/sync_docs.py` | bundle offline |
| `docs/HANDOFF_REDESIGN.md:171` | «34 apparati» | «32 apparati comunali (+1 esterno)» | 34 = punti |
| `docs/HANDOFF_REDESIGN.md:68` | `#stat-tot` = «totale apparati/elementi» | «totale apparati comunali» | descrizione ambigua |
| `data/snapshots/CHANGELOG_DATI.md` (Snapshot 3) | nessuna cifra di apparati | riga «Apparati censiti (Snapshot 3): 32 + 1 esterno» | mancava |
| `dossier_audit_e_sopralluoghi_collesalvetti.md:8` | tabella senza riferimento allo snapshot | nota: la tabella è di Snapshot 1 | cifra storica, lasciata invariata ma etichettata |

Lasciati invariati perché già corretti: 63 feature, 34 punti / 25 linee / 4 poligoni, 21,716 km, conteggi di Snapshot 1–3 del `CHANGELOG_DATI.md` (verificati dal test contro i KML).

## 5. Difetti dei dati (non corretti, da segnalare)

1. `Coppie di corrugati scoperti` ha `frazione = Altro` ma le coordinate (43,5913 N; 10,3500 E) cadono a Stagno. Non è stato toccato.
2. Le centrali di frazione hanno il nome `Centrale di Frazione` identico nel KML (6 volte): nome e frazione sono **attribuiti dal convertitore** con riquadri geografici fissi (`kml_to_geojson.py`, righe ~245-264). L'ultimo ramo è `lat < 43,532 ⇒ Parrana San Giusto`: qualunque punto più a sud finirebbe lì. Il test verifica il totale delle centrali ma non la frazione assegnata.
3. `G [0?] ARL` ha il numero «da verificare» nel KML: contato come ARL, ma identità incerta.
4. I km per frazione dipendono dall'euristica `categorize()` (le tratte INFRATEL, 9,995 km, non hanno frazione; Vicarello e Guasticce risultano a 0 km).
5. Il confine comunale non è nei dati: l'unico apparato dichiarato fuori Comune è la Centrale Feeder, in base al nome («Livorno Nord», impostato dal convertitore). Gli altri punti non sono stati verificati geometricamente contro il confine.
6. Il CHANGELOG indica 13,503 km per Snapshot 2, mentre il ricalcolo dal KML dà 13,504; non toccato (fuori dal perimetro apparati).
7. Il pannello «CANTIERI ATTIVI» conta le feature con `category` che contiene `cantiere` (14, incluse le tratte «non eseguite»). Non riguarda gli apparati e non è stato modificato.
8. Nessun duplicato di placemark o di nome nei punti (controllato su id e nome).

## 6. Domande aperte

1. **Corrugati scoperti**: va considerato un apparato? Interpretazione conservativa adottata: **no** (32 comunali). Se sì: 33 comunali, 34 incluso il Feeder.
2. **Centrale Feeder**: va considerata un apparato «della rete comunale»? Adottato: apparato, ma esterno e fuori dal totale (32 + 1).
3. **`S [28] ARLO`** è davvero l'ex `S [0?] ARLO`? Il KML non lo prova; ci si fida del CHANGELOG. Il conteggio non cambia in nessun caso: 2 ARLO in Snapshot 3.
4. **`G [0?] ARL`** e armadi «NUMERO da verificare»: contati come ARL esistenti (nessuna esclusione per «da verificare»).
5. Si vuole aggiungere nel KML un campo operatore? Senza quello, nessuna ripartizione per operatore è onesta.
6. Vuoi l'attribuzione geografica delle centrali di frazione spostata dal convertitore a dati (es. nome nel KML)?

## 7. Comandi

```bash
git checkout fix/equipment-recount
python3 scripts/kml_to_geojson.py      # network_data.json, js/data.js e (via compute_stats) stats.json, js/stats.js
python3 scripts/export_sheets.py       # CSV e XLSX
python3 scripts/sync_docs.py           # blocchi AUTO-STATS dei Markdown + wiki/articles_data.js
python3 -m unittest tests.test_stats -v
python3 scripts/sync_docs.py --check   # facoltativo: solo verifica
python3 start_server.py                # poi aprire http://localhost:8080 e confrontare il pannello con data/stats.json
```

`scripts/compute_stats.py` si può lanciare da solo (`python3 scripts/compute_stats.py`) e legge solo `data/network_data.json`.

Nota: `data/rete_ftth_collesalvetti.xlsx` contiene timestamp di creazione dello zip, quindi cambia byte a ogni rigenerazione anche a dati invariati; CSV e JSON sono deterministici.
