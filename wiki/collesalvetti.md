---
title: "La Rete FTTH nel Comune di Collesalvetti"
summary: "Analisi tecnica e geospaziale della rete in fibra ottica nel Comune di Collesalvetti (LI): dati quantitativi certificati da Snapshot 4 (68 feature, 21,78 km), distribuzione per frazione, censimento apparati e registro delle ordinanze comunali aggiornato all'11 ottobre 2026."
updated: "2026-10-11"
sources:
  - id: "snapshot4-kml"
    title: "Rilievo Geospaziale Indipendente: Snapshot 4 (11/10/2026)"
    url: "data/snapshots/rilievo_snapshot4.kml"
    type: "dati"
    note: "Rilievo GIS di campo: 68 feature, 21,780 km di tracciato, 37 apparati, 4 poligoni"
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
| **Elementi Puntuali (Apparati)** | 31 | 34 | **37** | +3 apparati (+8,8%) |
| **Elementi Lineari (Tratte e Scavi)** | 14 | 25 | **27** | +2 tratte (+8,0%) |
| **Elementi Areali (Poligoni)** | 4 | 4 | **4** | Invariati (perimetri rilievo) |
| **Chilometri Totali Tracciati** | 13,503 km | 21,716 km | **21,780 km** | **+0,064 km netti** |
| **Tasso Avanzamento Comunale** | 48,2% | 52,4% | **62,8%** | **+10,4%** |

---

## 2. Censimento Apparati sul Territorio

I 37 elementi puntuali censiti sul suolo comunale e di confine comprendono:

| Tipologia Apparato | Categoria GIS | Quantità Rilevata | Operatore / Rete | Note di Rilievo |
|---|---|:---:|---|---|
| **Armadio Ripartilinea Ottico** | `arlo` | **4** | FiberCop / Wholesale | 1 nel capoluogo (`C [] ARLO`, rotatoria Via Roma/Via Nenni) + 3 a Stagno (`S [27]`, `S [28]`, `S []` su Via Romita) |
| **Armadio Ripartilinea Rame** | `arl` | **24** | TIM (Rete Storica) | 7 a Collesalvetti, 8 a Vicarello, 6 a Stagno, 3 a Guasticce |
| **Centrale di Commutazione** | `centrale` | **8** | Rete Fissa Primaria | 1 comunale (Collesalvetti), 6 di frazione (Vicarello, Stagno, Guasticce, Nugola, Parrana S.M., Parrana S.G.) + 1 Feeder (Livorno) |
| **Pozzetto di Derivazione** | `infrastruttura` | **1** | Rete Sotterranea | Corrugati scoperti e camerette di derivazione dorsale |
| **Totale Apparati** | | **37** | | |

---

## 3. Ripartizione Geografica per Frazione

La suddivisione chilometrica e infrastrutturale evidenzia l'avanzamento su **Stagno** e **Collesalvetti capoluogo**:

| Frazione | Lunghezza Tratte (km) | Quota % Chilometrica | ARLO Fibra | ARL Rame | Centrali TLC | Avanzamento Stimato | Tratte e Cantieri Principali |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Stagno** | **11,525 km** | 52,9% | 3 | 6 | 1 | **86,4%** | Cantiere 2 in completamento, Cantiere 3 autorizzato (Ord. 105), Ripristini conclusi |
| **Collesalvetti (Centro)** | **6,516 km** | 29,9% | 1 | 7 | 1 | **41,5%** | Cantiere 1 (Ord. 95), 1° ARLO posato, hub rotatoria completato, Via Nenni in attesa proroga |
| **Vicarello** | **3,122 km** | 14,3% | 0 | 8 | 1 | **35,0%** | Dorsale urbana e centrale di commutazione locale |
| **Guasticce** | **0,399 km** | 1,8% | 0 | 3 | 1 | **20,0%** | Tratta dorsale primaria di collegamento |
| **Altro / Intercomunale** | **0,519 km** | 2,4% | 0 | 0 | 1 | - | Opera sulla Backbone e Centrale Feeder esterna (Comune di Livorno) |
| **Totale Territoriale** | **21,780 km** | **100,0%** | **4** | **24** | **8** | **62,8%** | |

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
