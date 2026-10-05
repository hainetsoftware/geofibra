# Dossier di Audit Rete FTTH & Checklist Sopralluoghi IRL
**Comune di Collesalvetti (LI) — Analisi Infrastrutturale e Verifica sul Campo**
*Basato sui dati geospaziali di mappatura territoriale*

---

## 1. Analisi Comparativa delle Numerazioni e Gaps (Buchi di Rete)

> **Nota:** la tabella seguente riflette lo stato di **Snapshot 1** (in Snapshot 3 Stagno ha 5 ARL + 2 ARLO e `S [0?] ARLO` è stato rinumerato `S [28] ARLO`). Conteggi correnti: `docs/APPARATI_RECOUNT.md` e `data/stats.json`.

Dall'incrocio di tutti gli apparati censiti per frazione, emergono anomalie, armadi con numerazione dubbia e buchi sequenziali molto interessanti:

| Frazione | Armadi Censiti (ARL / ARLO) | Sequenza Rilevata | Armadi Mancanti / Gaps da Cercare | Note Speciali di Rete |
| :--- | :--- | :--- | :--- | :--- |
| **Vicarello (V)** | **8 ARL** | `01, 02, 03, 04, 05, 06, 07, 08` | **Nessuno (Sequenza 100% completa)** | Il cabinet `V [05]` è contrassegnato come *"NUOVO DAL 2025"*. |
| **Collesalvetti (C)** | **7 ARL** | `01, 02, 04, 9605, 9606, 07, 08` | **`C [03]`**, **`C [05]`**, **`C [06]`** (?) | Presenza anomala della serie a 4 cifre `9605` e `9606`. Il `C [08]` ha la dicitura *"NUMERO DA VERIFICARE IRL"*. |
| **Stagno (S)** | **4 ARL + 1 ARLO** | `0?, 02, 04, 05, 07` | **`S [01]`**, **`S [03]`**, **`S [06]`** | Il cabinet ottico FiberCop `S [0?] ARLO` non ha numero censito. |
| **Guasticce (G)** | **3 ARL** | `01, 02, 0?` | **`G [03]`** (?) | L'armadio `G [0?]` ha l'alimentazione Enel appesa allo SLAM ed è da verificare. |

### 🔍 Focus Tecnico sulla Serie a 4 Cifre (`C [9605]` e `C [9606]`)
Nella topologia TIM/Telecom Italia:
- I numeri a 4 cifre che iniziano per `9xxx` indicano spesso **armadi derivati speciali**, armadi dedicati a **aree artigianali/commerciali**, oppure derivazioni storiche collegate a vecchi ponti radio o centraline remote.
- A Collesalvetti mancano proprio il numero `05` e il numero `06`: è altamente probabile che `9605` e `9606` siano le denominazioni Telecom ufficiali assegnate proprio a questi due armadi!

---

## 2. Stime di Copertura FTTH (Superfici e Percentuali)

Analisi spaziale dei poligoni di copertura mappati per i due centri urbani principali:

### 🏙️ Collesalvetti (Capoluogo)
- **Superficie Area Coperta FTTH:** $205.513\ m^2$ (**20,55 ettari** / $0,206\ km^2$)
- **Superficie Area NON Coperta:** $455.950\ m^2$ (**45,59 ettari** / $0,456\ km^2$)
- **Superficie Totale Perimetrata:** $661.463\ m^2$ ($0,661\ km^2$)
- 📊 **Tasso di Copertura FTTH Collesalvetti:** **31,07% Coperto** vs **68,93% Non Coperto**
- *Insight:* La parte coperta si concentra prevalentemente nel quadrante nord-est/centro (scuole medie, asilo, asse principale), mentre la fascia a sud e a ovest risulta attualmente non raggiunta dalla primaria FiberCop.

