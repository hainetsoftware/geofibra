---
title: "La Rete FTTH nel Comune di Collesalvetti"
summary: "Analisi tecnica e geospaziale della rete in fibra ottica nel Comune di Collesalvetti (LI): dati quantitativi certificati da Snapshot 3 (63 feature, 21,72 km), distribuzione per frazione, censimento apparati e registro delle ordinanze comunali."
updated: "2026-10-04"
sources:
  - id: "snapshot3-kml"
    title: "Rilievo Geospaziale Indipendente: Snapshot 3 (04/10/2026)"
    url: "data/snapshots/rilievo_snapshot3.kml"
    type: "dati"
    note: "Rilievo GIS di campo: 63 feature, 21,716 km di tracciato, 34 apparati, 4 poligoni"
  - id: "ordinanze-collesalvetti"
    title: "Albo Pretorio del Comune di Collesalvetti: Ordinanze di Polizia Municipale n. 75, 95 e 102/2026"
    url: "data/ordinanze.json"
    type: "ufficiale"
    note: "Atti autorizzativi di disciplina della circolazione e scavo stradale per fibra ottica"
  - id: "sinfi-mimit"
    title: "Catasto Nazionale SINFI / MIMIT: Rete di Accesso Provincia di Livorno"
    url: "https://www.sinfi.it"
    type: "ufficiale"
    note: "Inquadramento infrastrutturale e dorsali interurbane"
---

# La Rete FTTH nel Comune di Collesalvetti

Il territorio del Comune di Collesalvetti (provincia di Livorno) si estende per circa **109 chilometri quadrati** con una tipica conformazione toscana policentrica, composta dal capoluogo e da sei frazioni principali collocate tra la piana alluvionale verso Livorno e Pisa e le colline livornesi.

Questa pagina offre un quadro oggettivo, verificabile e documentato dello stato della rete in fibra ottica FTTH, elaborato a partire dai dati geospaziali dello **Snapshot 3 (rilievo del 04/10/2026)** e dagli atti ufficiali pubblicati all'Albo Pretorio municipale.

---

## 1. Quadro Quantitativo Generale (Snapshot 3 - 04/10/2026)

Rispetto ai precedenti rilievi (Snapshot 1 di 12,07 km e Snapshot 2 di 13,50 km), lo **Snapshot 3** registra un incremento consistente di opere di scavo, posa e censimento, portando la rete rilevata a oltre **21,7 chilometri**:

| Parametro Rilevato | Snapshot 1 (Storico) | Snapshot 2 (Settembre 2026) | **Snapshot 3 Corrente (04/10/2026)** | Variazione S2 $\rightarrow$ S3 |
|---|:---:|:---:|:---:|:---:|
| **Totale Feature Geospaziali** | 47 | 49 | **63** | +14 feature (+28,6%) |
| **Elementi Puntuali (Apparati)** | 31 | 31 | **34** | +3 apparati (+9,7%) |
| **Elementi Lineari (Tratte e Scavi)** | 12 | 14 | **25** | +11 tratte (+78,6%) |
| **Elementi Areali (Poligoni)** | 4 | 4 | **4** | Invariati (perimetri rilievo) |
| **Chilometri Totali Tracciati** | 12,070 km | 13,503 km | **21,716 km** | **+8,213 km (+60,8%)** |

---

## 2. Censimento Apparati sul Territorio

I 34 elementi puntuali censiti sul suolo comunale e di confine comprendono:

