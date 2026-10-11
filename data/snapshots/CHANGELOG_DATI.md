# Cronologia Rilievi Geospaziali (Snapshot KML)

Registro delle versioni dei dati cartografici della rete FTTH e cantieri nel Comune di Collesalvetti (LI).

---

## Snapshot 4 — 11 Ottobre 2026 (Stato Corrente)
- **File sorgente:** `data/snapshots/rilievo_snapshot4.kml` (e `FTTH Collesalvetti_snapshot4.kml`)
- **Feature totali censite:** **68** (37 punti, 27 linee, 4 poligoni)
- **Sviluppo lineare tracciato:** **21,780 km** (+64 m netti da anello raccordo rotatoria e nuove tratte)
- **Apparati censiti (Snapshot 4):** **35** nel territorio comunale (24 ARL, 4 ARLO, 1 centrale comunale, 6 centrali di frazione) + 1 esterno (Centrale Feeder, Livorno). Conteggi in `data/stats.json`, metodologia in `docs/APPARATI_RECOUNT.md`.
- **Novità principali:**
  - **Collesalvetti Capoluogo - Primo ARLO e Hub Rotatoria:**
    - Posato il **primo armadio ottico FiberCop del capoluogo** (`C [] ARLO`, futuro ARLO 01) alle coordinate `[10.475255, 43.593980]`, situato nell'aiuola/marciapiede della rotatoria tra Via Roma, Via Nenni e Via Piero Ciampi.
    - Stato: `Installato (Opere civili completate - In attesa di soffiaggio fibra/PTE)`.
    - Dettagli tecnici: Plinto gettato, cabinet montato, **4 pozzetti di smistamento FiberCop** posati a corona della rotatoria e raccordati ai cavidotti storici TIM.
    - **Tratta Eseguita Sud-Est (Cantiere 1):** Convalidate come completate le tratte su Via del Valico a Pisa, Via Peppino Impastato, Via di Cerretello e l'anello di raccordo rotatoria (`Cantiere 1 AGGIUNTO`, 71,8 m). Tipologia di posa: minitrincea sigillata (microtubi *Fender 4x10/14*) + riuso cavidotti storici TIM.
    - **Tratta Non Eseguita Nord-Ovest (Via Nenni):** Mantenuto il layer non eseguito (marcature spray blu a terra). Nota aggiornata: *Termini Ordinanza 88/2026 scaduti il 02/10; in attesa di nuova ordinanza viaria / proroga per il comparto Via Nenni*.
  - **Stagno - Parco ARLO e Chiusura Cantiere 2:**
    - Censimento complessivo degli armadi ottici di Stagno attestato a **3 nodi ARLO mappati** (`S [27]`, `S [28]` e il nuovo `S [] ARLO` privo di etichetta numerica posato in affiancamento al rame `S [04] ARL` all'angolo Via Romita / Via XXV Aprile).
    - Distinzione chiarita tra i **6 armadi rame storici ARL** (S [02]...S [07]) e i **3 armadi ottici FTTH ARLO** posati finora nella frazione.
    - Confermato e validato l'ARLO privo di etichetta posato in affiancamento al rame `S [04] ARL` (`[10.353902, 43.589311]`) su Via Romita / angolo Via XXV Aprile.
    - Stato armadi Stagno: `Infrastrutturati / In fase di cablaggio e predisposizione secondaria`.
    - **Cantiere 2 (Ord. 104/2026, 05/10 - 17/10):** Stato `In completamento (Posa condotte completata, 6 pozzetti in fase di getto/chiusura finale)`. Rilevata e convalidata tratta completata su Via Romita sud e Via XXV Aprile (`Cantiere 2 ESEGUITO`, 292,9 m).
  - **Stagno - Cantiere 3 Autorizzato (Ord. 105/2026 + Concessione Suolo 77/2026):**
    - Tratte lungo Via Aiaccia e Via Umbria (4 tratte lineari per 3,475 km).
    - Finestra temporale autorizzata: `19/10/2026 - 23/10/2026` (5 giorni feriali, occupazione 60 mq).
    - Stato: `Autorizzato / Avvio programmato`.
    - Nota cartografica: Innesto sud di Via Aiaccia verso la direttrice provinciale come punto di raccordo con la tratta dorsale SP555 autorizzata a luglio 2026.
- **Avanzamento Complessivo:**
  - **Collesalvetti Centro:** incremento al **41,5%** di avanzamento infrastrutturale (grazie a primo ARLO, hub rotatoria e tratte Sud-Est).
  - **Stagno:** consolidamento all'**86,4%** di avanzamento (3 nodi ARLO censiti su 6 ARL rame, chiusura imminente Cantiere 2 e Cantiere 3 programmato).
  - **Comune di Collesalvetti (Globale):** avanzamento complessivo attestato al **62,8%** (in netta crescita rispetto al 52,4% di inizio mese).

---

## Snapshot 3 — 04 Ottobre 2026
- **File sorgente:** `data/snapshots/rilievo_snapshot3.kml`
- **Feature totali censite:** **63** (34 punti, 25 linee, 4 poligoni)
- **Sviluppo lineare tracciato:** **21,716 km**
- **Apparati censiti (Snapshot 3):** **32** nel territorio comunale (23 ARL, 2 ARLO, 1 centrale comunale, 6 centrali di frazione) + 1 esterno (Centrale Feeder, Livorno). Il 34° punto (`Coppie di corrugati scoperti`) è un punto di infrastruttura, non un apparato. Conteggi in `data/stats.json`, metodologia in `docs/APPARATI_RECOUNT.md`.
- **Novità principali:**
  - **Aggiornamento Cantiere 1 (Collesalvetti Centro):** suddivisione in 2 tratte verificate come eseguite (`Cantiere 1 ESEGUITO`, sopralluoghi 29/09 e 03/10 con riscontro di minitrincee, corrugati e pozzetti FiberCop) e 5 tratte (`Cantiere 1 NON ESEGUITO`, solo segni spray blu su asfalto).
  - **Aggiornamento Cantiere 2 (Stagno Centro):** slittamento finestra lavori al 05/10 - 17/10 (rispetto all'originario 21/09 - 16/10 previsto dall'Ord. 102/2026).
  - **Nuovo Cantiere 3 (Stagno / Via Aiaccia):** censite 4 tratte per complessivi 3,475 km previste per il 19/10 - 23/10. *Nota: privo di ordinanza comunale formalmente collegata nel tracker.*
  - **Seconda tratta INFRATEL BUL:** +3,462 km di dorsale pubblica per il rilegamento delle centrali collinari di Parrana San Martino e Parrana San Giusto. Totale dorsale BUL a 9,995 km.
  - **Completamenti di posa Stagno:** 4 nuove tratte secondarie (+0,828 km), totale tratte Stagno a 3,008 km.
  - **Opera sulla Backbone (07/2026):** tratta di dorsale di 519 m a ovest di Stagno. *Da collegare a un'ordinanza.*
  - **Riconoscimento apparati:**
    - Identificato armadio ottico FiberCop `S [28] ARLO` (ex `S [0?] ARLO`).
    - Censito nuovo armadio ottico FiberCop `S [27] ARLO` a Stagno.
    - Censito armadio rame `S [03] ARL` a Stagno (risolve il gap numerico di frazione).
    - Censita `Centrale Feeder` esterna (Livorno) di alimentazione a monte della rete comunale.
- **Aree e superfici:**
  - Stagno: 37,17 ha coperti su 46,30 ha perimetrati (80,28%).
  - Collesalvetti Centro: 20,55 ha coperti su 66,15 ha perimetrati (31,07%).

---

## Snapshot 2 — 10 Settembre 2026
- **File sorgente:** `data/snapshots/rilievo_snapshot2.kml`
- **Feature totali censite:** **49** (31 punti, 14 linee, 4 poligoni)
- **Sviluppo lineare tracciato:** **13,503 km**
- **Novità rispetto a Snapshot 1:**
  - Censimento del nuovo **Cantiere 2 - Stagno** autorizzato dall'Ordinanza P.M. n. 95 (Reg. Gen. 102/2026) del 10/09/2026 (+1,43 km di scavi su 6 vie).
  - Espansione del poligono di copertura a Stagno da 28,65 ha a **37,17 ha** (+29,7% di superficie, tasso al 80,3%).

---

## Snapshot 1 — Rilievo Iniziale Storico
- **File sorgente:** `data/snapshots/rilievo_snapshot1.kml`
- **Feature totali censite:** **46** (31 punti, 11 linee, 4 poligoni)
- **Sviluppo lineare tracciato:** **12,073 km**
  - Dorsale INFRATEL BUL: 6,533 km
  - Cantieri Collesalvetti C1: 2,666 km
  - Tratte Stagno posa: 2,180 km
  - Tratto Sanità Connesse: 0,348 km
  - Tratto Scuole Connesse: 0,346 km
- **Superfici:**
  - Collesalvetti Centro: 20,55 ha coperti vs 45,59 ha non coperti (31,07%).
  - Stagno Centro: 28,65 ha coperti vs 17,29 ha non coperti (62,37%).