### 🌊 Stagno
- **Superficie Area Coperta FTTH:** $286.535\ m^2$ (**28,65 ettari** / $0,287\ km^2$)
- **Superficie Area NON Coperta:** $172.855\ m^2$ (**17,29 ettari** / $0,173\ km^2$)
- **Superficie Totale Perimetrata:** $459.390\ m^2$ ($0,459\ km^2$)
- 📊 **Tasso di Copertura FTTH Stagno:** **62,37% Coperto** vs **37,63% Non Coperto**
- *Insight:* A Stagno la copertura è notevolmente più avanzata (oltre il 62% dell'abitato), supportata dalle tratte di posa recenti (Maggio-Giugno 2026).

---

## 3. Metrature Lineari dell'Infrastruttura Mappata

| Tratta / Tipologia Scavo | Lunghezza Totale (m) | Lunghezza (km) | Note Operatore / Appalto |
| :--- | :--- | :--- | :--- |
| **Dorsale INFRATEL BUL** | $6.533,3\ m$ | **$6,53\ km$** | Dorsale strategica regionale aree bianche/grigie |
| **Cantieri Collesalvetti (6 tratte)** | $2.665,9\ m$ | **$2,67\ km$** | Scavi e ripristini stradali eseguiti (14/09-02/10) |
| **Tratte Stagno (2 tratte)** | $2.180,3\ m$ | **$2,18\ km$** | Posa recente cavi ottici (Maggio-Giugno 2026) |
| **Tratto Sanità Connesse** | $348,3\ m$ | **$0,35\ km$** | Bando Fastweb: allaccio RSA S. Caterina e USL |
| **Tratto Scuole Connesse** | $345,6\ m$ | **$0,35\ km$** | Raccordo ARL 01 a Scuole medie e asilo "I cubi" |
| **TOTALE SVILUPPO RETE TRACCIATA** | **$12.073,4\ m$** | **$12,07\ km$** | **Oltre 12 chilometri di infrastruttura censita!** |

---

## 4. Checklist Operativa per Sopralluoghi IRL (Field Inspection)

Questa lista ordina gli obiettivi prioritari da verificare fisicamente sul campo a Collesalvetti e frazioni.

### 🎯 Obiettivo 1: Verifica Numero ARL 08 (Collesalvetti)
- [ ] **Stato di verifica:** Da confermare sul campo
- **Apparato segnato:** `C [08] ARL`
- **Coordinate GPS:** `43.587389, 10.476109`
- **Quota:** $47,0\ m$ s.l.m.
- **Cosa cercare:** Armadio Telecom isolato senza ARLO a fianco.
- **Cosa verificare sul posto:**
  1. Verificare l'etichetta nera/gialla adesiva sul fronte o sul fianco dell'armadio. Riporta davvero il numero **08** o un numero diverso (es. 03, 05, o un'altra serie)?
  2. Verificare se alla base o sul chiusino adiacente ci sono marchi Telecom/SIP.
- 📍 **[Apri Posizione su Google Maps](https://www.google.com/maps?q=43.587389,10.476109)**

---

### 🎯 Obiettivo 2: Identificazione Numero ARLO Stagno
- [ ] **Stato di verifica:** Numero sconosciuto (`S [0?] ARLO`)
- **Apparato segnato:** `S [0?] ARLO`
- **Coordinate GPS:** `43.590687, 10.356220`
- **Quota:** $9,2\ m$ s.l.m.
- **Cosa cercare:** Armadio ottico moderno grigio chiaro FiberCop.
- **Cosa verificare sul posto:**
  1. Controllare la targhetta identificativa blu/bianca o la matricola alfanumerica di FiberCop (solitamente serigrafata in alto a sinistra o sulla serratura).
  2. Verificare a quale ARL rame è associato o se è un'installazione autonoma (*stand-alone*).
- 📍 **[Apri Posizione su Google Maps](https://www.google.com/maps?q=43.590687,10.356220)**

---

### 🎯 Obiettivo 3: Identificazione Numero ARL Guasticce
- [ ] **Stato di verifica:** Numero sconosciuto (`G [0?] ARL`)
- **Apparato segnato:** `G [0?] ARL`
- **Coordinate GPS:** `43.606389, 10.437333`
- **Quota:** $12,5\ m$ s.l.m.
- **Nota sul campo registrata:** *"Alimentazione e-distribuzione appesa allo SLAM - Da verificare numero IRL"*
- **Cosa verificare sul posto:**
  1. Leggere la matricola dell'ARL e dello SLAM/ONU soprastante (solitamente ha un cartellino giallo con cifre nere riflettenti).
  2. Verificare se corrisponde all'armadio `G [03]` mancante nella sequenza di Guasticce.
- 📍 **[Apri Posizione su Google Maps](https://www.google.com/maps?q=43.606389,10.437333)**

---

### 🎯 Obiettivo 4: Ispezione "Coppie di Corrugati Scoperti"
- [ ] **Stato di verifica:** Punto critico di vulnerabilità infrastrutturale
- **Elemento segnato:** `Coppie di corrugati scoperti`
- **Coordinate GPS:** `43.600611, 10.474639`
- **Cosa verificare sul posto:**
  1. Tipologia e colore dei corrugati (es. rosso/nero da 110mm, minitubo blu/arancio o fender).
  2. Stato di conservazione: sono tagliati, chiusi con nastro o esposti all'acqua/vegetazione?
  3. Presenza di cavi ottici già infilati o pozzetto interrato nelle immediate vicinanze.
- 📍 **[Apri Posizione su Google Maps](https://www.google.com/maps?q=43.600611,10.474639)**

---

### 🎯 Obiettivo 5: Caccia ai Tre Armadi Mancanti a Collesalvetti (`03`, `05`, `06`)
- [ ] **Ricerca sul campo:**
  - **`C [03]`**: Cercare lungo la direttrice tra l'armadio 02 e l'armadio 04 o verso la parte bassa del paese.
  - **`C [05]` e `C [06]`**: Confrontare la posizione degli armadi `C [9605]` (`43.588526, 10.472213`) e `C [9606]` (`43.588510, 10.473370`) per verificare se le chiostrine delle case circostanti riportano la dicitura `C 05` / `C 06` oppure `C 9605` / `C 9606`.