| Tipologia Apparato | Categoria GIS | Quantità Rilevata | Operatore / Rete | Note di Rilievo |
|---|---|:---:|---|---|
| **Armadio Ripartilinea Ottico** | `arlo` | **21** | FiberCop / Wholesale | Armadi passivi stradali installati su basamento in cemento accanto ai vecchi ARL |
| **Armadio Ripartilinea Rame** | `arl` | **8** | TIM (Rete Storica) | Armadi rame tradizionali della rete secondaria, molti dotati di modulo ONU FTTC |
| **Centrale di Commutazione** | `centrale` / `centrale_esterna` | **3** | Rete Fissa Primaria | 2 centrali comunali (Collesalvetti, Vicarello) + 1 Centrale Feeder a Livorno (a 4,1 km dal confine) |
| **Pozzetto di Derivazione** | `infrastruttura` | **2** | Rete Sotterranea | Camerette rompitratta con derivazione dorsale |
| **Totale Apparati** | | **34** | | |

---

## 3. Ripartizione Geografica per Frazione

La suddivisione chilometrica e infrastrutturale evidenzia come la frazione di **Stagno** concentri oltre la metà dell'infrastruttura complessiva, seguita da **Collesalvetti capoluogo** e **Vicarello**:

| Frazione | Lunghezza Tratte (km) | Quota % Chilometrica | ARLO Fibra | ARL Rame | Centrali TLC | Tratte e Cantieri Principali |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Stagno** | **11,232 km** | 51,7% | 13 | 4 | 0 | Cantiere 2 (Ord. 102/2026), Cantiere 3 Via Aiaccia (da collegare a ordinanza), Ripristino Via Marx |
| **Collesalvetti (Centro)** | **6,444 km** | 29,7% | 6 | 3 | 1 | Cantiere 1 (Ord. 95/2026), rotatoria Via Nenni/Via Roma, dorsale Via del Valico a Pisa |
| **Vicarello** | **3,122 km** | 14,4% | 2 | 1 | 1 | Dorsale urbana e centrale di commutazione locale |
| **Guasticce** | **0,399 km** | 1,8% | 0 | 0 | 0 | Tratta dorsale primaria di collegamento |
| **Altro / Intercomunale** | **0,519 km** | 2,4% | 0 | 0 | 1 | Opera sulla Backbone e Centrale Feeder esterna (Comune di Livorno) |
| **Totale Territoriale** | **21,716 km** | **100,0%** | **21** | **8** | **3** | |

---

## 4. Registro dei Cantieri e delle Ordinanze di Polizia Municipale

L'incrocio tra gli atti formali pubblicati sull'Albo Pretorio e i riscontri dei sopralluoghi sul terreno permette di documentare lo stato reale dei lavori, separando i termini dell'ordinanza dagli scostamenti effettivi.

```
NOTE METODOLOGICHE SULLA NUMERAZIONE DEGLI ATTI:
Nel Comune di Collesalvetti ciascuna ordinanza riceve due identificativi distinti:
1. Numero interno di settore della Polizia Municipale (es. P.M. n. 88 o n. 95)
2. Numero di Registro Generale del Comune (es. Reg. Gen. 95 o Reg. Gen. 102)
Per garantire la massima trasparenza, questo osservatorio cita sempre entrambi i numeri.
```

### Ordinanze Ufficiali Identificate

