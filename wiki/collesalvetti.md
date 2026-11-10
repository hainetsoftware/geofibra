---
title: "La Rete FTTH nel Comune di Collesalvetti"
summary: "Analisi tecnica e geospaziale della rete in fibra ottica nel Comune di Collesalvetti (LI): dati quantitativi certificati da Snapshot 6 (73 feature, 23,785 km), distribuzione per frazione, censimento apparati e registro delle ordinanze comunali con riscontri di campo al 5 novembre 2026."
updated: "2026-11-05"
sources:
  - id: "snapshot6-kml"
    title: "Rilievo Geospaziale Indipendente: Snapshot 6 (05/11/2026)"
    url: "data/kml_snapshots/FTTH%20Collesalvetti_snapshot6.kml"
    type: "dati"
    note: "Rilievo GIS di campo: 73 feature, 23,785 km di tracciato, 36 apparati nel territorio comunale (+1 esterno), 4 poligoni"
  - id: "ordinanze-collesalvetti"
    title: "Albo Pretorio del Comune di Collesalvetti: Ordinanze di Polizia Municipale n. 75, 95, 102/104, 105, 110, 111 e 112/2026"
    url: "data/ordinanze.json"
    type: "ufficiale"
    note: "Atti autorizzativi di disciplina della circolazione, occupazione suolo e scavo stradale per fibra ottica"
  - id: "sinfi-mimit"
    title: "Catasto Nazionale SINFI / MIMIT: Rete di Accesso Provincia di Livorno"
    url: "https://www.sinfi.it"
    type: "ufficiale"
    note: "Inquadramento infrastrutturale e dorsali interurbane"
---

# La Rete FTTH nel Comune di Collesalvetti

Il territorio del Comune di Collesalvetti (provincia di Livorno) si estende per circa **109 chilometri quadrati** con una tipica conformazione toscana policentrica, composta dal capoluogo e da sei frazioni principali collocate tra la piana alluvionale verso Livorno e Pisa e le colline livornesi.

Questa pagina offre un quadro oggettivo, verificabile e documentato dello stato della rete in fibra ottica FTTH, elaborato a partire dai dati geospaziali dello **Snapshot 6 (rilievo del 05/11/2026)** e dagli atti ufficiali pubblicati all'Albo Pretorio municipale.

---

## 1. Quadro Quantitativo Generale (Snapshot 6 - 05/11/2026)

Lo **Snapshot 6** registra il quarto ARLO di Stagno, il completamento del Cantiere 2 e dell’anello nord del Cantiere 4. A Collesalvetti documenta la progettazione esecutiva del Cantiere 1 e il deposito di corrugati presso le Scuole Medie.

| Parametro Rilevato | Snapshot 3 (04/10/2026) | Snapshot 4 (11/10/2026) | **Snapshot 6 (05/11/2026)** | Variazione rispetto a Snapshot 5 |
|---|:---:|:---:|:---:|:---:|
| **Totale Feature Geospaziali** | 63 | 68 | **73** | +2 |
| **Elementi Puntuali (punti censiti)** | 34 | 37 | **39** | +2 |
| **di cui Apparati (armadi e centrali, comune)** | 32 | 35 | **36** | +1 |
| **Elementi Lineari (Tratte e Scavi)** | 25 | 27 | **30** | 0 |
| **Elementi Areali (Poligoni)** | 4 | 4 | **4** | 0 |
| **Chilometri Totali Tracciati** | 21,716 km | 21,778 km | **23,785 km** | −0,055 km |

---

## 2. Censimento Apparati sul Territorio

<!-- AUTO-STATS:BEGIN equipment -->
Apparato = punto di rete censito (armadio ARL/ARLO o centrale). Linee, poligoni e punti di infrastruttura non sono apparati. Dei 39 punti dello Snapshot, 37 sono apparati (36 nel territorio comunale + 1 esterno al Comune) e i restanti (2) sono esclusi dal conteggio.

| Tipologia | Categoria GIS | Quantità | Note |
|---|---|:---:|---|
| **Armadio Ripartilinea (ARL, rame)** | `arl` | **24** | |
| **Armadio Ripartilinea Ottico (ARLO)** | `arlo` | **5** | |
| *Totale armadi (ARL + ARLO)* | | *29* | |
| **Centrale Comunale** | `centrale_comunale` | **1** | |
| **Centrali di Frazione** | `centrale_frazione` | **6** | |
| **Totale apparati sul territorio comunale** | | **36** | |
| Apparati esterni al Comune (non inclusi nel totale): Centrale Feeder (Livorno Nord) | `centrale_feeder` | 1 | fuori dal territorio comunale |
| Punti non-apparato (esclusi dal conteggio): Coppie di corrugati scoperti | `infrastruttura` | 1 | punto di infrastruttura, non apparato |
| Punti non-apparato (esclusi dal conteggio): Coppie di fibre | `materials_depot` | 1 | punto di infrastruttura, non apparato |
<!-- AUTO-STATS:END equipment -->

