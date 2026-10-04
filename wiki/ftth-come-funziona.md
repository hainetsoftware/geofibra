---
title: "Come Funziona la Fibra FTTH"
summary: "Principi fisici della propagazione della luce, topologia di rete punto-multipunto PON e architettura trasmissiva dall'OLT di centrale fino al modem domestico."
updated: "2026-10-04"
sources:
  - id: "itu-g652"
    title: "ITU-T Recommendation G.652: Characteristics of a single-mode optical fibre and cable"
    url: "https://www.itu.int/rec/T-REC-G.652"
    type: "standard"
    note: "Specifiche fisiche del core in silice e coefficienti di attenuazione spettrale"
  - id: "itu-g984"
    title: "ITU-T Recommendation G.984.1: Gigabit-capable passive optical networks (GPON)"
    url: "https://www.itu.int/rec/T-REC-G.984.1"
    type: "standard"
    note: "Architettura dell'albero ottico punto-multipunto e allocazione del power budget"
  - id: "fibra-click-ftth"
    title: "Guida all'architettura FTTH nelle reti italiane"
    url: "https://fibra.click/ftth/"
    type: "guida"
    note: "Riferimenti topologici e componentistica di posa in Italia"
---

# Come Funziona la Fibra FTTH (Fiber to the Home)

La tecnologia **FTTH** (*Fiber to the Home*, fibra fino a casa) rappresenta il vertice dell'evoluzione delle reti di telecomunicazione ad accesso fisso. A differenza delle architetture ibride che impiegano ancora tratti metallici in rame (come l'ADSL o l'FTTC), una linea FTTH trasporta il segnale informativo interamente sotto forma di impulsi luminosi dal punto di commutazione centrale fino alla presa all'interno dell'abitazione dell'utente.

---

## 1. Principi Fisici: La Luce nel Vetro

Il conduttore di un cavo in fibra ottica è un filamento di finissimo vetro di silice ultrapuro ($SiO_2$), dal diametro complessivo confrontabile con quello di un capello umano. La struttura si suddivide in due strati concentrici:

1. **Nucleo (*Core*):** la zona cilindrica centrale, con diametro di appena **9 micrometri ($\mu m$)** nelle fibre monomodali per telecomunicazioni. Presenta un indice di rifrazione $n_1$.
2. **Mantello (*Cladding*):** il guscio cilindrico circostante, con diametro di **125 $\mu m$**, avente un indice di rifrazione leggermente inferiore $n_2 < n_1$.

```
       +-------------------------------------------------------+
       | Mantello (Cladding, diametro 125 µm, indice n2)       |
+------+-------------------------------------------------------+------+
| Luce | Nucleo (Core, diametro 9 µm, indice n1 > n2)                  | Luce
| ===> | ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~> | ===>
+------+-------------------------------------------------------+------+
       | Mantello (Cladding, diametro 125 µm, indice n2)       |
       +-------------------------------------------------------+
```

### Riflessione Totale Interna e Lunghezze d'Onda
Quando un impulso di luce laser viene iniettato nel nucleo con un angolo d'incidenza superiore all'angolo critico $\theta_c = \arcsin(n_2 / n_1)$, non riesce a fuoriuscire nel mantello e subisce il fenomeno della **riflessione interna totale** (*total internal reflection*), propagandosi per decine di chilometri con perdite minime.

Nelle comunicazioni ottiche non si impiega luce visibile, bensì radiazione nello spettro del vicino infrarosso, dove la silice presenta finestre di trasparenza a bassissima attenuazione:
- **1310 nm:** tipicamente usata per la trasmissione da utente verso la centrale (*upstream*).
- **1490 nm:** impiegata per la trasmissione dalla centrale verso l'utente (*downstream* in standard GPON).
- **1550 nm - 1577 nm:** utilizzata per i segnali XGS-PON a 10 Gbps e broadcast avanzati.

L'attenuazione media su una fibra monomodale moderna oscilla tra appena **0,18 e 0,35 dB per ogni chilometro**, un valore infinitesimale rispetto alla dissipazione resistiva e dielettrica che subisce un segnale ad alta frequenza su un doppino in rame.

---

## 2. Architettura di Rete: La Topologia Punto-Multipunto (PON)

