---
title: "Tecnologie a Confronto: FTTH, FTTC, FWA e ADSL"
summary: "Analisi comparativa dettagliata dei parametri fisici, prestazionali e normativi delle tecnologie di accesso broadband e ultrabroadband, con tabella sinottica e bollini AGCOM."
updated: "2026-10-04"
sources:
  - id: "agcom-292-18"
    title: "AGCOM Delibera n. 292/18/CONS: Misure a tutela degli utenti in materia di trasparenza delle offerte di connettività a banda ultralarga"
    url: "https://www.agcom.it/visualizza-documento/3a59807a-d0ff-4e44-8dcf-65fb356ca7d9"
    type: "ufficiale"
    note: "Istituzione formale dei bollini di connettività Verde (F), Giallo (FR) e Rosso (R)"
  - id: "mimit-relazione-annuale"
    title: "Ministero delle Imprese e del Made in Italy: Relazione sullo stato della banda ultralarga in Italia"
    url: "https://www.mimit.gov.it"
    type: "ufficiale"
    note: "Rilevazioni statistiche sull'adozione della banda ultralarga sul territorio nazionale"
---

# Tecnologie a Confronto: FTTH, FTTC, FWA e ADSL

Nel mercato italiano delle telecomunicazioni convivono differenti mezzi trasmissivi. Per tutelare gli utenti dalla pubblicità ingannevole (che in passato etichettava come "fibra" anche linee con chilometri di vecchio rame), l'Autorità per le Garanzie nelle Comunicazioni (**AGCOM**) ha introdotto un sistema rigoroso di certificazione visiva tramite bollini colorati obbligatori.

---

## 1. I Bollini di Connettività AGCOM (Delibera 292/18/CONS)

| Bollino | Simbolo | Denominazione Ufficiale | Tecnologie Abilitate | Criterio Tecnico Distintivo |
|---|:---:|---|---|---|
| **Verde** | **F** | **Fibra Pura (FTTH / FTTB)** | FTTH (*Fiber to the Home*), FTTB (*Fiber to the Building*) | La fibra ottica arriva direttamente all'interno dell'abitazione o almeno alla base del fabbricato. Nessun tratto in rame nella rete pubblica. |
| **Giallo** | **FR** | **Misto Fibra-Rame / Misto Fibra-Radio** | FTTC (*Fiber to the Cabinet*), FWA (*Fixed Wireless Access*) su licenza | La fibra ottica raggiunge l'armadio stradale o la stazione radio base (BTS); la tratta finale verso l'utente è in rame o onde radio. |
| **Rosso** | **R** | **Rame Integrale / Radio Base** | ADSL, HDSL, ponti radio non autorizzati | L'intera tratta di accesso è realizzata in cavo telefonico in rame, senza fibra ottica nella rete distributiva secondaria. |

---

## 2. Tabella Sinottica Comparativa

La seguente tabella riassume le caratteristiche fisiche e prestazionali reali delle quattro principali tecnologie di accesso sul mercato residenziale e business:

| Parametro Fisico / Prestazionale | ADSL (Rame Tradizionale) | FTTC / VDSL2 (Misto Rame) | FWA 5G / Millimetriche (Misto Radio) | FTTH GPON (Fibra Pura) | FTTH XGS-PON (Fibra Pura Avanzata) |
|---|---|---|---|---|---|
| **Bollino Ufficiale AGCOM** | 🔴 **R** (Rosso) | 🟡 **FR** (Giallo) | 🟡 **FR** (Giallo) | 🟢 **F** (Verde) | 🟢 **F** (Verde) |
| **Mezzo Trasmissivo Finale** | Doppino in Rame (0,4-0,6 mm) | Doppino in Rame (0,4-0,6 mm) | Etere (Frequenze radio 3.5 / 26 GHz) | Fibra Ottica Monomodale (9 $\mu m$) | Fibra Ottica Monomodale (9 $\mu m$) |
| **Tratta in Fibra Ottica** | Solo dorsale primaria | Dalla centrale all'armadio stradale | Dalla centrale alla BTS radio | Dalla centrale alla presa domestica | Dalla centrale alla presa domestica |
| **Velocità Max Download** | 20 Mbps | 100 - 200 Mbps | 100 - 300 Mbps (picco 1 Gbps) | 1.000 - 2.500 Mbps | 10.000 Mbps (10 Gbps) |
| **Velocità Max Upload** | 1 Mbps | 20 Mbps | 20 - 50 Mbps | 300 - 1.000 Mbps | 2.000 - 10.000 Mbps |
| **Latenza Tipica (Ping verso Gateway)** | 35 - 70 ms | 15 - 30 ms | 20 - 45 ms | 2 - 8 ms | 1 - 5 ms |
| **Degrado con la Distanza** | Drastico oltre 1,5 km | Severo oltre 300 metri | Vincolo linea visiva (LOS) e ostacoli | Assente in contesto urbano (< 20 km) | Assente in contesto urbano (< 20 km) |
| **Suscettibilità Elettromagnetica** | Molto elevata (crosstalk, fulmini) | Molto elevata (diafonia di diaframma) | Media (attenuazione da pioggia) | Totalmente immune (dielettrico) | Totalmente immune (dielettrico) |
| **Consumo Energetico Locale** | Basso (linea analogica passiva) | Alto (ONU attiva alimentata in armadio) | Medio (apparati radio BTS) | Nullo lungo il tracciato stradale | Nullo lungo il tracciato stradale |

---

## 3. Il Limite Fisico del Rame: Perché la FTTC Non Basta Più

Nell'architettura FTTC (spesso commercializzata come "fibra mista rame"), la fibra ottica collega la centrale all'armadio ripartilinea stradale (ARL). Sopra l'armadio viene installato un modulo alimentato a 230V detto **ONU** (*Optical Network Unit*) o "tettoia rossa", contenente modem VDSL2 (profilo 17a o 35b).

Dall'armadio all'abitazione, tuttavia, il segnale viaggia sul cavo in rame posato spesso 40 o 50 anni fa. Questo comporta tre gravi limiti:

1. **Attenuazione ad alta frequenza:** Il profilo 35b lavora fino a 35 MHz. A tali frequenze il rame si comporta come un filtro passa-basso: ogni 100 metri di distanza dalla colonnina comportano una perdita esponenziale di portante.
2. **Diafonia (*Crosstalk*):** Quando più residenti della stessa via attivano una linea VDSL2, le frequenze radio emesse da ciascun doppino si accoppiano per induzione elettromagnetica sui doppini adiacenti nello stesso cavidotto, riducendo le velocità di tutti fino al 40-50% del valore iniziale (attenuabile parzialmente solo con la tecnologia *Vectoring*).
3. **Degrado da umidità e ossidazione:** Le infiltrazioni d'acqua nelle chiostrine stradali deteriorano la continuità dei giunti rame, provocando disconnessioni cicliche e variazioni del margine rumore (SNR).

---

## 4. Fixed Wireless Access (FWA): Quando Conviene

La tecnologia FWA impiega stazioni radio base collegate in fibra ottica per irradiare il segnale radio verso un'antenna ricevente (*CPE*) installata sul tetto o sul balcone dell'edificio.

- **Vantaggi:** Tempi di attivazione rapidi, ideale per case sparse, zone collinari o frazioni rurali dove i costi di scavo per la fibra ottica sarebbero proibitivi.
- **Svantaggi:** Richiede la visibilità ottica (*Line-of-Sight*) senza alberi o palazzi interposti; risente dell'attenuazione da pioggia battente (*rain fade*) sulle frequenze ad onde millimetriche (26 GHz); la banda disponibile sull'antenna è condivisa fra tutti gli utenti collegati alla medesima cella.