---

## 3. Ripartizione Geografica per Frazione

La suddivisione chilometrica e infrastrutturale evidenzia l'avanzamento su **Stagno** e **Collesalvetti capoluogo**:

<!-- AUTO-STATS:BEGIN frazioni -->
| Frazione | Apparati | ARLO | ARL | Centrali | Tratte (km) | Quota % km |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Stagno** | 11 | 4 | 6 | 1 | 10,535 km | 44,3% |
| **Collesalvetti** | 9 | 1 | 7 | 1 | 3,255 km | 13,7% |
| **Vicarello** | 9 | 0 | 8 | 1 | 0,000 km | 0,0% |
| **Guasticce** | 4 | 0 | 3 | 1 | 0,000 km | 0,0% |
| **Nugola** | 1 | 0 | 0 | 1 | 0,000 km | 0,0% |
| **Parrana San Martino** | 1 | 0 | 0 | 1 | 0,000 km | 0,0% |
| **Parrana San Giusto** | 1 | 0 | 0 | 1 | 0,000 km | 0,0% |
| **Altro / non attribuito** | 0 | 0 | 0 | 0 | 9,995 km | 42,0% |
| **Totale** | 36 | 5 | 24 | 7 | 23,785 km | 100,0% |

*Gli apparati sono contati per frazione dal solo territorio comunale; i km delle tratte comprendono anche la dorsale INFRATEL BUL e le tratte senza frazione (`Altro`).*
<!-- AUTO-STATS:END frazioni -->

Tratte e cantieri principali per frazione:

- **Stagno:** Cantiere 2 completato, anello nord del Cantiere 4 completato e ramo sud ancora pianificato. Quattro ARLO censiti.
- **Collesalvetti (Centro):** Cantiere 1 (Ord. 88/95), primo ARLO posato, hub rotatoria completato e soffiaggio della fibra osservato sull’anello primario.
- **Vicarello:** Dorsale urbana e centrale di commutazione locale.
- **Guasticce:** Tratta dorsale primaria di collegamento.
- **Altro / non attribuito:** Dorsale INFRATEL BUL, opera sulla Backbone; la Centrale Feeder esterna (Comune di Livorno) è riportata a parte e non è inclusa negli apparati comunali.

---

## 4. Registro dei Cantieri e delle Ordinanze di Polizia Municipale

L'incrocio tra gli atti formali pubblicati sull'Albo Pretorio e i riscontri dei sopralluoghi sul terreno permette di documentare lo stato reale dei lavori, separando i termini dell'ordinanza dagli scostamenti effettivi.

```
NOTE METODOLOGICHE SULLA NUMERAZIONE DEGLI ATTI:
Nel Comune di Collesalvetti ciascuna ordinanza riceve due identificativi distinti:
1. Numero interno di settore della Polizia Municipale (es. P.M. n. 88, n. 95, n. 105, n. 110, n. 111 o n. 112)
2. Numero di Registro Generale del Comune (es. Reg. Gen. 95, 102/104, 105, 110, 111 o 112)
Per garantire la massima trasparenza, questo osservatorio cita sempre entrambi i numeri.
```

### Ordinanze Ufficiali Identificate

