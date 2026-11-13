// js/cantieri_tracker.js - Monitoraggio Cantieri e Ordinanze Albo Pretorio Comune di Collesalvetti
// Fuso Orario di Riferimento: Europe/Rome

// Copia di data/ordinanze.json per l'uso da file://.
const ORDINANZE_DATA_DEFAULT = [
  {
    "id": "PM-COLLE-ORD-118-2026",
    "titolo": "Cantiere 2 - Collesalvetti (Progettazione esecutiva)",
    "frazione": "Collesalvetti",
    "richiedente": "Fastweb Spa",
    "oggetto": "Lavori di scavo stradale per posa infrastruttura FTTH FiberCop",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "118",
    "atto_registro_generale": "125",
    "codice_atto_completo": "Ordinanza P.M. n. 118/2026 (Reg. Gen. 125/2026, Aut. 28/2026)",
    "data_emissione": "2026-11-09",
    "autorizzazione_settore_tecnico": "Autorizzazione n. 28/2026 del 28/10/2026",
    "periodo_ordinanza": {
      "inizio": "2026-11-16T08:00:00+01:00",
      "fine": "2026-12-04T18:00:00+01:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 7 (rilievo del 05/11/2026)",
      "nota_campo": "Survey 05/11/2026: Road spray paint markings and staged industrial Fender microduct reels already observed on-site. Tied to Municipal Ordinance PM n. 118/2026 (Aut. 28/2026), operative 16/11/2026 - 04/12/2026."
    },
    "lunghezza_stimata_km": 1.071,
    "vie_interessate": [
      {
        "via": "Via Roma (da rotatoria Via Nenni a rotatoria di collegamento con Via Europa)",
        "prescrizione": "Divieto di sosta con rimozione su ambo i lati e senso unico alternato a vista o con movieri"
      },
      {
        "via": "Via del Valico a Pisa",
        "prescrizione": "Divieto di sosta con rimozione su ambo i lati e senso unico alternato a vista o con movieri"
      },
      {
        "via": "Via del Vione",
        "prescrizione": "Divieto di sosta con rimozione su ambo i lati e senso unico alternato a vista o con movieri"
      },
      {
        "via": "Via Guido Rossa",
        "prescrizione": "Divieto di sosta con rimozione su ambo i lati e senso unico alternato a vista o con movieri"
      }
    ],
    "file_pdf": "data/ordinanze/17991_AltreOrdinanze_Copia_125_2026.pdf",
    "coordinate_centro": [
      43.59547,
      10.474
    ],
    "descrizione_ufficiale": "Disciplina temporanea della viabilità nei tratti interessati dal cantiere itinerante.",
    "stato_base": "staged_for_digging"
  },
  {
    "id": "cantiere-2-stagno",
    "titolo": "Cantiere 2 - Stagno (Nuova Espansione FTTH - Ord. 104/2026 + Proroga Ord. 111/2026)",
    "frazione": "Stagno",
    "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
    "oggetto": "Lavori di scavo stradale per posa infrastruttura rete FTTH FiberCop – Stagno, vie varie (comparto sud)",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "95",
    "atto_registro_generale": "104",
    "codice_atto_completo": "Ordinanza P.M. n. 95/2026 (Reg. Gen. 102/104/2026) + Proroga Ord. n. 111 del 16/10/2026",
    "data_emissione": "2026-09-10",
    "autorizzazione_settore_tecnico": "Autorizzazione n. 17/2026 del 16/07/2026",
    "periodo_ordinanza": {
      "inizio": "2026-09-21T08:00:00+02:00",
      "fine": "2026-10-23T18:00:00+02:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 6 (05/11/2026)",
      "inizio_stimato": "2026-10-05T08:00:00+02:00",
      "fine_stimata": "2026-10-23T18:00:00+02:00",
      "nota_campo": "Opere civili completate sulle quattro tratte censite, incluse Via Romita sud, Via De Gasperi, Via Machiavelli e Via XXV Aprile."
    },
    "lunghezza_stimata_km": 1.48,
    "vie_interessate": [
      { "via": "Via Romita sud", "prescrizione": "Divieto di sosta e senso unico alternato con movieri; posa condotte completata" },
      { "via": "Via De Gasperi", "prescrizione": "Divieto di sosta e senso unico alternato regolato da movieri o semaforo" },
      { "via": "Via Machiavelli", "prescrizione": "Mantenimento senso unico con divieto di sosta ambo i lati" },
      { "via": "Via XXV Aprile", "prescrizione": "Mantenimento senso unico con divieto di sosta ambo i lati; nuovo ARLO posato" },
      { "via": "Piazza Di Vittorio", "prescrizione": "Divieto di sosta e senso unico alternato regolato a vista o movieri" },
      { "via": "Via Don Verità", "prescrizione": "Restringimento di carreggiata e divieto di sosta per allaccio utenze" },
      { "via": "Via 8 Marzo", "prescrizione": "Divieto di sosta con rimozione forzata e senso unico alternato" }
    ],
    "file_pdf": "data/ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf",
    "coordinate_centro": [43.5930, 10.3540],
    "descrizione_ufficiale": "Provvedimento di disciplina temporanea della viabilità per esecuzione di scavi stradali per posa della rete in fibra ottica FiberCop a Stagno. Prorogato fino al 23/10/2026 con Ordinanza n. 111/2026.",
    "stato_base": "eseguito"
  },
  {
    "id": "cantiere-3-stagno",
    "titolo": "Cantiere 3 - Stagno (Via Aiaccia / Via Umbria)",
    "frazione": "Stagno",
    "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
    "oggetto": "Lavori di scavo stradale e occupazione suolo pubblico per posa rete FTTH FiberCop lungo Via Aiaccia e Via Umbria",
    "atto_tipo": "Polizia Municipale + Concessione Suolo",
    "atto_numero": "105",
    "atto_registro_generale": "110",
    "codice_atto_completo": "Ordinanza P.M. n. 105/2026 + Concessione Suolo n. 77/2026",
    "data_emissione": "2026-10-01",
    "autorizzazione_settore_tecnico": "Concessione Occupazione Suolo Pubblico n. 77/2026 (occupazione 60 mq)",
    "periodo_ordinanza": {
      "inizio": "2026-10-19T08:00:00+02:00",
      "fine": "2026-10-23T18:00:00+02:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 5 (17/10/2026) - 4 tratte lineari (3,475 km)",
      "inizio_stimato": "2026-10-19T08:00:00+02:00",
      "fine_stimata": "2026-10-23T18:00:00+02:00",
      "nota_campo": "Finestra temporale: 19/10/2026 - 23/10/2026 (5 giorni feriali, occupazione 60 mq). Stato: Autorizzato / Avvio programmato. Punto di raccordo: innesto sud di Via Aiaccia verso la direttrice provinciale con la tratta dorsale autorizzata a luglio 2026."
    },
    "lunghezza_stimata_km": 3.48,
    "vie_interessate": [
      { "via": "Via Aiaccia", "prescrizione": "Divieto di sosta e senso unico alternato con movieri o semaforo per scavo minitrincea" },
      { "via": "Via Umbria", "prescrizione": "Restringimento temporaneo carreggiata e divieto di sosta per posa infrastruttura secondaria" }
    ],
    "file_pdf": "data/ordinanze/pdf/2026-10-01_COLLE_ORD_105_Fastweb_Stagno.pdf",
    "coordinate_centro": [43.5875, 10.3580],
    "descrizione_ufficiale": "Provvedimento di disciplina viaria e concessione suolo pubblico (60 mq) per la posa della dorsale e della rete secondaria FTTH FiberCop lungo Via Aiaccia e Via Umbria.",
    "stato_base": "programmato"
  },
  {
    "id": "ripristino-rosselli-stagno",
    "titolo": "Ripristino Manto Stradale - Fase 1 Stagno (Via Fratelli Rosselli)",
    "frazione": "Stagno",
    "richiedente": "Fastweb S.p.A. per conto FiberCop",
    "oggetto": "Lavori di fresatura e ripristino definitivo del manto stradale sulle tratte FTTH posate a maggio-giugno 2026 in Via Fratelli Rosselli",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "112",
    "atto_registro_generale": "118",
    "codice_atto_completo": "Ordinanza P.M. n. 112 del 16/10/2026",
    "data_emissione": "2026-10-16",
    "autorizzazione_settore_tecnico": "Autorizzazione n. 10/2026",
    "periodo_ordinanza": {
      "inizio": "2026-10-19T08:00:00+02:00",
      "fine": "2026-11-24T18:00:00+02:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 5 (17/10/2026) - Tratte Stagno maggio-giugno 2026",
      "inizio_stimato": "2026-10-19T08:00:00+02:00",
      "fine_stimata": "2026-11-24T18:00:00+02:00",
      "nota_campo": "Ripristino definitivo del manto stradale (fresatura e asfaltatura a caldo) sulle trincee FTTH eseguite a maggio-giugno 2026. Operativo da lunedì 19/10/2026 al 24/11/2026."
    },
    "lunghezza_stimata_km": 0.65,
    "vie_interessate": [
      { "via": "Via Fratelli Rosselli", "prescrizione": "Senso unico alternato e divieto di sosta con rimozione forzata per fresatura e asfaltatura definitiva" }
    ],
    "file_pdf": "data/ordinanze/pdf/2026-10-16_COLLE_RIP_112_Fastweb_Stagno.pdf",
    "coordinate_centro": [43.5898, 10.3535],
    "descrizione_ufficiale": "Provvedimento viario per esecuzione dei ripristini definitivi del manto stradale a seguito degli scavi per la fibra ottica eseguiti a maggio-giugno 2026 lungo Via F.lli Rosselli. Finestra: 19/10/2026 - 24/11/2026.",
    "stato_base": "programmato"
  },
  {
    "id": "cantiere-4-stagno",
    "titolo": "Cantiere 4 - Stagno (Nuova Espansione Ovest - Ord. 110/2026)",
    "frazione": "Stagno",
    "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
    "oggetto": "Lavori di scavo stradale e posa infrastruttura rete FTTH FiberCop – Stagno, comparto ovest/sud-ovest (Via Marx, Via Curiel, ecc.)",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "110",
    "atto_registro_generale": "116",
    "codice_atto_completo": "Ordinanza P.M. n. 110/2026",
    "data_emissione": "2026-10-14",
    "autorizzazione_settore_tecnico": "Autorizzazione Tecnica n. 26/2026",
    "periodo_ordinanza": {
      "inizio": "2026-10-26T08:00:00+01:00",
      "fine": "2026-11-20T18:00:00+01:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 6 (05/11/2026)",
      "nota_campo": "Anello nord completato (Via Karl Marx, Via Gobetti e Via Curiel, 734 m). Restano pianificate tre tratte, tra cui il ramo di Via Don Giovanni Verità (446 m)."
    },
    "lunghezza_stimata_km": 2.052,
    "vie_interessate": [
      { "via": "Via Marx", "prescrizione": "Divieto di sosta e senso unico alternato per posa condotte" },
      { "via": "Via Curiel (lato sud)", "prescrizione": "Divieto di sosta e restringimento carreggiata" },
      { "via": "Via Gobetti", "prescrizione": "Divieto di sosta ambo i lati per scavo minitrincea" },
      { "via": "Via Don Verità", "prescrizione": "Restringimento carreggiata per allacci secondari" },
      { "via": "Via F.lli Cervi", "prescrizione": "Divieto di sosta e senso unico alternato" },
      { "via": "Via La Malfa", "prescrizione": "Restringimento temporaneo carreggiata" },
      { "via": "Via Verga", "prescrizione": "Divieto di sosta con rimozione forzata" },
      { "via": "Via Berlinguer", "prescrizione": "Divieto di sosta e senso unico alternato" }
    ],
    "file_pdf": "data/ordinanze/pdf/2026-10-14_COLLE_ORD_110_Fastweb_Stagno.pdf",
    "coordinate_centro": [43.5885, 10.3480],
    "descrizione_ufficiale": "Provvedimento temporaneo di viabilità per scavo e posa infrastruttura fibra ottica FiberCop a Stagno nel comparto Via Marx / Curiel / Cervi. Finestra: 26/10/2026 - 20/11/2026.",
    "stato_base": "parzialmente_eseguito"
  },
  {
    "id": "cantiere-1-collesalvetti",
    "titolo": "Cantiere 1 - Collesalvetti Centro",
    "frazione": "Collesalvetti",
    "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
    "oggetto": "Lavori di scavo stradale per posa infrastruttura rete FTTH FiberCop – Collesalvetti, vie varie",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "88",
    "atto_registro_generale": "95",
    "codice_atto_completo": "Ordinanza P.M. n. 88 del 02/09/2026 (Reg. Gen. 95)",
    "data_emissione": "2026-09-02",
    "autorizzazione_settore_tecnico": "Autorizzazione n. 10/2026 del 14/05/2026",
    "periodo_ordinanza": {
      "inizio": "2026-09-14T08:00:00+02:00",
      "fine": "2026-10-02T18:00:00+02:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 6 (05/11/2026)",
      "inizio_stimato": "2026-09-14T08:00:00+02:00",
      "fine_stimata": "2026-10-02T18:00:00+02:00",
      "nota_campo": "Due tratte in progettazione esecutiva. Marcature e tecnici osservati su una tratta, soffiaggio della fibra nei pozzetti sull’altra. Su due ulteriori tratte è probabile il riuso dei pozzetti e cavidotti SIP/Telecom."
    },
    "lunghezza_stimata_km": 2.67,
    "vie_interessate": [
      { "via": "Via del Valico a Pisa", "prescrizione": "Tratta Sud-Est ESEGUITA: minitrincea sigillata (microtubi Fender 4x10/14) e riuso cavidotti TIM" },
      { "via": "Via Peppino Impastato", "prescrizione": "Tratta Sud-Est ESEGUITA: minitrincea sigillata e riuso cavidotti TIM" },
      { "via": "Via di Cerretello", "prescrizione": "Tratta Sud-Est ESEGUITA: minitrincea sigillata e pozzetti posati" },
      { "via": "Via Roma (rotatoria Via Nenni / Via Ciampi)", "prescrizione": "Tratta ESEGUITA (Cantiere 1 AGGIUNTO): anello di raccordo rotatoria, posati 4 pozzetti FiberCop e primo ARLO cittadino" },
      { "via": "Via Nenni", "prescrizione": "Tratta Nord-Ovest NON ESEGUITA: marcature blu a terra. Termini Ord. 88/2026 scaduti il 02/10, in attesa di proroga/nuova ordinanza" }
    ],
    "file_pdf": "data/ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf",
    "coordinate_centro": [43.5945, 10.4760],
    "descrizione_ufficiale": "Provvedimento di disciplina della viabilità per scavo e posa infrastruttura in fibra ottica FiberCop nel centro abitato di Collesalvetti.",
    "stato_base": "parziale_scaduto"
  },
  {
    "id": "ripristino-stagno",
    "titolo": "Lavori di Ripristino Manto Stradale Scavi Fibra - Stagno (Via Marx)",
    "frazione": "Stagno",
    "richiedente": "Fastweb S.p.A.",
    "oggetto": "Lavori stradali per ripristino scavi fibra ottica – Stagno, vie varie",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "70",
    "atto_registro_generale": "75",
    "codice_atto_completo": "Ordinanza P.M. n. 70 del 16/07/2026 (Reg. Gen. 75)",
    "data_emissione": "2026-07-16",
    "autorizzazione_settore_tecnico": "Autorizzazione n. 10/2025 del 16/07/2025",
    "periodo_ordinanza": {
      "inizio": "2026-08-03T08:00:00+02:00",
      "fine": "2026-08-13T18:00:00+02:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": null,
    "lunghezza_stimata_km": 0.85,
    "vie_interessate": [
      { "via": "Via Marx (lato opposto accesso Chiesa San Luca)", "prescrizione": "Restringimento carreggiata e senso unico alternato a vista o con semaforo" },
      { "via": "Via Marx (ponte sul Fosso Cateratto, lato nord)", "prescrizione": "Restringimento carreggiata e senso unico alternato" },
      { "via": "Via Guerrazzi (intersezione Via Curiel, lato sud)", "prescrizione": "Restringimento carreggiata e senso unico alternato" },
      { "via": "Via La Malfa", "prescrizione": "Restringimento carreggiata e senso unico alternato" }
    ],
    "file_pdf": "data/ordinanze/ordinanza_75_2026_stagno_ripristino.pdf",
    "coordinate_centro": [43.5910, 10.3520],
    "descrizione_ufficiale": "Provvedimento straordinario di circolazione per esecuzione di ripristini del manto stradale a seguito degli scavi per la fibra ottica a Stagno. Lavori formalmente conclusi.",
    "stato_base": "concluso"
  }
];

let ORDINANZE_DATA = ORDINANZE_DATA_DEFAULT;

// Prova a caricare in modo asincrono data/ordinanze.json se disponibile
if (typeof fetch === 'function') {
  fetch('data/ordinanze.json')
    .then(r => {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(data => {
      if (Array.isArray(data) && data.length > 0) {
        ORDINANZE_DATA = data;
        window.ORDINANZE_DATA = data;
        if (typeof renderCantieriModal === 'function') renderCantieriModal();
        if (typeof updateCantieriNavbarBadge === 'function') updateCantieriNavbarBadge();
      }
    })
    .catch(() => {
      // Usa i dati di default inclusi nel bundle
    });
}

/**
 * Estrae i parametri temporali secondo il fuso orario Europe/Rome
 */
function getRomeTimeParts(date) {
  const d = date || new Date();
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Europe/Rome',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    weekday: 'short',
    hour12: false
  });

  const parts = {};
  formatter.formatToParts(d).forEach(p => {
    parts[p.type] = p.value;
  });

  const monthDay = `${parts.month}-${parts.day}`;
  // Giorni festivi nazionali italiani fissi
  const festiviNazionali = [
    '01-01', // Capodanno
    '01-06', // Epifania
    '04-25', // Liberazione
    '05-01', // Festa dei Lavoratori
    '06-02', // Festa della Repubblica
    '08-15', // Ferragosto
    '11-01', // Ognissanti
    '12-08', // Immacolata
    '12-25', // Natale
    '12-26'  // Santo Stefano
  ];

  const isSunday = parts.weekday === 'Sun';
  const isNationalHoliday = festiviNazionali.includes(monthDay);
  const isWorkingDay = !isSunday && !isNationalHoliday;

  const hour = parseInt(parts.hour, 10);
  const minute = parseInt(parts.minute, 10);

  // Fascia oraria autorizzata dalle ordinanze (08:00 - 18:00)
  const isWorkingHours = (hour >= 8 && hour < 18);

  return {
    year: parseInt(parts.year, 10),
    month: parseInt(parts.month, 10),
    day: parseInt(parts.day, 10),
    hour,
    minute,
    second: parseInt(parts.second, 10),
    weekday: parts.weekday,
    isWorkingDay,
    isWorkingHours,
    dateObj: d
  };
}

function getRomeCurrentDate() {
  return new Date();
}

/**
 * Calcola lo stato del cantiere in base all'ordinanza e all'orario effettivo Europe/Rome.
 */
function calculateCantiereStatus(cantiere, currentDate) {
  const now = currentDate || getRomeCurrentDate();
  const rome = getRomeTimeParts(now);

  // Normalizza date di inizio e fine dell'ordinanza
  const inizioStr = cantiere.periodo_ordinanza ? cantiere.periodo_ordinanza.inizio : (cantiere.inizio || cantiere.inizio_lavori || cantiere.start_date);
  const fineStr = cantiere.periodo_ordinanza ? cantiere.periodo_ordinanza.fine : (cantiere.fine || cantiere.fine_lavori || cantiere.end_date);

  const start = new Date(inizioStr);
  const end = new Date(fineStr);

  const startFormatted = start.toLocaleDateString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'Europe/Rome'
  });
  const endFormatted = end.toLocaleDateString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'Europe/Rome'
  });

  if (cantiere.stato_base === 'eseguito') {
    return {
      statusCode: 'eseguito',
      statusLabel: 'OPERE CIVILI COMPLETATE',
      timingSummary: 'Completamento verificato sul campo',
      isActiveNow: false
    };
  }

  if (cantiere.stato_base === 'parzialmente_eseguito') {
    return {
      statusCode: 'parzialmente_eseguito',
      statusLabel: 'OPERE CIVILI PARZIALMENTE COMPLETATE',
      timingSummary: `Finestra autorizzata ${startFormatted}–${endFormatted}`,
      isActiveNow: now >= start && now <= end && rome.isWorkingDay && rome.isWorkingHours
    };
  }

  // Gestione stato "in_completamento" (es. Cantiere 2 Stagno prorogato al 23/10)
  if (cantiere.stato_base === 'in_completamento' && now <= end) {
    return {
      statusCode: 'in_completamento',
      statusLabel: 'IN COMPLETAMENTO (PROROGA AL 23/10 - 6 POZZETTI ATTORNO AD ARLO)',
      timingSummary: `Operativo in fase di rifinitura e collaudo pozzetti fino al ${endFormatted} (Ord. 111/2026, feriali 08:00 - 18:00)`,
      isActiveNow: true
    };
  }

  // 1. Prima dell'inizio autorizzato dall'ordinanza (es. Cantiere 3, Cantiere 4, Ripristino Rosselli)
  if (now < start) {
    const isPlanned = cantiere.stato_base === 'planned';
    return {
      statusCode: isPlanned ? 'planned' : 'programmato',
      statusLabel: isPlanned ? 'PIANIFICATO (ORDINANZA N. 110/2026)' : 'ATTIVAZIONE PROGRAMMATA (AUTORIZZATO)',
      timingSummary: `Avvio autorizzato da ordinanza: ${startFormatted} (feriali 08:00 - 18:00)`,
      isActiveNow: false
    };
  }

  // 2. Oltre il termine stabilito dall'ordinanza
  if (now > end) {
    if (cantiere.stato_base === 'staged_for_digging') {
      return {
        statusCode: 'ordinanza_scaduta',
        statusLabel: 'ORDINANZA SCADUTA',
        timingSummary: `Termine efficacia ordinanza: ${endFormatted}`,
        isActiveNow: false
      };
    }
    if (['parziale_scaduto', 'riuso_previsto', 'non_eseguito'].includes(cantiere.stato_base)) {
      return {
        statusCode: cantiere.stato_base,
        statusLabel: 'ORDINANZA SCADUTA',
        timingSummary: `Efficacia scaduta il ${endFormatted}`,
        isActiveNow: false
      };
    }
    return {
      statusCode: 'concluso',
      statusLabel: 'ORDINANZA SCADUTA',
      timingSummary: `Termine efficacia ordinanza: ${endFormatted}`,
      isActiveNow: false
    };
  }

  // 3. All'interno del periodo di validita' dell'ordinanza (start <= now <= end)
  // Controllo giorni feriali (lunedì - sabato) vs domenica / festivo
  if (!rome.isWorkingDay) {
    return {
      statusCode: 'non_lavorativo',
      statusLabel: 'ORDINANZA IN CORSO (NON LAVORATIVO)',
      timingSummary: 'Oggi non è un giorno lavorativo (feriali 08:00 - 18:00)',
      isActiveNow: false
    };
  }

  // Controllo fascia oraria autorizzata (08:00 - 18:00)
  if (!rome.isWorkingHours) {
    return {
      statusCode: 'fuori_orario',
      statusLabel: 'ORDINANZA IN CORSO (FUORI ORARIO)',
      timingSummary: 'Fuori orario lavorativo autorizzato (feriali 08:00 - 18:00)',
      isActiveNow: false
    };
  }

  // 4. In giorno feriale e in fascia oraria lavorativa autorizzata
  return {
    statusCode: 'attivo',
    statusLabel: 'IN FASCIA ORARIA AUTORIZZATA',
    timingSummary: `Lavori autorizzati (orario feriale 08:00 - 18:00, termine autorizzazione ${endFormatted})`,
    isActiveNow: true
  };
}

