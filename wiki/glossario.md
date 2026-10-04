---
title: "Glossario Tecnico e Normativo della Fibra Ottica"
summary: "Oltre 40 definizioni ragionate e rigorose di sigle, apparati, protocolli trasmissivi e concetti normativi impiegati nelle reti di telecomunicazione fisse italiane."
updated: "2026-10-04"
sources:
  - id: "itu-telecom-glossary"
    title: "ITU Telecommunication Standardization Bureau: ICT Terms and Definitions"
    url: "https://www.itu.int"
    type: "standard"
    note: "Definizioni degli standard fisici e protocolli trasmissivi"
  - id: "agcom-glossario"
    title: "AGCOM: Glossario dei termini tecnici di rete fissa e mobile"
    url: "https://www.agcom.it"
    type: "ufficiale"
    note: "Definizioni dei profili di accesso wholesale (VULA, Bitstream, NGA) e classificazione aree"
---

# Glossario Tecnico e Normativo della Fibra Ottica

Un repertorio di consultazione rapida con oltre 40 lemmi fondamentali, ordinati alfabeticamente.

---

### 10G-PON
Famiglia di standard per reti ottiche passive capaci di erogare 10 Gbps di capacità nominale. Include sia lo standard simmetrico XGS-PON (10G down / 10G up) sia il profilo asimmetrico XG-PON (10G down / 2.5G up).

### ADSL (*Asymmetric Digital Subscriber Line*)
Tecnologia di accesso su doppino telefonico tradizionale in rame a frequenze fino a 1,1 MHz o 2,2 MHz (ADSL2+), con velocità massima teorica di 24 Mbps in download e 1 Mbps in upload, fortemente soggetta a degrado per distanza.

### ARL (*Armadio Ripartilinea*)
L'armadio metallico stradale tradizionale della rete telefonica in rame (Telecom Italia/TIM) in cui si incontrano i cavi primari provenienti dalla centrale e i cavi secondari diretti alle chiostrine degli edifici.

### ARLO (*Armadio Ripartilinea Ottico*)
Armadio stradale totalmente passivo introdotto da FiberCop per ospitare la terminazione delle fibre primarie dalla centrale, gli splitter ottici primari (tipicamente 1:4) e la partenza delle fibre verso i singoli stabili.

### Attenuazione Ottica
La perdita di potenza del segnale luminoso che si propaga lungo la fibra, espressa in decibel (dB) o decibel per chilometro (dB/km). Nelle fibre monomodali standard vale circa 0,35 dB/km a 1310 nm e 0,20 dB/km a 1550 nm.

### Bitstream
Servizio di accesso all'ingrosso (*wholesale*) in cui l'operatore di rete trasporta il traffico dell'utente fino a un punto di interconnessione centrale o regionale concordato con l'operatore telefonico venditore.

### Borchia Ottica
Presa a muro terminale (solitamente di formato 80x80 mm) installata all'interno dell'abitazione dell'utente, che protegge il raccordo tra il cavo montante proveniente dal PTE e la bretella ottica verso l'ONT.

### Cavi LSZH (*Low Smoke Zero Halogen*)
Cavi isolati con mescole termoplastiche che in caso di incendio non emettono alogeni tossici e producono fumi opachi minimi. Obbligatori per legge nelle montanti e negli ambienti interni.

### CdS (*Codice della Strada*)
Decreto Legislativo 30 aprile 1992, n. 285. Disciplina le autorizzazioni di circolazione, i divieti e le ordinanze comunali di viabilità per l'esecuzione di lavori e scavi su strade pubbliche (artt. 5, 6, 7 e 21).

### Chiostrina
Scatola di derivazione della vecchia rete telefonica in rame, fissata sui muri esterni o nei locali contatori, da cui partono i singoli doppietti telefonici verso gli appartamenti.

### Cladding (Mantello)
Strato cilindrico di vetro di silice ultrapuro da 125 $\mu m$ di diametro che avvolge il nucleo (*core*) della fibra ottica con un indice di rifrazione inferiore, consentendo la riflessione totale interna.

### CNO (*Centro di Nodo Ottico*)
Apparato stradale primario utilizzato nelle architetture Open Fiber (specialmente nelle Aree Bianche BUL) per concentrare le fibre dei vari PoP e distribuire le tratte verso i pozzetti di derivazione.

### Core (Nucleo)
La parte centrale della fibra ottica in cui viaggia l'impulso luminoso. Nelle fibre monomodali standard (G.652 e G.657) ha un diametro nominale microscopico di soli **9 micrometri ($\mu m$)**.

### DBA (*Dynamic Bandwidth Allocation*)
Algoritmo intelligente eseguito dall'OLT in centrale per ripartire dinamicamente la banda di upstream tra gli ONT collegati allo stesso albero GPON/XGS-PON, prevenendo collisioni di pacchetti e ottimizzando i tempi di latenza.