#### 1. Cantiere 2 - Stagno (Nuova Espansione FTTH) & Proroga
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 95/2026 (**Registro Generale n. 102/104/2026**) + **Ordinanza PM n. 111 del 16/10/2026 (Proroga)**
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 17/2026 del 16/07/2026
- **Periodo da Ordinanza:** Dal **21/09/2026** al **23/10/2026** (prorogato di 5 giorni lavorativi con Ord. 111 per completamento minitrincee secondarie e chiusura pozzetti attorno all'ARLO, fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Romita sud, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio, Via Don Verità, Via 8 Marzo
- **Lunghezza Tratta:** 1,48 km stimati
- **Stato lavori (rilievo 05/11/2026)**. Opere civili completate su tutte le quattro tratte censite.
- **Armadi ottici**. Il quarto ARLO è stato installato accanto a `S [07] ARL` e attende verifica del numero. Si aggiunge a `S [27]`, `S [28]` e all’armadio senza etichetta accanto a `S [04] ARL`.
- **File Documentale:** [`data/ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf`](data/ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf)

#### 2. Cantiere 3 - Stagno (Via Aiaccia / Via Umbria)
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 105/2026 (**Registro Generale n. 105**) + **Concessione Suolo n. 77/2026**
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Occupazione Suolo:** Concessione per 60 mq di suolo pubblico
- **Periodo Autorizzato:** Dal **19/10/2026** al **23/10/2026** (5 giorni feriali, 08:00 – 18:00)
- **Vie Coinvolte:** Via Aiaccia e Via Umbria
- **Lunghezza Tratta:** 3,48 km complessivi
- **Stato Lavori:** **Autorizzato / Avvio programmato.**
- **Nota Cartografica:** L'innesto sud di Via Aiaccia verso la direttrice provinciale costituisce il punto di raccordo con la tratta dorsale SP555 autorizzata a luglio 2026.

#### 3. Cantiere 4 - Stagno (Nuova Espansione Sud/Ovest)
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 110/2026 (**Registro Generale n. 110**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 26/2026
- **Periodo Autorizzato:** Dal **26/10/2026** al **20/11/2026** (fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Marx, Via Curiel (lato sud), Via Gobetti, Via Don Verità, Via F.lli Cervi, Via La Malfa, Via Verga, Via Berlinguer
- **Lunghezza Tratta:** 2,052 km (quattro tratte censite)
- **Stato lavori**. Anello nord completato (734 m) tra Via Karl Marx, Via Gobetti e Via Curiel. Restano pianificate tre tratte, tra cui il ramo di Via Don Giovanni Verità (446 m).

#### 4. Ripristino Definitivo Manto Stradale - Via Fratelli Rosselli (Stagno)
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 112 del 16/10/2026 (**Registro Generale n. 112**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 10/2026
- **Periodo Autorizzato:** Dal **19/10/2026** al **24/11/2026** (fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Fratelli Rosselli
- **Oggetto:** Fresatura e ripristino del tappeto d'usura definitivo sulle trincee FTTH realizzate a maggio-giugno 2026
- **Stato Lavori:** **In avvio lunedì 19/10.**

#### 5. Cantiere 1 - Collesalvetti Centro
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 88 del 02/09/2026 (**Registro Generale n. 95**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Periodo da Ordinanza:** Dal **14/09/2026** al **02/10/2026** (fascia feriale 08:00 – 18:00)
- **Stato Giuridico:** **Termini scaduti il 02/10/2026.**
- **Rilievo di Campo (Snapshot 6 al 05/11/2026):**
  - **Tratte eseguite (Sud-Est):** Via del Valico a Pisa, Via Peppino Impastato, Via di Cerretello e anello di raccordo rotatoria (`Cantiere 1 AGGIUNTO`, 71,8 m) completate con minitrincea sigillata (microtubi *Fender 4x10/14*), posa di 4 pozzetti FiberCop e montaggio del **primo ARLO cittadino** (`C [] ARLO`, futuro ARLO 01) alla rotatoria Via Roma / Via Nenni / Via Ciampi.
  - **Progettazione esecutiva**. Marcature e tecnici osservati su una tratta, soffiaggio della fibra nei pozzetti sull’altra. Su due ulteriori tratte è probabile il riuso di pozzetti e cavidotti SIP/Telecom.
- **File Documentale:** [`data/ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf`](data/ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf)

#### 6. Lavori di Ripristino Manto Stradale (Conclusi) - Stagno
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 70 del 16/07/2026 (**Registro Generale n. 75**)
- **Vie Coinvolte:** Via Marx, Via Guerrazzi, Via La Malfa
- **Lunghezza Tratta:** 0,85 km
- **Stato Lavori:** **Conclusi formalmente e sul campo.**
- **File Documentale:** [`data/ordinanze/ordinanza_75_2026_stagno_ripristino.pdf`](data/ordinanze/ordinanza_75_2026_stagno_ripristino.pdf)

---

## 5. Tratte Rilevate "Da Collegare a Ordinanza"

In conformità ai principi di trasparenza del progetto civico, rimane una sola tratta geospaziale non associata a ordinanza di viabilità comunale:

1. **Opera sulla Backbone (Luglio 2026):**
   - Tratta lineare di **0,519 km** (519 metri) situata ad ovest del confine comunale.
   - Dorsale di interconnessione interurbana verso Livorno lungo la viabilità extraurbana (SP555).

---

## 6. Dichiarazione d'Indipendenza e Metodologia Civica

Questo osservatorio è un'iniziativa informativa indipendente senza scopo di lucro, gestita da cittadini ed esperti di telecomunicazioni. Non è sponsorizzato né affiliato con il Comune di Collesalvetti, con la Polizia Municipale, né con le società FiberCop, Telecom Italia, Fastweb o Open Fiber.

Tutti i dati cartografici e le tabelle vengono rilasciati con licenza aperta per consentire a cittadini, comitati di quartiere e amministratori di verificare lo stato reale dei servizi di connettività sul territorio comunale.
