---
title: "Gli Apparati Fisici della Rete sul Territorio"
summary: "Guida illustrativa al riconoscimento e alla funzione degli elementi visibili e sotterranei della rete FTTH: centrali OLT, cavi Feeder, armadi ARLO, pozzetti, muffole stagne e distributori ottici PTE/ROE."
updated: "2026-10-04"
sources:
  - id: "fibercop-arch"
    title: "FiberCop: Architettura di Rete e Specifiche Tecniche di Ripartizione"
    url: "https://www.fibercop.it"
    type: "documentazione"
    note: "Specifiche costruttive e topologia di sdoppiamento ARLO/PTE"
  - id: "openfiber-pfs"
    title: "Open Fiber: Schema Tecnico di Distribuzione Urbana (Cluster A&B)"
    url: "https://openfiber.it"
    type: "documentazione"
    note: "Specifiche per PFS, CNO e montanti d'edificio"
---

# Gli Apparati Fisici della Rete sul Territorio

Passeggiando lungo le vie di un comune servito dalla fibra ottica è possibile osservare decine di componenti fisici, sia a livello stradale che all'interno degli edifici. Questa guida spiega come identificarli e quale ruolo svolgono nell'infrastruttura di accesso.

---

## 1. Centrale di Telecomunicazioni (PoP / OLT)

La centrale telefonica è l'edificio tecnico principale dell'operatore di rete presente nel comune o nel circondario.

- **Cosa contiene:** I telai con gli apparati attivi **OLT** (*Optical Line Terminal*), i permutatori generali delle fibre ottiche (**ODF** - *Optical Distribution Frame*), i banchi di batterie di soccorso in corrente continua a 48V e i generatori diesel per garantire la continuità del servizio anche durante blackout prolungati.
- **Riconoscimento:** Edifici in muratura spesso storici (ex SIP/Telecom Italia), privi di finestre o con grate di aerazione pesante, dotati di parabole e recinzioni di sicurezza. Nel Comune di Collesalvetti sono presenti centrali locali (Collesalvetti capoluogo, Vicarello) oltre a interconnessioni verso la Centrale Feeder interurbana.

---

## 2. Il Cavo di Alimentazione Primaria (*Feeder*)

Dal permutatore di centrale partono i cavi primari della rete ottica.
- **Caratteristiche:** Cavi corazzati a nastro d'acciaio o dielettrici antiroditore, contenenti un numero molto elevato di fibre (tipicamente **144, 192 o 288 fibre ottiche** raggruppate in tubetti colorati).
- **Posa:** Transitano nei cavidotti sotterranei principali (tubazioni da 110 mm o 125 mm) e arrivano direttamente all'interno degli armadi stradali senza subire alcuna derivazione intermedia.

---

## 3. Armadio Ripartilinea Ottico (ARLO / CRO / PFS)

L'armadio ripartilinea ottico è l'elemento più riconoscibile della rete stradale. Nelle aree coperte da **FiberCop** prende il nome di **ARLO** (*Armadio Ripartilinea Ottico*); nelle reti **Open Fiber** è denominato **CNO** (*Centro di Nodo Ottico*) o **PFS** (*Punto di Flessibilità Secondario*).

| Caratteristica | Rete Rame Tradizionale (ARL) | Rete Fibra Ottica (ARLO / CNO) |
|---|---|---|
| **Denominazione** | ARL (*Armadio Ripartilinea*) | ARLO (*Armadio Ripartilinea Ottico*) |
| **Aspetto Visivo** | Struttura metallica grigia stretta e alta, spesso sormontata dal modulo ONU "tettoia rossa" | Struttura più larga e tozza, colore grigio chiaro o antracite, con chiusura a doppia serratura |
| **Alimentazione Elettrica** | Sì, se convertito in FTTC con ONU attiva a 230V | **No, 100% passivo** (nessun allaccio elettrico, zero ventole) |
| **Capacità** | Centinaia di coppie in rame su morsettiere a saldare o a incisione | Fino a centinaia di connettori ottici e alloggiamenti per splitter passivi |
| **Collocazione** | Storicamente collocato all'angolo delle vie | Installato a terra sul proprio basamento prefabbricato in cemento, quasi sempre **affiancato al vecchio ARL rame** |

All'interno dell'ARLO:
1. Le fibre primarie dalla centrale si innestano nella semisezione primaria.
2. I cavi secondari diretti ai palazzi si innestano nella semisezione secondaria.
3. Al centro risiedono gli **splitter ottici passivi** (con rapporto di sdoppiamento primario tipico di **1:4** in FiberCop).

---

## 4. Pozzetti Stradali e Camerette Rompitratta

Lungo i marciapiedi e le carreggiate si incontrano chiusini in ghisa o cemento con aperture per sonde e passaggio cavi:
- **Marchiature comuni:** *TIM*, *SIP*, *FiberCop*, *Open Fiber*, *Fastweb*, *BUL Infratel*.
- **Dimensioni normalizzate:**
  - **Pozzetti 40x40 cm:** utilizzati per cambi di direzione o giunzioni terminali vicino ai civici.
  - **Pozzetti 76x40 cm:** posati lungo le tratte di minitrincea stradale per l'infilaggio dei cavi.
  - **Camerette 125x80 cm:** ospitano le muffole di giunzione principali e i cambi di dorsale.

---

## 5. Muffole di Giunzione Ottica

Collocate all'interno dei pozzetti o sospese su palificate, le muffole sono involucri cilindrici in materiale plastico ad altissima resistenza con guarnizioni termorestringenti o meccaniche con grado di protezione **IP68** (totale tenuta stagna e resistenza all'immersione continua in acqua e fango).

All'interno della muffola:
- I cavi ottici vengono sguainati.
- Le fibre vengono alloggiate in cassetti di giunzione a ribalta (*tray*).
- I giunti a fusione sono protetti da tubetti termorestringenti con anima metallica d'irrigidimento (*smouv*).

---

## 6. Punto di Terminazione d'Edificio (PTE / ROE)

Il **PTE** (*Punto di Terminazione d'Edificio*, chiamato anche **ROE** - *Ripartitore Ottico d'Edificio*) rappresenta il confine tra la rete pubblica dell'operatore e la rete interna del condominio o della singola abitazione.

- **Dove si trova:** Di norma nel locale contatori, nell'androne scale, all'esterno sulla facciata del fabbricato (in cassetta grigia stagna) o all'interno della chiostrina rame preesistente.
- **Funzionamento:** Riceve il cavo multifibra proveniente dall'armadio ARLO. Al suo interno è ospitato il secondo stadio di sdoppiamento ottico (splitter con rapporto tipico **1:16** in architettura FiberCop).
- **Terminazione:** Da qui partono i cavi monofibra verticali (*drop*) che salgono lungo i corrugati dello stabile per raggiungere gli appartamenti degli utenti che richiedono l'attivazione.
