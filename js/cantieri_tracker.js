// js/cantieri_tracker.js - Monitoraggio Cantieri e Ordinanze Albo Pretorio Comune di Collesalvetti
// Fuso Orario: Europe/Rome

const ORDINANZE_DATA = [
    {
        id: 'cantiere-2-stagno',
        nome: 'Cantiere 2 - Stagno (Nuova Espansione FTTH)',
        localita: 'Stagno',
        categoria: 'FTTH FiberCop',
        richiedente: 'Fastweb S.p.A. per rete FTTH FiberCop',
        ordinanza: 'Ordinanza P.M. N. 95 del 10/09/2026 (Reg. Gen. 102)',
        dataEmissione: '10/09/2026 (Rilasciata Oggi!)',
        inizio: '2026-09-21T08:00:00+02:00',
        fine: '2026-10-16T18:00:00+02:00',
        fasciaOraria: '08:00 - 18:00 (giorni feriali)',
        lunghezzaKm: '1.43 km',
        vie: [
            'Via Otto Marzo (divieto di sosta e senso unico alternato)',
            'Via Romita (divieto di sosta e senso unico alternato)',
            'Via De Gasperi (senso unico alternato con semaforo o movieri)',
            'Via Machiavelli (mantenimento senso unico con divieto di sosta)',
            'Via XXV Aprile (mantenimento senso unico con divieto di sosta)',
            'Piazza Di Vittorio (senso unico alternato / divieto di sosta)'
        ],
        centerCoords: [43.5930, 10.3540],
        pdfFile: 'ordinanze/ordinanza_102_2026_stagno_cantiere2.pdf',
        descrizione: 'Nuova ordinanza pubblicata sull\'Albo Pretorio di Collesalvetti che autorizza lo scavo stradale per la posa dell\'infrastruttura FTTH FiberCop a Stagno, espandendo significativamente l\'area coperta.'
    },
    {
        id: 'cantiere-1-collesalvetti',
        nome: 'Cantiere 1 - Collesalvetti Centro',
        localita: 'Collesalvetti',
        categoria: 'FTTH FiberCop',
        richiedente: 'Fastweb S.p.A. per rete FTTH FiberCop',
        ordinanza: 'Ordinanza P.M. N. 88 del 02/09/2026 (Reg. Gen. 95)',
        dataEmissione: '02/09/2026',
        inizio: '2026-09-14T08:00:00+02:00',
        fine: '2026-10-02T18:00:00+02:00',
        fasciaOraria: '08:00 - 18:00 (giorni feriali)',
        lunghezzaKm: '2.67 km',
        vie: [
            'Via Nenni (divieto sosta e restringimento carreggiata)',
            'Via Roma (altezza rotatoria Via Nenni - senso unico alternato)',
            'Via del Valico a Pisa (divieto sosta e senso unico alternato)',
            'Via di Cerretello (divieto sosta e senso unico alternato)'
        ],
        centerCoords: [43.5945, 10.4760],
        pdfFile: 'ordinanze/ordinanza_95_2026_collesalvetti_cantiere1.pdf',
        descrizione: 'Lavori di scavo stradale per posa della dorsale primaria e secondaria FTTH FiberCop nel centro abitato di Collesalvetti.'
    },
    {
        id: 'ripristino-stagno',
        nome: 'Lavori di Ripristino Scavi Fibra - Stagno',
        localita: 'Stagno',
        categoria: 'Ripristino Asfalti',
        richiedente: 'Fastweb S.p.A.',
        ordinanza: 'Ordinanza P.M. N. 70 del 16/07/2026 (Reg. Gen. 75)',
        dataEmissione: '16/07/2026',
        inizio: '2026-08-03T08:00:00+02:00',
        fine: '2026-08-13T18:00:00+02:00',
        fasciaOraria: '08:00 - 18:00',
        lunghezzaKm: '0.85 km',
        vie: [
            'Via Marx (lato opposto accesso Chiesa San Luca)',
            'Via Marx (altezza ponte Fosso Cateratto, lato nord)',
            'Via Guerrazzi (intersezione con Via Curiel, lato sud)',
            'Via La Malfa'
        ],
        centerCoords: [43.5910, 10.3520],
        pdfFile: 'ordinanze/ordinanza_75_2026_stagno_ripristino.pdf',
        descrizione: 'Completamento e riasfaltatura definitiva degli scavi per la fibra ottica a Stagno.'
    }
];

function getRomeCurrentDate() {
    // Restituisce la data attuale forzata nel fuso orario Europe/Rome
    const now = new Date();
    return now;
}

