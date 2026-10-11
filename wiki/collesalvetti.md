---
title: "La Rete FTTH nel Comune di Collesalvetti"
summary: "Analisi tecnica e geospaziale della rete in fibra ottica nel Comune di Collesalvetti (LI): dati quantitativi certificati da Snapshot 4 (68 feature, 21,78 km), distribuzione per frazione, censimento apparati e registro delle ordinanze comunali aggiornato all'11 ottobre 2026."
updated: "2026-10-11"
sources:
  - id: "snapshot4-kml"
    title: "Rilievo Geospaziale Indipendente: Snapshot 4 (11/10/2026)"
    url: "data/snapshots/rilievo_snapshot4.kml"
    type: "dati"
    note: "Rilievo GIS di campo: 68 feature, 21,778 km di tracciato, 35 apparati nel territorio comunale (+1 esterno), 4 poligoni"
  - id: "ordinanze-collesalvetti"
    title: "Albo Pretorio del Comune di Collesalvetti: Ordinanze di Polizia Municipale n. 75, 95, 102/104 e 105/2026"
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

Questa pagina offre un quadro oggettivo, verificabile e documentato dello stato della rete in fibra ottica FTTH, elaborato a partire dai dati geospaziali dello **Snapshot 4 (rilievo dell'11/10/2026)** e dagli atti ufficiali pubblicati all'Albo Pretorio municipale.

---

## 1. Quadro Quantitativo Generale (Snapshot 4 - 11/10/2026)

Rispetto ai precedenti rilievi, lo **Snapshot 4** registra l'installazione del primo cabinet ottico nel capoluogo, il censimento del terzo ARLO di Stagno e la formalizzazione del Cantiere 3:

| Parametro Rilevato | Snapshot 2 (Settembre 2026) | Snapshot 3 (04/10/2026) | **Snapshot 4 Corrente (11/10/2026)** | Variazione S3 $\rightarrow$ S4 |
|---|:---:|:---:|:---:|:---:|
| **Totale Feature Geospaziali** | 49 | 63 | **68** | +5 feature (+7,9%) |
| **Elementi Puntuali (punti censiti)** | 31 | 34 | **37** | +3 punti (+8,8%) |
| **di cui Apparati (armadi e centrali, comune)** | 30 | 32 | **35** | +3 apparati (+9,4%) |
| **Elementi Lineari (Tratte e Scavi)** | 14 | 25 | **27** | +2 tratte (+8,0%) |
| **Elementi Areali (Poligoni)** | 4 | 4 | **4** | Invariati (perimetri rilievo) |
| **Chilometri Totali Tracciati** | 13,503 km | 21,716 km | **21,778 km** | **+0,064 km netti** |
| **Tasso Avanzamento Comunale** | 48,2% | 52,4% | **62,8%** | **+10,4%** |

---

## 2. Censimento Apparati sul Territorio

<!-- AUTO-STATS:BEGIN equipment -->
Apparato = punto di rete censito (armadio ARL/ARLO o centrale). Linee, poligoni e punti di infrastruttura non sono apparati. Dei 37 punti dello Snapshot, 36 sono apparati (35 nel territorio comunale + 1 esterno al Comune) e 1 è un punto di infrastruttura non conteggiato.

| Tipologia | Categoria GIS | Quantità | Note |
|---|---|:---:|---|
| **Armadio Ripartilinea (ARL, rame)** | `arl` | **24** | |
| **Armadio Ripartilinea Ottico (ARLO)** | `arlo` | **4** | |
| *Totale armadi (ARL + ARLO)* | | *28* | |
| **Centrale Comunale** | `centrale_comunale` | **1** | |
| **Centrali di Frazione** | `centrale_frazione` | **6** | |
| **Totale apparati sul territorio comunale** | | **35** | |
| Apparati esterni al Comune (non inclusi nel totale): Centrale Feeder (Livorno Nord) | `centrale_feeder` | 1 | fuori dal territorio comunale |
| Punti non-apparato (esclusi dal conteggio): Coppie di corrugati scoperti | `infrastruttura` | 1 | punto di infrastruttura, non apparato |
<!-- AUTO-STATS:END equipment -->

---

## 3. Ripartizione Geografica per Frazione

La suddivisione chilometrica e infrastrutturale evidenzia l'avanzamento su **Stagno** e **Collesalvetti capoluogo**:

<!-- AUTO-STATS:BEGIN frazioni -->
| Frazione | Apparati | ARLO | ARL | Centrali | Tratte (km) | Quota % km |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Stagno** | 10 | 3 | 6 | 1 | 8,483 km | 39,0% |
| **Collesalvetti** | 9 | 1 | 7 | 1 | 3,300 km | 15,2% |
| **Vicarello** | 9 | 0 | 8 | 1 | 0,000 km | 0,0% |
| **Guasticce** | 4 | 0 | 3 | 1 | 0,000 km | 0,0% |
| **Nugola** | 1 | 0 | 0 | 1 | 0,000 km | 0,0% |
| **Parrana San Martino** | 1 | 0 | 0 | 1 | 0,000 km | 0,0% |
| **Parrana San Giusto** | 1 | 0 | 0 | 1 | 0,000 km | 0,0% |
| **Altro / non attribuito** | 0 | 0 | 0 | 0 | 9,995 km | 45,9% |
| **Totale** | 35 | 4 | 24 | 7 | 21,778 km | 100,0% |

*Gli apparati sono contati per frazione dal solo territorio comunale; i km delle tratte comprendono anche la dorsale INFRATEL BUL e le tratte senza frazione (`Altro`).*
<!-- AUTO-STATS:END frazioni -->

Tratte e cantieri principali per frazione:

- **Stagno:** Cantiere 2 in completamento (Ord. 95/104), Cantiere 3 Via Aiaccia autorizzato (Ord. 105), Ripristini Via Marx conclusi.
- **Collesalvetti (Centro):** Cantiere 1 (Ord. 88/95), 1° ARLO posato (`C [] ARLO`), hub rotatoria completato, Via Nenni in attesa proroga.
- **Vicarello:** Dorsale urbana e centrale di commutazione locale.
- **Guasticce:** Tratta dorsale primaria di collegamento.
- **Altro / non attribuito:** Dorsale INFRATEL BUL, opera sulla Backbone; la Centrale Feeder esterna (Comune di Livorno) è riportata a parte e non è inclusa negli apparati comunali.

---

## 4. Registro dei Cantieri e delle Ordinanze di Polizia Municipale

L'incrocio tra gli atti formali pubblicati sull'Albo Pretorio e i riscontri dei sopralluoghi sul terreno permette di documentare lo stato reale dei lavori, separando i termini dell'ordinanza dagli scostamenti effettivi.

```
NOTE METODOLOGICHE SULLA NUMERAZIONE DEGLI ATTI:
Nel Comune di Collesalvetti ciascuna ordinanza riceve due identificativi distinti:
1. Numero interno di settore della Polizia Municipale (es. P.M. n. 88, n. 95 o n. 105)
2. Numero di Registro Generale del Comune (es. Reg. Gen. 95, 102/104 o 105)
Per garantire la massima trasparenza, questo osservatorio cita sempre entrambi i numeri.
```

### Ordinanze Ufficiali Identificate

#### 1. Cantiere 2 - Stagno (Nuova Espansione FTTH)
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 95/2026 (**Registro Generale n. 102/104/2026**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 17/2026 del 16/07/2026
- **Periodo da Ordinanza:** Dal **21/09/2026** al **17/10/2026** (fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Romita sud, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio, Via Don Verità, Via 8 Marzo
- **Lunghezza Tratta:** 1,48 km stimati
- **Stato Lavori (Rilievo 11/10/2026):** **In completamento.** Posa delle condotte completata; 6 pozzetti di smistamento in fase di getto/chiusura finale lungo l'asse Via Romita / Via XXV Aprile. Tratta completata convalidata (`Cantiere 2 ESEGUITO`, 292,9 m).
- **Nuovo ARLO:** Confermato l'ARLO posato in affiancamento a `S [04] ARL` (`[10.353902, 43.589311]`, senza etichetta numerica, 3° ARLO censito a Stagno oltre a `S [27]` e `S [28]`).
- **File Documentale:** [`ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf`](file:///c:/Users/blankdisk/Documents/GitHub/fiberpulse/ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf)

#### 2. Cantiere 3 - Stagno (Via Aiaccia / Via Umbria)
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 105/2026 (**Registro Generale n. 105**) + **Concessione Suolo n. 77/2026**
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Occupazione Suolo:** Concessione per 60 mq di suolo pubblico
- **Periodo Autorizzato:** Dal **19/10/2026** al **23/10/2026** (5 giorni feriali, 08:00 – 18:00)
- **Vie Coinvolte:** Via Aiaccia e Via Umbria
- **Lunghezza Tratta:** 3,48 km complessivi
- **Stato Lavori:** **Autorizzato / Avvio programmato.**
- **Nota Cartografica:** L'innesto sud di Via Aiaccia verso la direttrice provinciale costituisce il punto di raccordo con la tratta dorsale SP555 autorizzata a luglio 2026.

#### 3. Cantiere 1 - Collesalvetti Centro
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 88 del 02/09/2026 (**Registro Generale n. 95**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Periodo da Ordinanza:** Dal **14/09/2026** al **02/10/2026** (fascia feriale 08:00 – 18:00)
- **Stato Giuridico:** **Termini scaduti il 02/10/2026.**
- **Rilievo di Campo (Snapshot 4 al 11/10/2026):**
  - **Tratte eseguite (Sud-Est):** Via del Valico a Pisa, Via Peppino Impastato, Via di Cerretello e anello di raccordo rotatoria (`Cantiere 1 AGGIUNTO`, 71,8 m) completate con minitrincea sigillata (microtubi *Fender 4x10/14*), posa di 4 pozzetti FiberCop e montaggio del **primo ARLO cittadino** (`C [] ARLO`, futuro ARLO 01) alla rotatoria Via Roma / Via Nenni / Via Ciampi.
  - **Tratte non eseguite (Nord-Ovest / Via Nenni):** 5 tratte con sole marcature spray blu a terra. In attesa di nuova ordinanza viaria / proroga per il comparto Via Nenni.
- **File Documentale:** [`ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf`](file:///c:/Users/blankdisk/Documents/GitHub/fiberpulse/ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf)

#### 4. Lavori di Ripristino Manto Stradale - Stagno
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 70 del 16/07/2026 (**Registro Generale n. 75**)
- **Vie Coinvolte:** Via Marx, Via Guerrazzi, Via La Malfa
- **Lunghezza Tratta:** 0,85 km
- **Stato Lavori:** **Conclusi formalmente e sul campo.**
- **File Documentale:** [`ordinanze/ordinanza_75_2026_stagno_ripristino.pdf`](file:///c:/Users/blankdisk/Documents/GitHub/fiberpulse/ordinanze/ordinanza_75_2026_stagno_ripristino.pdf)

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
