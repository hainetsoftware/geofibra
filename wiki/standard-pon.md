---
title: "Standard PON: GPON, XGS-PON e NG-PON2"
summary: "L'evoluzione degli standard di rete ottica passiva definiti dall'ITU-T: multiplazione spettrale, lunghezze d'onda, bit rate simmetrici, fattori di splitting e coesistenza WDM sulla stessa fibra."
updated: "2026-10-04"
sources:
  - id: "itu-g984"
    title: "ITU-T Recommendation G.984 Series: Gigabit-capable passive optical networks"
    url: "https://www.itu.int/rec/T-REC-G.984"
    type: "standard"
    note: "Specifiche trasmissive e frame di multiplazione dello standard GPON"
  - id: "itu-g9807"
    title: "ITU-T Recommendation G.9807.1: 10-Gigabit-capable symmetric passive optical networks (XGS-PON)"
    url: "https://www.itu.int/rec/T-REC-G.9807.1"
    type: "standard"
    note: "Architettura, allocazione spettrale e ottiche per trasmissione simmetrica a 10 Gbps"
  - id: "itu-g989"
    title: "ITU-T Recommendation G.989 Series: 40-Gigabit-capable passive optical networks (NG-PON2)"
    url: "https://www.itu.int/rec/T-REC-G.989"
    type: "standard"
    note: "Standard multi-lunghezza d'onda TWDM per operatori e reti convergenti"
---

# Standard PON: GPON, XGS-PON e NG-PON2

Nelle reti di telecomunicazione fisse ad accesso ottico, la standardizzazione internazionale curata dall'**ITU-T** (*International Telecommunication Union - Telecommunication Standardization Sector*) garantisce l'interoperabilità tra apparati di centrale (OLT) e apparati utente (ONT) di produttori diversi.

---

## 1. Multiplazione Temporale (TDM / TDMA)

Nelle reti PON ad albero, una singola fibra in uscita dalla centrale viene condivisa tra più clienti (tipicamente 16, 32 o 64 utenze) attraverso splitter passivi:

- **Direzione Downstream (Centrale $\rightarrow$ Utenti):** L'OLT trasmette un flusso ottico continuo in broadcast contenente i pacchetti di tutti gli utenti. Ogni ONT domestico riceve tutti i fotogrammi, ma decifra ed elabora unicamente quelli a sé indirizzati grazie a una chiave di cifratura hardware **AES-128**.
- **Direzione Upstream (Utenti $\rightarrow$ Centrale):** Poiché decine di trasmettitori condividono la medesima fibra, se trasmettessero simultaneamente i segnali colliderebbero distruggendosi. L'OLT governa il traffico tramite un algoritmo di **DBA** (*Dynamic Bandwidth Allocation*): assegna a ciascun ONT specifici intervalli temporali (*time slot*) nell'ordine dei microsecondi durante i quali il laser dell'utente può accendersi ed emettere dati.

---

## 2. Tabella Sinottica degli Standard ITU-T

| Parametro Tecnico | GPON (ITU-T G.984) | XGS-PON (ITU-T G.9807.1) | NG-PON2 (ITU-T G.989) | 50G-PON (ITU-T G.9804) |
|---|---|---|---|---|
| **Anno Approvazione** | 2003 - 2008 | 2016 | 2015 | 2021 |
| **Banda Downstream** | **2,488 Gbps** | **9,953 Gbps (~10 Gbps)** | 4 $\times$ 10 Gbps (TWDM) | **49,766 Gbps (~50 Gbps)** |
| **Banda Upstream** | **1,244 Gbps** | **9,953 Gbps (~10 Gbps)** | 4 $\times$ 10 Gbps (TWDM) | 12,5 / 25 / 50 Gbps |
| **Simmetria di Banda** | Asimmetrico (2,5G / 1,25G) | **Simmetrico (10G / 10G)** | Simmetrico o asimmetrico | Simmetrico o asimmetrico |
| **Lunghezza d'Onda Downstream** | 1480 – 1500 nm (tipico **1490 nm**) | 1575 – 1580 nm (tipico **1577 nm**) | 1596 – 1603 nm | 1340 – 1344 nm |
| **Lunghezza d'Onda Upstream** | 1290 – 1330 nm (tipico **1310 nm**) | 1260 – 1280 nm (tipico **1270 nm**) | 1524 – 1544 nm | 1260 – 1280 nm |
| **Split Ratio Tipico** | 1:64 (max 1:128) | 1:64 (max 1:128) | 1:64 / 1:256 | 1:64 / 1:128 |
| **Optical Power Budget** | Classe B+ (28 dB), C+ (32 dB) | Nominale 29 dB (Class N1/N2/E1) | 29 – 32 dB | 29 – 32 dB |
| **Uso in Italia** | Standard di massa (Open Fiber, FiberCop) | Profili 2,5G / 10G (TIM, Iliad, Fastweb, OF) | Sperimentale / Business | Lab e prime prove sul campo |

---

## 3. Coesistenza Spettrale sulla Stessa Fibra (Filtro WDM1r)

Una caratteristica ingegneristica fondamentale dello standard XGS-PON è la possibilità di **coesistere sulla medesima infrastruttura in fibra ottica** già stesa per il GPON, senza interruzioni di servizio e senza dover sostituire i cavi interrati o gli splitter negli armadi stradali.

Ciò è reso possibile dalla rigorosa separazione delle lunghezze d'onda luminose:

```
SPETTRO LUNGHEZZE D'ONDA (nm):
1260      1280      1300      1320             1490             1577
 |---------|         |---------|                |                |
 XGS-PON Up            GPON Up               GPON Down       XGS-PON Down
 (1270 nm)            (1310 nm)              (1490 nm)        (1577 nm)
```

In centrale viene inserito un filtro passivo chiamato **WDM1r** (*Wavelength Division Multiplexing Coexistence Element*):
- Il fascio a 1490 nm (GPON) e quello a 1577 nm (XGS-PON) vengono combinati nella stessa fibra.
- A casa dell'utente che sottoscrive un contratto base a 1 Gbps, l'ONT GPON legge unicamente la luce a 1490 nm scartando le altre lunghezze d'onda.
- Nel medesimo condominio, un utente con abbonamento a 10 Gbps riceve un ONT XGS-PON che filtra e decodifica la finestra a 1577 nm, mentre trasmette verso la centrale sulla frequenza a 1270 nm senza generare la minima interferenza sul vicino.
