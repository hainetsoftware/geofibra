// js/cantieri_tracker.js - Monitoraggio Cantieri e Ordinanze Albo Pretorio Comune di Collesalvetti
// Fuso Orario di Riferimento: Europe/Rome

// Dati ufficiali estratti da data/ordinanze.json (fonte unica di verita')
const ORDINANZE_DATA_DEFAULT = [
  {
    "id": "cantiere-2-stagno",
    "titolo": "Cantiere 2 - Stagno (Nuova Espansione FTTH)",
    "frazione": "Stagno",
    "richiedente": "Fastweb S.p.A. per rete FTTH FiberCop",
    "oggetto": "Lavori di scavo stradale per posa infrastruttura rete FTTH FiberCop – Stagno, vie varie",
    "atto_tipo": "Polizia Municipale",
    "atto_numero": "95",
    "atto_registro_generale": "102",
    "codice_atto_completo": "Ordinanza P.M. n. 95 del 10/09/2026 (Reg. Gen. 102)",
    "data_emissione": "2026-09-10",
    "autorizzazione_settore_tecnico": "Autorizzazione n. 17/2026 del 16/07/2026",
    "periodo_ordinanza": {
      "inizio": "2026-09-21T08:00:00+02:00",
      "fine": "2026-10-16T18:00:00+02:00",
      "fascia_oraria": "08:00 - 18:00",
      "giorni": "feriali"
    },
    "slittamento_osservato": {
      "fonte_kml": "Snapshot 3 (04/10/2026) - campo name 'Cantiere 2 (05/10-17/10)' e description",
      "inizio_stimato": "2026-10-05T08:00:00+02:00",
      "fine_stimata": "2026-10-17T18:00:00+02:00",
      "nota_campo": "Slittamento rilevato sul campo: avvio posticipato al 05/10/2026"
    },
    "lunghezza_stimata_km": 1.43,
    "vie_interessate": [
      { "via": "Via Otto Marzo", "prescrizione": "Divieto di sosta con rimozione e senso unico alternato con movieri o a vista" },
      { "via": "Via Romita", "prescrizione": "Divieto di sosta e senso unico alternato con movieri (o mantenimento senso unico)" },
      { "via": "Via De Gasperi", "prescrizione": "Divieto di sosta e senso unico alternato regolato da movieri o semaforo" },
      { "via": "Via Machiavelli", "prescrizione": "Mantenimento senso unico con divieto di sosta ambo i lati" },
      { "via": "Via XXV Aprile", "prescrizione": "Mantenimento senso unico con divieto di sosta ambo i lati" },
      { "via": "Piazza Di Vittorio", "prescrizione": "Divieto di sosta e senso unico alternato regolato a vista o movieri" }
    ],
    "file_pdf": "ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf",
    "coordinate_centro": [43.5930, 10.3540],
    "descrizione_ufficiale": "Provvedimento di disciplina temporanea della viabilita per esecuzione di scavi stradali per posa della rete in fibra ottica FiberCop a Stagno."
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
      "fonte_kml": "Snapshot 3 (04/10/2026) - suddivisione tratte ESEGUITO / NON ESEGUITO",
      "inizio_stimato": "2026-09-14T08:00:00+02:00",
      "fine_stimata": "2026-10-02T18:00:00+02:00",
      "nota_campo": "Rilievo del 29/09/2026 e 03/10/2026: 2 tratte eseguite (Via Nenni/rotatoria con minitrincee e pozzetti), 5 tratte non eseguite (solo segni blu sull'asfalto)"
    },
    "lunghezza_stimata_km": 2.60,
    "vie_interessate": [
      { "via": "Via Nenni", "prescrizione": "Divieto di sosta ambo i lati con rimozione e restringimento carreggiata con mantenimento senso unico" },
      { "via": "Via Roma (altezza rotatoria Via Nenni)", "prescrizione": "Divieto di sosta e senso unico alternato a vista o con movieri" },
      { "via": "Via del Valico a Pisa", "prescrizione": "Divieto di sosta e senso unico alternato a vista o con movieri" },
      { "via": "Via di Cerretello", "prescrizione": "Divieto di sosta e senso unico alternato a vista o con movieri" }
    ],
    "file_pdf": "ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf",
    "coordinate_centro": [43.5945, 10.4760],
    "descrizione_ufficiale": "Provvedimento di disciplina della viabilita per scavo e posa infrastruttura in fibra ottica FiberCop nel centro abitato di Collesalvetti."
  },
  {
    "id": "ripristino-stagno",
    "titolo": "Lavori di Ripristino Manto Stradale Scavi Fibra - Stagno",
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
    "file_pdf": "ordinanze/ordinanza_75_2026_stagno_ripristino.pdf",
    "coordinate_centro": [43.5910, 10.3520],
    "descrizione_ufficiale": "Provvedimento straordinario di circolazione per esecuzione di ripristini del manto stradale a seguito degli scavi per la fibra ottica a Stagno. Lavori formalmente conclusi."
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
 * Risolve specificamente il bug che segnava "CANTIERE ATTIVO ORA" di domenica o fuori orario.
 */
function calculateCantiereStatus(cantiere, currentDate) {
  const now = currentDate || getRomeCurrentDate();
  const rome = getRomeTimeParts(now);

  // Normalizza date di inizio e fine dell'ordinanza
  const inizioStr = cantiere.periodo_ordinanza ? cantiere.periodo_ordinanza.inizio : (cantiere.inizio || cantiere.inizio_lavori);
  const fineStr = cantiere.periodo_ordinanza ? cantiere.periodo_ordinanza.fine : (cantiere.fine || cantiere.fine_lavori);

  const start = new Date(inizioStr);
  const end = new Date(fineStr);

  const startFormatted = start.toLocaleDateString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'Europe/Rome'
  });
  const endFormatted = end.toLocaleDateString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'Europe/Rome'
  });

  // 1. Prima dell'inizio autorizzato dall'ordinanza
  if (now < start) {
    return {
      statusCode: 'programmato',
      statusLabel: 'ATTIVAZIONE PROGRAMMATA',
      badgeClass: 'bg-amber-500/20 text-amber-400 border border-amber-500/40',
      dotClass: 'bg-amber-400 animate-pulse',
      timingSummary: `Avvio autorizzato da ordinanza: ${startFormatted} (feriali 08:00 - 18:00)`,
      isActiveNow: false
    };
  }

  // 2. Oltre il termine stabilito dall'ordinanza
  if (now > end) {
    return {
      statusCode: 'concluso',
      statusLabel: 'LAVORI COMPLETATI (DA ORDINANZA)',
      badgeClass: 'bg-slate-500/20 text-slate-400 border border-slate-500/40',
      dotClass: 'bg-slate-500',
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
      badgeClass: 'bg-amber-500/20 text-amber-300 border border-amber-500/40',
      dotClass: 'bg-amber-400',
      timingSummary: 'Oggi non è un giorno lavorativo (feriali 08:00 - 18:00)',
      isActiveNow: false
    };
  }

  // Controllo fascia oraria autorizzata (08:00 - 18:00)
  if (!rome.isWorkingHours) {
    return {
      statusCode: 'fuori_orario',
      statusLabel: 'ORDINANZA IN CORSO (FUORI ORARIO)',
      badgeClass: 'bg-blue-500/20 text-blue-300 border border-blue-500/40',
      dotClass: 'bg-blue-400',
      timingSummary: 'Fuori orario lavorativo autorizzato (feriali 08:00 - 18:00)',
      isActiveNow: false
    };
  }

  // 4. In giorno feriale e in fascia oraria lavorativa autorizzata
  return {
    statusCode: 'attivo',
    statusLabel: 'CANTIERE ATTIVO ORA',
    badgeClass: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40',
    dotClass: 'bg-emerald-400 animate-ping',
    timingSummary: `Cantiere operativo sul campo (orario feriale 08:00 - 18:00, termine autorizzazione ${endFormatted})`,
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
    const endStr = c.periodo_ordinanza ? c.periodo_ordinanza.fine : c.fine;
    return new Date(endStr) >= now;
  }).length;

  badgeEl.innerText = `${activeOrUpcoming} ordinanze in corso/future`;
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

  listCont.innerHTML = '';

  ORDINANZE_DATA.forEach(cantiere => {
    const status = calculateCantiereStatus(cantiere, now);

    const card = document.createElement('div');
    card.className = "glass-panel border border-cyber-border/50 rounded-xl p-5 hover:border-cyber-neon/50 transition-all flex flex-col justify-between";

    // Format vie con prescrizioni
    let vieHtml = '';
    if (Array.isArray(cantiere.vie_interessate)) {
      vieHtml = cantiere.vie_interessate.map(v => {
        if (typeof v === 'string') {
          return `<li class="flex items-start gap-1.5 text-xs text-slate-200"><span class="text-cyber-neon">•</span> <span>${v}</span></li>`;
        }
        return `<li class="flex items-start gap-1.5 text-xs text-slate-200"><span class="text-cyber-neon">•</span> <span><b class="text-white">${v.via}</b>${v.prescrizione ? ': ' + v.prescrizione : ''}</span></li>`;
      }).join('');
    } else if (Array.isArray(cantiere.vie)) {
      vieHtml = cantiere.vie.map(v => `<li class="flex items-start gap-1.5 text-xs text-slate-200"><span class="text-cyber-neon">•</span> <span>${v}</span></li>`).join('');
    }

    // Blocco note di rilievo / slittamento (distinto dall'ordinanza ufficiale)
    let slittamentoHtml = '';
    if (cantiere.slittamento_osservato && cantiere.slittamento_osservato.nota_campo) {
      slittamentoHtml = `
        <div class="bg-amber-500/10 border border-amber-500/30 rounded-lg p-2.5 mb-3 text-xs">
          <div class="flex items-center gap-1.5 font-bold text-amber-300 mb-1">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            Rilievo sul Campo (Osservazione Civica):
          </div>
          <p class="text-amber-200/90">${cantiere.slittamento_osservato.nota_campo}</p>
        </div>
      `;
    }

    const titolo = cantiere.titolo || cantiere.nome;
    const frazione = cantiere.frazione || cantiere.localita;
    const lunghezza = cantiere.lunghezza_stimata_km ? `${cantiere.lunghezza_stimata_km} km` : (cantiere.lunghezzaKm || 'N.D.');
    const attoCodice = cantiere.codice_atto_completo || cantiere.ordinanza || 'Atto PM';
    const richiedente = cantiere.richiedente || 'N.D.';
    const pdfPath = cantiere.file_pdf || cantiere.pdfFile || '#';
    const centerCoords = cantiere.coordinate_centro || cantiere.centerCoords || [43.59, 10.45];
    const descr = cantiere.descrizione_ufficiale || cantiere.descrizione || '';

    card.innerHTML = `
      <div>
        <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full ${status.dotClass}"></span>
            <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded ${status.badgeClass}">
              ${status.statusLabel}
            </span>
            <span class="text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded border border-white/10">📍 ${frazione}</span>
          </div>
          <div class="text-xs font-mono text-slate-400">Estensione: <b class="text-white">${lunghezza}</b></div>
        </div>

        <h4 class="text-lg font-['Rajdhani'] font-bold text-white mb-1">${titolo}</h4>
        <div class="text-xs text-cyber-neon font-mono mb-2">${status.timingSummary}</div>
        <p class="text-xs text-slate-300 mb-3">${descr}</p>

        ${slittamentoHtml}

        <div class="bg-black/30 p-3 rounded-lg border border-white/5 mb-3">
          <div class="text-[11px] uppercase tracking-wider font-bold text-slate-400 mb-1.5">
            Vie Interessate e Prescrizioni Traffico:
          </div>
          <ul class="space-y-1">
            ${vieHtml}
          </ul>
        </div>
      </div>

      <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-white/10 text-xs mt-2">
        <div class="text-slate-400">
          Atto Ufficiale: <b class="text-slate-200">${attoCodice}</b><br>
          <span class="text-[11px] text-slate-500">Richiedente: ${richiedente}</span>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="window.flyToCantiereCoords([${centerCoords[0]}, ${centerCoords[1]}])" class="px-3 py-1.5 bg-cyber-neon/20 hover:bg-cyber-neon/30 text-cyber-neon border border-cyber-neon/50 rounded text-xs font-bold flex items-center gap-1.5 transition-colors">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg> Mostra su Mappa
          </button>
          <a href="${pdfPath}" target="_blank" download class="px-3 py-1.5 bg-white/10 hover:bg-white/20 text-white border border-white/20 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> PDF Ordinanza
          </a>
        </div>
      </div>
    `;

    listCont.appendChild(card);
  });
}

window.flyToCantiereCoords = (coords) => {
  if (!window.map) return;
  const modal = document.getElementById('modal-cantieri');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
  window.map.flyTo(coords, 16, { duration: 1.8 });
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