La stragrande maggioranza degli accessi FTTH residenziali nel mondo e in Italia (reti FiberCop e Open Fiber) adotta l'architettura **PON** (*Passive Optical Network*, Rete Ottica Passiva). 

La caratteristica essenziale di una rete PON è l'essere **totalmente passiva lungo il percorso stradale**: tra la centrale telefonica e l'abitazione dell'utente finale non è presente alcun apparato attivo alimentato da corrente elettrica (come amplificatori, rigeneratori o switch da alimentare sui marciapiedi). Lo sdoppiamento del segnale avviene tramite minuscoli prismi o accoppiatori ottici integrati (*splitter passivi*).

```mermaid
flowchart LR
    OLT["Centrale TLC (OLT)"] -->|Cavo Primario Feeder| ARLO["Armadio Ottico (ARLO / CNO)"]
    ARLO -->|Splitter 1:4 / 1:8| DIST["Rete di Distribuzione"]
    DIST -->|Cavo Secondario| PTE["Scatola d'Edificio (PTE / ROE)"]
    PTE -->|Splitter 1:16 / Caduta| BORCHIA["Borchia Ottica Utente"]
    BORCHIA --> ONT["Terminale Utente (ONT)"]
    ONT --> ROUTER["Router Domestico"]
```

---

## 3. La Catena Trasmissiva: Dalla Centrale all'Appartamento

Il collegamento attraversa sei livelli strutturali chiaramente identificabili:

| Livello | Elemento di Rete | Posizione Fisica | Funzione Principale |
|---|---|---|---|
| **1. Sorgente** | **OLT** (*Optical Line Terminal*) | Centrale di commutazione (PoP) | Genera i fasci laser, gestisce la banda di tutti gli alberi ottici e instarda i pacchetti IP verso la rete di trasporto nazionale. |
| **2. Primaria** | **Tratta Primaria (*Feeder*)** | Sottosuolo, cavidotti principali | Cavi multifiocina ad alta capacità (da 72 a 288 fibre) che uniscono la centrale ai vari armadi ripartilinea ottici nei quartieri. |
| **3. Ripartizione** | **ARLO / CNO** | Marciapiede / stradale | Armadio stradale passivo dove le fibre primarie vengono derivate tramite un primo stadio di sdoppiamento ottico (*splitting*). |
| **4. Secondaria** | **Tratta di Distribuzione** | Minitrincee stradali / tombini | Microcavi flessibili che collegano l'armadio stradale ai singoli fabbricati o numeri civici serviti. |
| **5. Edificio** | **PTE / ROE** | Vano contatori / androne / facciata | Punto di Terminazione d'Edificio: scatola stagna in cui terminano i cavi stradali e da cui partono le bretelle verso gli appartamenti. |
| **6. Terminale** | **Borchia Ottica & ONT** | All'interno dell'appartamento | La presa a muro termina la fibra; l'ONT riconverte gli impulsi fotonici in pacchetti elettrici Ethernet diretti al router. |

---

## 4. Perché la Fibra è Superiore al Rame

1. **Immunità Elettromagnetica Assoluta:** Essendo il vettore ottico costituito da fotoni che viaggiano in un dielettrico trasparente (vetro), la fibra non capta interferenze causate da cavi di media/alta tensione, fulmini, scariche elettrostatiche o radiodiffusione.
2. **Assenza di Diafonia (*Zero Crosstalk*):** Nelle reti in rame, centinaia di doppini stipati nello stesso cavo generano interferenza elettromagnetica reciproca (*crosstalk*), degradando sensibilmente le prestazioni. Nelle fibre ogni impulso resta confinato nel rispettivo nucleo.
3. **Indipendenza dalla Distanza Urbana:** Se una connessione FTTC decade da 200 Mbps a 30 Mbps qualora ci si trovi a 600 metri dall'armadio, la fibra ottica garantisce prestazioni identiche a 50 metri come a 10 chilometri dalla centrale.
4. **Scalabilità Futura Illimitata:** La capacità fisica intrinseca di una fibra monomodale supera svariati Terabit al secondo. Per passare da una connessione a 1 Gbps a una a 10 Gbps (XGS-PON) o 50 Gbps (50G-PON) non è necessario riaprire le strade: basta sostituire i terminali elettronici (OLT e ONT) ai due estremi della linea.