#### 1. Cantiere 2 - Stagno (Nuova Espansione FTTH)
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 95 del 10/09/2026 (**Registro Generale n. 102**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 17/2026 del 16/07/2026
- **Periodo da Ordinanza:** Dal **21/09/2026** al **16/10/2026** (fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Otto Marzo, Via Romita, Via De Gasperi, Via Machiavelli, Via XXV Aprile, Piazza Di Vittorio
- **Lunghezza Tratta:** 1,43 km stimati
- **Prescrizioni di Viabilità:** Divieti di sosta con rimozione forzata ambo i lati, sensi unici alternati a vista o regolati da movieri/semaforo temporaneo
- **Rilievo di Campo (Snapshot 3 al 04/10/2026):** *Slittamento osservato.* I lavori sul campo risultano posticipati con avvio effettivo programmato dal **05/10/2026** al **17/10/2026**.
- **File Documentale:** [`ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf`](file:///c:/Users/blankdisk/Documents/GitHub/fiberpulse/ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf)

#### 2. Cantiere 1 - Collesalvetti Centro
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 88 del 02/09/2026 (**Registro Generale n. 95**)
- **Richiedente:** Fastweb S.p.A. per conto della rete FTTH FiberCop
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 10/2026 del 14/05/2026
- **Periodo da Ordinanza:** Dal **14/09/2026** al **02/10/2026** (fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Nenni, Via Roma (rotatoria intersezione Via Nenni), Via del Valico a Pisa, Via di Cerretello
- **Lunghezza Tratta:** 2,60 km stimati
- **Stato Giuridico:** **Termini scaduti il 02/10/2026.**
- **Rilievo di Campo (Snapshot 3 al 04/10/2026):**
  - **Tratte eseguite:** 2 tratte completate (Via Nenni e rotatoria con minitrincee fresate e pozzetti posati).
  - **Tratte non eseguite:** 5 tratte risultano non ancora scavate alla scadenza dell'atto (presenza di soli tracciamenti con vernice spray blu sull'asfalto).
- **File Documentale:** [`ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf`](file:///c:/Users/blankdisk/Documents/GitHub/fiberpulse/ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf)

#### 3. Lavori di Ripristino Manto Stradale - Stagno
- **Atto Ufficiale:** Ordinanza Polizia Municipale n. 70 del 16/07/2026 (**Registro Generale n. 75**)
- **Richiedente:** Fastweb S.p.A.
- **Autorizzazione Tecnica:** Autorizzazione Settore Tecnico n. 10/2025 del 16/07/2025
- **Periodo da Ordinanza:** Dal **03/08/2026** al **13/08/2026** (fascia feriale 08:00 – 18:00)
- **Vie Coinvolte:** Via Marx (accesso Chiesa San Luca e ponte Fosso Cateratto), Via Guerrazzi (angolo Via Curiel), Via La Malfa
- **Lunghezza Tratta:** 0,85 km
- **Stato Lavori:** **Conclusi formalmente e sul campo.**
- **File Documentale:** [`ordinanze/ordinanza_75_2026_stagno_ripristino.pdf`](file:///c:/Users/blankdisk/Documents/GitHub/fiberpulse/ordinanze/ordinanza_75_2026_stagno_ripristino.pdf)

---

## 5. Tratte Rilevate "Da Collegare a Ordinanza"

In conformità ai principi di trasparenza del progetto civico, le seguenti tratte geospaziali individuate nello Snapshot 3 **non sono state collegate ad alcun atto formale**, non essendo state rinvenute ordinanze di Polizia Municipale corrispondenti:

1. **Cantiere 3 (19/10 - 23/10) - Via Aiaccia (Stagno):**
   - 4 tratte lineari per complessivi **3,475 km**.
   - Tracciato lungo la viabilità di Via Aiaccia verso il confine di Stagno.
   - Segnalato come *"da collegare a un'ordinanza"* in attesa di eventuale futura pubblicazione all'Albo Pretorio.
2. **Opera sulla Backbone (Luglio 2026):**
   - Tratta lineare di **0,519 km** (519 metri) situata ad ovest del confine comunale.
   - Dorsale di interconnessione interurbana verso Livorno.
   - Non associata a ordinanza di viabilità ordinaria.

---

## 6. Dichiarazione d'Indipendenza e Metodologia Civica

Questo osservatorio è un'iniziativa informativa indipendente senza scopo di lucro, gestita da cittadini ed esperti di telecomunicazioni. Non è sponsorizzato né affiliato con il Comune di Collesalvetti, con la Polizia Municipale, né con le società FiberCop, Telecom Italia, Fastweb o Open Fiber.

Tutti i dati cartografici e le tabelle vengono rilasciati con licenza aperta per consentire a cittadini, comitati di quartiere e amministratori di verificare lo stato reale dei servizi di connettività sul territorio comunale.