function initCantieriTracker() {
  renderCantieriModal();
  updateCantieriNavbarBadge();

  // Aggiornamento live ogni minuto
  if (!window._cantieriInterval) {
    window._cantieriInterval = setInterval(() => {
      renderCantieriModal();
      updateCantieriNavbarBadge();
    }, 60000);
  }
}

function updateCantieriNavbarBadge() {
  const badgeEl = document.getElementById('cantieri-count-badge');
  if (!badgeEl) return;

  const now = getRomeCurrentDate();
  const activeOrUpcoming = ORDINANZE_DATA.filter(c => {
    const endStr = c.periodo_ordinanza ? c.periodo_ordinanza.fine : (c.fine || c.end_date);
    return new Date(endStr) >= now;
  }).length;

  badgeEl.textContent = activeOrUpcoming;
  badgeEl.title = `${activeOrUpcoming} ordinanze in corso o future`;
  badgeEl.hidden = false;
}

function renderCantieriModal() {
  const listCont = document.getElementById('cantieri-list-container');
  const clockEl = document.getElementById('cantieri-live-clock');
  if (!listCont) return;

  const now = getRomeCurrentDate();
  if (clockEl) {
    clockEl.innerText = now.toLocaleString('it-IT', {
      weekday: 'short',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: 'Europe/Rome'
    }) + ' (Europe/Rome)';
  }

  ORDINANZE_DATA.forEach((cantiere, index) => {
    const status = calculateCantiereStatus(cantiere, now);
    const timing = listCont.children[index]?.querySelector('.tracker-timing');
    if (timing) {
      timing.dataset.status = status.statusCode;
      timing.querySelector('strong').textContent = status.statusLabel;
      timing.querySelector('p').textContent = status.timingSummary;
      return;
    }

    const card = document.createElement('article');
    card.className = 'tracker-card';
    const streets = cantiere.vie_interessate || cantiere.vie || [];
    const observation = cantiere.slittamento_osservato;
    const titolo = cantiere.titolo || cantiere.nome;
    const frazione = cantiere.frazione || cantiere.localita;
    const lunghezza = cantiere.lunghezza_stimata_km ? `${cantiere.lunghezza_stimata_km} km` : cantiere.lunghezzaKm;
    const attoCodice = cantiere.codice_atto_completo || cantiere.ordinanza || 'Atto PM';
    const richiedente = cantiere.richiedente;
    const pdfPath = cantiere.file_pdf || cantiere.pdfFile;
    const centerCoords = cantiere.coordinate_centro || cantiere.centerCoords;
    const descr = cantiere.descrizione_ufficiale || cantiere.descrizione || '';

    card.innerHTML = `
      <header>
        <p class="tracker-place">📍 ${[frazione, lunghezza].filter(Boolean).join(' · ')}</p>
        <h3>${titolo}</h3>
      </header>
      <div class="tracker-timing" data-status="${status.statusCode}">
        <strong>${status.statusLabel}</strong>
        <p>${status.timingSummary}</p>
      </div>
      <p>${descr}</p>
      ${observation?.nota_campo ? `<div class="tracker-note">
        <strong>${observation.fonte_kml || 'Rilievo sul campo'}</strong>
        <p>${observation.nota_campo}</p>
      </div>` : ''}
      ${streets.length ? `<details class="tracker-streets"><summary>Vie interessate e prescrizioni (${streets.length})</summary><ul>
        ${streets.map(street => typeof street === 'string' ? `<li>${street}</li>` :
          `<li><strong>${street.via}</strong>${street.prescrizione ? ' · ' + street.prescrizione : ''}</li>`).join('')}
      </ul></details>` : ''}
      <p class="tracker-reference"><strong>${attoCodice}</strong>${richiedente ? `<br>Richiedente · ${richiedente}` : ''}</p>
      <div class="archivio-actions">
        ${centerCoords ? '<button type="button" data-tracker-map><span class="emoji" aria-hidden="true">🧭</span> Mostra sulla mappa</button>' : ''}
        ${pdfPath ? `<a href="${pdfPath}" target="_blank" rel="noopener" download><span class="emoji" aria-hidden="true">📄</span> PDF ordinanza</a>` : ''}
      </div>
    `;
    card.querySelector('[data-tracker-map]')?.addEventListener('click', () => window.flyToCantiereCoords(centerCoords));

    listCont.appendChild(card);
  });
}

window.flyToCantiereCoords = (coords) => {
  if (!window.map) return;
  document.getElementById('modal-cantieri').close();
  resetMapFilters();
  showSidebarView('map-explore');
  window.flyToFrazione(...coords);
};

window.flyToCantiere = (cantiereId) => {
  const c = ORDINANZE_DATA.find(item => item.id === cantiereId);
  if (!c) return;
  const coords = c.coordinate_centro || c.centerCoords;
  if (coords) window.flyToCantiereCoords(coords);
};

window.ORDINANZE_DATA = ORDINANZE_DATA;
window.calculateCantiereStatus = calculateCantiereStatus;
window.initCantieriTracker = initCantieriTracker;
window.renderCantieriModal = renderCantieriModal;
window.updateCantieriNavbarBadge = updateCantieriNavbarBadge;
window.getRomeTimeParts = getRomeTimeParts;
