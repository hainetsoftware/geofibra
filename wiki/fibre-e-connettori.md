---
title: "Fibre Ottiche, Cavi e Connettori"
summary: "Caratteristiche dei conduttori in silice: standard monomodali ITU-T G.652.D e G.657, tipologie di connettori SC/APC vs SC/UPC, tecniche di fusione ad arco voltaico e codici colore normati."
updated: "2026-10-04"
sources:
  - id: "itu-g657"
    title: "ITU-T Recommendation G.657: Characteristics of a bending-loss insensitive single-mode optical fibre and cable"
    url: "https://www.itu.int/rec/T-REC-G.657"
    type: "standard"
    note: "Definizione delle classi A1, A2, B2 e B3 per fibre insensibili alla piega"
  - id: "cei-86-46"
    title: "Norma CEI 86-46: Cavi in fibra ottica per telecomunicazioni e codice colori dei conduttori"
    url: "https://www.ceiweb.it"
    type: "standard"
    note: "Sequenza convenzionale italiana delle 12 colorazioni per tubetto"
---

# Fibre Ottiche, Cavi e Connettori

L'efficienza di un'infrastruttura FTTH dipende dalla precisione microscopica dei componenti di giunzione e dalla conformità dei materiali agli standard internazionali.

---

## 1. Fibre Monomodali: Standard G.652.D vs G.657

Nelle telecomunicazioni geografiche e nell'accesso FTTH si impiegano esclusivamente fibre **monomodali** (*Single Mode Fiber*), che consentono la propagazione di un solo modo fondamentale di luce lungo l'asse ottico, eliminando la dispersione modale tipica delle vecchie fibre multimodali da 50 o 62,5 $\mu m$.

L'ITU-T definisce due famiglie principali di fibre monomodali:

| Standard ITU-T | Denominazione Comune | Raggio Minimo di Curvatura | Applicazione Tipica nella Rete FTTH |
|---|---|:---:|---|
| **ITU-T G.652.D** | *Standard Low Water Peak* | **30 mm** | Cavi primari (*Feeder*) e dorsali di trasporto interurbane. Ottimizzata per bassissima attenuazione complessiva lungo tratti rettilinei o in ampi cavidotti. |
| **ITU-T G.657.A1** | *Bend-Insensitive (Grado 1)* | **10 mm** | Cavi di distribuzione stradale secondaria e tubazioni sotterranee con curve strette. |
| **ITU-T G.657.A2** | *Bend-Insensitive (Grado 2)* | **7,5 mm** | **Montanti verticali d'edificio e cablaggio interno all'appartamento.** Sopporta angoli retti attorno agli stipiti delle porte o dentro scatole di derivazione 503 senza subire perdite di luce apprezzabili. |
| **ITU-T G.657.B3** | *Ultra Bend-Insensitive* | **5,0 mm** | Patch cord terminali e situazioni di posa estreme ad altissimo raggio di curvatura. |

---

## 2. Connettori Ottici: SC/APC vs SC/UPC

Nelle reti ottiche, la qualità del connettore è determinata dalla finitura geometrica della ferrule in ceramica (ossido di zirconio) che allinea i due nuclei da 9 micrometri.

```
       SC/UPC (Ultra Physical Contact)         SC/APC (Angled Physical Contact)
            Corpo connettore: BLU                   Corpo connettore: VERDE

               +--------------+                        +--------------+
               |              |                        |            / | (Inclinazione
               |  Fronte 0°   |                        |  Fronte 8°/  |  a 8 gradi)
               |  (Piatto)    |                        |          /   |
               +--------------+                        +--------------+
            Return Loss: ≥ 50 dB                    Return Loss: ≥ 60 dB
```

### Perché in FTTH si usa esclusivamente il connettore SC/APC (Verde)?
Nel connettore **SC/UPC** (blu, a taglio ortogonale a 0 gradi), una frazione microscopica della luce laser che incontra la discontinuità aria-vetro viene riflessa indietro direttamente verso la sorgente lungo lo stesso asse del nucleo.

Nel connettore **SC/APC** (verde, lucidato con un angolo di **8 gradi**), la luce riflessa non torna indietro nel nucleo ma rimbalza verso il mantello (*cladding*), dove si disperde innocua. Questo garantisce un valore di **Optical Return Loss (ORL) superiore a 60 dB**, indispensabile per non danneggiare i trasmettitori laser degli OLT e per evitare disturbi di fase sulle modulazioni ad alta velocità GPON e XGS-PON.

> [!CAUTION]
> Non inserire mai un connettore blu (UPC) in una presa verde (APC): l'inclinazione differente danneggerebbe irreparabilmente le superfici lucidate delle ferrule in ceramica, causando gravissime perdite ottiche.

---

## 3. Giunzione per Fusione (*Fusion Splicing*)

A differenza dei cavi elettrici in rame, che possono essere uniti con semplici morsetti o mammut, due fibre ottiche non possono essere intrecciate. La giunzione permanente richiede una **saldatrice a fusione ad arco voltaico**:

1. **Spellatura e pulizia:** La guaina protettiva esterna in acrilato (da 250 $\mu m$) viene rimossa per circa 3 cm; la fibra nuda viene lavata con alcool isopropilico ultrapuro.
2. **Taglio di precisione (*Cleaving*):** Una taglierina con lama diamantata esegue un'incisione e una frattura ortogonale controllata con deviazione angolare inferiore a 0,5 gradi rispetto alla normale.
3. **Allineamento automatico sul nucleo (*Core Alignment*):** La giuntatrice inquadra i due nuclei con telecamere microscopiche su due assi ortogonali (X e Y) e li allinea con micromotori piezoelettrici.
4. **Scarica dell'arco voltaico:** Due elettrodi di tungsteno generano una scintilla calibrata che fonde istantaneamente il vetro di silice (a circa 1600 °C), saldando i due tronconi in un unico filamento continuo.
5. **Protezione termo-restringente (*Smouv*):** Il punto fuso viene avvolto da una cannuccia con anima in acciaio inossidabile e cotto in un fornetto a 200 °C per conferire rigidità meccanica.

La perdita tipica di una giunzione a fusione ben eseguita è inferiore a **0,02 - 0,05 dB**.

---

## 4. Codice Colori Convenzionale delle Fibre (Norma CEI 86-46)

All'interno di un cavo multifibra, i singoli filamenti di vetro sono rivestiti da uno strato di acrilato colorato per permettere ai tecnici di identificarli univocamente durante le operazioni di intestazione negli armadi e nei giunti. In Italia, la sequenza unificata segue la norma **CEI 86-46**:

| Posizione Fibra | Colore Tubetto / Fibra | Codice Esadecimale Rappresentativo |
|:---:|---|:---:|
| **1** | **Rosso** | `#E53935` |
| **2** | **Bianco** | `#FFFFFF` |
| **3** | **Blu** | `#1E88E5` |
| **4** | **Verde** | `#43A047` |
| **5** | **Giallo** | `#FDD835` |
| **6** | **Grigio** | `#757575` |
| **7** | **Marrone** | `#6D4C41` |
| **8** | **Viola** | `#8E24AA` |
| **9** | **Nero** | `#212121` |
| **10** | **Arancione** | `#FB8C00` |
| **11** | **Rosa** | `#F06292` |
| **12** | **Turchese / Celeste** | `#00ACC1` |
