# Archivio Atti & Ordinanze

Geo Fibra serve i file statici dalla root del repository, sia in locale sia su GitHub Pages. Il tracker in `data/ordinanze.json` riunisce finestre autorizzate e rilievi di cantiere. L’archivio in `data/ordinanze/ordinanze.json` cataloga i documenti e collega gli atti alle geometrie del rilievo.

## Layout e distribuzione

| Percorso | Contenuto |
| --- | --- |
| `ordinanze/` o `data/ordinanze/inbox/` | Download originali locali, esclusi da Git |
| `data/ordinanze/pdf/` | Copie byte per byte dei PDF pubblicati |
| `data/ordinanze/ordinanze.json` | Indice generato con metadati, validità, riferimenti e ID geografici |
| `data/ordinanze/overrides.json` | Correzioni verificate e metadati manuali per scansioni o allegati |
| `data/ordinanze/testo.json` | Testo estratto, richiesto alla prima ricerca |
| `data/ordinanze/offline.js` | Fallback caricato su richiesta quando si apre il sito da file o il JSON non è disponibile |
| `public/data/ordinanze.json` | Copia dell’indice per un eventuale build con Vite |

Il sito attuale legge direttamente `data/ordinanze/`. In una futura migrazione Vite si può copiare la stessa cartella nella distribuzione, conservando i percorsi relativi `data/ordinanze/…`. I PDF vengono richiesti quando si apre l’anteprima o il documento. Il catalogo si carica alla prima apertura del drawer o di un popup collegabile.

I nuovi PDF seguono il formato `YYYY-MM-DD_ENTE_TIPO_NUMERO_RICHIEDENTE_AREA.pdf`, ad esempio `2026-10-01_COLLE_ORD_105_Fastweb_Stagno.pdf`. I campi mancanti usano `UNDATED`, `Nd` o un identificatore derivato dall’hash. I PDF pubblicati con un nome precedente conservano il percorso. La soglia di 2 MiB per PDF tiene le planimetrie e i fascicoli più pesanti nell’inbox. Per pubblicarli in futuro, usare uno storage statico con URL versionati e aggiungere un riferimento esplicito nell’indice. La pubblicazione corrente usa file PDF ordinari in Git, compatibili con il server statico.

## Importazione e verifica

1. Salvare i PDF originali nell’inbox. Usare una cartella per ente e indicare l’ente di provenienza, soprattutto per scansioni e documenti privi di intestazione leggibile.
2. Installare Poppler (`pdftotext`) e lanciare `python3 scripts/parse_ordinanze.py --import-dir ordinanze --ente COMUNE_COLLESALVETTI`. Per rigenerare dai soli PDF pubblicati, omettere `--import-dir`. L’estrazione conserva la disposizione delle colonne e delle clausole. Lo script deduplica per SHA-256 e conserva la prima copia pubblicata per un atto con numerazione identificabile.
3. Controllare l’indice rispetto ai PDF. Per correggere date, strade, richiedenti, cluster o riferimenti, usare l’ID in `overrides.json`. Un documento senza testo sufficiente mantiene `ocr_required: true` e si può cercare tramite i metadati manuali. Il testo OCR va verificato prima di pubblicare una copia ricercabile.
4. Aggiornare GeoJSON e archivio nell’ordine seguente quando si promuove un rilievo. La conversione KML legge l’indice per i PDF del tracker. La seconda generazione ricalcola i link sui Placemark ID del nuovo rilievo.

   ```sh
   python3 scripts/kml_to_geojson.py
   python3 scripts/parse_ordinanze.py
   python3 scripts/export_sheets.py
   python3 scripts/sync_docs.py
   python3 scripts/sync_docs.py --check
   python3 -m unittest discover -v
   npm ci
   npm run build
   ```

Il build verifica il contratto TypeScript del componente JavaScript, la sintassi della mappa e la corrispondenza degli indici con i PDF pubblicati. Il sito continua a essere servito direttamente dalla root. La pipeline conserva la data di emissione, il protocollo e il Registro Generale separati dalla finestra di validità. Alcuni atti storici richiedono correzioni manuali a causa di impaginazioni o grafie irregolari.

## Collegamenti e stati

- Un riferimento esplicito al numero P.M. nel rilievo o un Placemark ID verificato in `overrides.json` genera un collegamento diretto. Le geometrie compatibili comprendono le tratte e i punti ARLO.
- Una strada in comune nella stessa frazione genera una corrispondenza per strada, mostrata con un’etichetta distinta. I nomi stradali provengono dai PDF e dagli attributi del rilievo.
- Le autorizzazioni tecniche esplicite alimentano i gruppi per ente, frazione e numero. I riferimenti ad altri atti sono navigabili in entrambe le direzioni quando il documento è presente in archivio.
- Il badge di validità usa le date civili di Roma. Il completamento dell’opera richiede un’osservazione separata e può essere aggiunto come metadato verificato.