function calculateCantiereStatus(cantiere, currentDate) {
    const start = new Date(cantiere.inizio);
    const end = new Date(cantiere.fine);
    const now = currentDate || getRomeCurrentDate();

    if (now < start) {
        const diffMs = start - now;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        
        let timeMsg = "";
        if (diffDays > 0) {
            timeMsg = `Tra ${diffDays} giorn${diffDays === 1 ? 'o' : 'i'} e ${diffHours} or${diffHours === 1 ? 'a' : 'e'}`;
        } else {
            timeMsg = `Tra ${diffHours} or${diffHours === 1 ? 'a' : 'e'}`;
        }

        const dateStr = start.toLocaleDateString('it-IT', { 
            weekday: 'long', 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'Europe/Rome'
        });

        return {
            statusCode: 'programmato',
            statusLabel: 'ATTIVAZIONE PROGRAMMATA',
            badgeClass: 'bg-amber-500/20 text-amber-400 border border-amber-500/40',
            dotClass: 'bg-amber-400 animate-pulse',
            timingSummary: `Si attiverà: ${dateStr} (${timeMsg})`,
            isActiveNow: false
        };
    } else if (now >= start && now <= end) {
        const endStr = end.toLocaleDateString('it-IT', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'Europe/Rome'
        });

        return {
            statusCode: 'attivo',
            statusLabel: 'CANTIERE ATTIVO ORA',
            badgeClass: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40',
            dotClass: 'bg-emerald-400 animate-ping',
            timingSummary: `Attivo sul campo fino al ${endStr} (${cantiere.fasciaOraria})`,
            isActiveNow: true
        };
    } else {
        const endStr = end.toLocaleDateString('it-IT', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric',
            timeZone: 'Europe/Rome'
        });

        return {
            statusCode: 'concluso',
            statusLabel: 'LAVORI COMPLETATI',
            badgeClass: 'bg-slate-500/20 text-slate-400 border border-slate-500/40',
            dotClass: 'bg-slate-500',
            timingSummary: `Lavori stradali conclusi il ${endStr}`,
            isActiveNow: false
        };
    }
}

function initCantieriTracker() {
    renderCantieriModal();
    updateCantieriNavbarBadge();

    // Aggiornamento live ogni minuto
    setInterval(() => {
        renderCantieriModal();
        updateCantieriNavbarBadge();
    }, 60000);
}

function updateCantieriNavbarBadge() {
    const badgeEl = document.getElementById('cantieri-count-badge');
    if (!badgeEl) return;
    
    const now = getRomeCurrentDate();
    const activeOrUpcoming = ORDINANZE_DATA.filter(c => new Date(c.fine) >= now).length;
    badgeEl.innerText = `${activeOrUpcoming} programmati / attivi`;
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
        card.className = "glass-panel border border-cyber-border/50 rounded-xl p-5 hover:border-cyber-neon/50 transition-all";
        
        let vieHtml = cantiere.vie.map(v => `<li class="flex items-start gap-1.5 text-xs text-slate-200"><span class="text-cyber-neon">•</span> <span>${v}</span></li>`).join('');

        card.innerHTML = `
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full ${status.dotClass}"></span>
                    <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded ${status.badgeClass}">
                        ${status.statusLabel}
                    </span>
                    <span class="text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded border border-white/10">📍 ${cantiere.localita}</span>
                </div>
                <div class="text-xs font-mono text-slate-400">Tratta: <b class="text-white">${cantiere.lunghezzaKm}</b></div>
            </div>

            <h4 class="text-lg font-['Rajdhani'] font-bold text-white mb-1">${cantiere.nome}</h4>
            <div class="text-xs text-cyber-neon font-mono mb-2">${status.timingSummary}</div>
            <p class="text-xs text-slate-300 mb-3">${cantiere.descrizione}</p>

            <div class="bg-black/30 p-3 rounded-lg border border-white/5 mb-3">
                <div class="text-[11px] uppercase tracking-wider font-bold text-slate-400 mb-1.5">
                    Vie Interessate da Ordinanza:
                </div>
                <ul class="space-y-1">
                    ${vieHtml}
                </ul>
            </div>

            <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-white/10 text-xs">
                <div class="text-slate-400">
                    Fonte Ufficiale: <b class="text-slate-200">${cantiere.ordinanza}</b>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="window.flyToCantiere('${cantiere.id}')" class="px-3 py-1.5 bg-cyber-neon/20 hover:bg-cyber-neon/30 text-cyber-neon border border-cyber-neon/50 rounded text-xs font-bold flex items-center gap-1.5 transition-colors">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg> Mostra su Mappa
                    </button>
                    <a href="${cantiere.pdfFile}" target="_blank" download class="px-3 py-1.5 bg-white/10 hover:bg-white/20 text-white border border-white/20 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> PDF Ordinanza
                    </a>
                </div>
            </div>
        `;

        listCont.appendChild(card);
    });
}

window.flyToCantiere = (cantiereId) => {
    const c = ORDINANZE_DATA.find(item => item.id === cantiereId);
    if (!c || !window.map) return;

    // Chiudi il modale cantieri
    const modal = document.getElementById('modal-cantieri');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }

    window.map.flyTo(c.centerCoords, 16, { duration: 1.8 });
};

window.ORDINANZE_DATA = ORDINANZE_DATA;
window.calculateCantiereStatus = calculateCantiereStatus;
window.initCantieriTracker = initCantieriTracker;