### Diafonia (*Crosstalk*)
Disturbo elettromagnetico che si verifica quando il segnale elettrico ad alta frequenza che scorre in un conduttore in rame genera un campo indotto sui conduttori vicini, riducendo la velocità delle linee adiacenti. Assente nella fibra ottica.

### Dispersione Cromatica
Fenomeno ottico per cui le diverse componenti spettrali (lunghezze d'onda) di un impulso luminoso viaggiano a velocità di gruppo leggermente diverse nel vetro, provocando un allargamento temporale dell'impulso che limita la portata su distanze molto elevate.

### Drop Cable (Cavo di Sgancio)
Il cavo ottico monofibra o bifibra sottile, leggero e flessibile che connette il PTE nell'androne dell'edificio alla borchia ottica all'interno dell'appartamento.

### Feeder (Cavo Primario)
Cavo ottico ad altissima capacità (generalmente da 72 a 288 fibre) posato nelle canalizzazioni principali tra la centrale di commutazione e l'armadio di strada (ARLO o CNO).

### FTTC (*Fiber to the Cabinet*)
Architettura mista in cui la fibra ottica raggiunge l'armadio stradale (ARL), mentre la tratta finale fino a casa dell'utente rimane costituita dal vecchio doppino telefonico in rame. Identificata dal bollino giallo **FR**.

### FTTH (*Fiber to the Home*)
Architettura a banda ultralarga pura in cui il conduttore in fibra ottica collega ininterrottamente la centrale telefonica fino alla presa interna all'alloggio dell'utente. Identificata dal bollino verde **F**.

### FWA (*Fixed Wireless Access*)
Tecnologia che combina una dorsale in fibra ottica fino alla stazione radio base (BTS) con un collegamento wireless su frequenze dedicate (licenziate o libere) verso un'antenna ricevente installata sull'edificio dell'utente.

### G.652.D
Standard internazionale dell'ITU-T che definisce la fibra monomodale standard a basso picco d'acqua (*Low Water Peak*), utilizzata in tutto il mondo per cavi primari e dorsali di trasporto.

### G.657 (A1, A2, B3)
Standard ITU-T per fibre ottiche monomodali insensibili alle curvature (*bend-insensitive*), che possono essere piegate con raggi fino a 7,5 mm senza disperdere segnale, indispensabili per il cablaggio domestico.

### Giunzione a Fusione (*Fusion Splice*)
Metodo definitivo di unione di due fibre ottiche mediante l'allineamento microscopico dei nuclei e la fusione del vetro ottenuta con una scarica ad arco voltaico controllato.

### GPON (*Gigabit Passive Optical Network*)
Standard ITU-T G.984 per reti ottiche passive con velocità massima condivisa di 2,488 Gbps in download (a 1490 nm) e 1,244 Gbps in upload (a 1310 nm).

### Infratel Italia
Società in-house del Ministero delle Imprese e del Made in Italy (MIMIT), soggetto attuatore dei piani governativi per la banda ultralarga (Aree Bianche, Piano Italia a 1 Giga, Scuole e Sanità Connesse).

### Latenza (Ping / RTT)
Il tempo (in millisecondi, ms) impiegato da un pacchetto dati per andare dal dispositivo dell'utente a un server remoto e tornare indietro (*Round Trip Time*). Nelle reti FTTH è generalmente compreso tra 2 e 8 ms verso nodi nazionali.

### Microtrincea
Scavo stradale a basso impatto eseguito con disco diamantato, di larghezza compresa tra 2,5 e 4 cm e profondità di 15-20 cm, utilizzato prevalentemente su marciapiedi e piste ciclabili.

### Minitrincea
Tecnica di scavo con fresa a disco rotante e aspirazione continua delle polveri, avente larghezza di circa 5-10 cm e profondità di 30-40 cm, utilizzata per la posa di fasci di microtubi sotto carreggiata stradale.

### Muffola Ottica
Contenitore plastico a tenuta stagna (grado IP68) posizionato all'interno di pozzetti o camerette stradali, al cui interno sono racchiusi e protetti i giunti a fusione delle fibre.

### No-Dig (Trivellazione Orizzontale Controllata - TOC)
Tecnica di posa sotterranea guidata senza scavo a cielo aperto, che consente di infilare tubazioni sotto incroci, ferrovie o fiumi senza interrompere la circolazione superficiale.

### ODF (*Optical Distribution Frame*)
Permutatore ottico modulare installato all'interno della centrale telefonica, che funge da interfaccia di connessione e test tra le schede laser degli OLT e i cavi primari uscenti in strada.

### OLT (*Optical Line Terminal*)
L'apparato attivo principale situato nella centrale di telecomunicazioni, responsabile della conversione dei pacchetti IP della rete Internet in fasci laser ottici modulati verso gli utenti.

### ONT (*Optical Network Terminal*)
L'apparato elettronico attivo collocato presso l'utente finale, che riconverte gli impulsi luminosi della fibra ottica in segnali elettrici standard su interfaccia Ethernet RJ45 a 1, 2.5 o 10 Gbps.

### OPM (*Optical Power Meter*)
Strumento portatile di misura utilizzato dai tecnici per quantificare con precisione assoluta la potenza ottica (espressa in dBm) presente su una determinata lunghezza d'onda.

### OTDR (*Optical Time Domain Reflectometer*)
Riflettometro ottico nel dominio del tempo: strumento diagnostico avanzato che analizza la luce riflessa all'interno della fibra, individuando con precisione metrica la posizione e l'entità di ogni giunzione, curva anomala o rottura.

### PFS (*Punto di Flessibilità Secondario*)
Armadio ripartilinea ottico stradale impiegato nelle reti Open Fiber delle grandi città (corrispettivo dell'ARLO di FiberCop).

### Pigtail
Spezzone corto di fibra ottica monomodale semirigida già intestato in fabbrica a una estremità con un connettore SC/APC, utilizzato per collegare tramite fusione una fibra nuda a una bussola di permutazione.

### PON (*Passive Optical Network*)
Topologia di rete ottica punto-multipunto in cui la ripartizione del segnale tra centrale e utenze avviene esclusivamente mediante componenti fisici passivi (splitter), senza alimentazione elettrica stradale.

### PTE (*Punto di Terminazione d'Edificio*)
Scatola di derivazione ottica posizionata all'ingresso o nel vano scale di un immobile (spesso identificata anche come ROE), che contiene lo splitter secondario e i connettori verso gli appartamenti.

### Return Loss (Perdita di Ritorno Ottico - ORL)
Il rapporto, espresso in decibel positivi (dB), tra la potenza ottica incidente e la frazione di potenza riflessa all'indietro verso la sorgente. Più è alto il valore (es. > 60 dB nei connettori SC/APC), migliore è la stabilità del laser.

### ROE (*Ripartitore Ottico d'Edificio*)
Sinonimo diffuso di PTE, utilizzato originariamente da Telecom Italia e Open Fiber per indicare il punto di permutazione e terminazione della fibra all'interno dei condomini.

### SC/APC
Connettore ottico a innesto rapido (*Subscriber Connector*) con ferrule in ceramica lucidata con un'angolazione di **8 gradi** (*Angled Physical Contact*), contraddistinto dal colore verde della plastica. È lo standard universale delle reti FTTH italiane.

### SC/UPC
Connettore ottico simile all'SC ma con lucidatura piana ortogonale a 0 gradi (*Ultra Physical Contact*), di colore blu, sconsigliato nelle reti PON ad alta potenza per l'eccessiva riflessione verso la sorgente.

### SINFI (*Sistema Informativo Nazionale Federato delle Infrastrutture*)
Catasto digitale nazionale delle infrastrutture del sottosuolo e di superficie, gestito da Infratel per favorire la condivisione dei cavidotti e prevenire scavi duplicati tra diversi gestori di servizi.

### Splitter Ottico Passivo
Componente microscopico basato su guide d'onda planari in silice (PLC - *Planar Lightwave Circuit*) che divide equamente la potenza luminosa in ingresso tra più fibre in uscita (es. 1:4, 1:8, 1:16 o 1:32) senza richiedere corrente elettrica.

### SUAP (*Sportello Unico Attività Produttive*)
La piattaforma telematica municipale attraverso cui le imprese depositano le istanze autorizzative per gli scavi stradali e l'installazione di impianti tecnologici sul suolo comunale.

### Vectoring
Algoritmo avanzato di cancellazione del rumore per linee FTTC VDSL2, che analizza ed elimina in tempo reale la diafonia tra i diversi doppini in rame attestati sullo stesso armadio.

### VULA (*Virtual Unbundled Local Loop*)
Offerta all'ingrosso regolamentata dall'AGCOM che consente a un operatore alternativo di noleggiare l'accesso in fibra ottica fino alla centrale di zona (PoP) dell'operatore di rete proprietario.

### WDM (*Wavelength Division Multiplexing*)
Tecnica di trasmissione ottica che multipla simultaneamente più canali dati indipendenti sulla stessa fibra fisica utilizzando lunghezze d'onda (colori di luce) differenti.

### XGS-PON
Standard ITU-T G.9807.1 per reti ottiche passive capaci di trasmettere alla velocità **simmetrica di 10 Gbps sia in download che in upload**, utilizzando lunghezze d'onda a 1577 nm (down) e 1270 nm (up).
