const FRAZIONI_COORDS = {
    'Collesalvetti': [43.5884, 10.4770],
    'Vicarello': [43.6085, 10.4710],
    'Stagno': [43.5900, 10.3540],
    'Guasticce': [43.5962, 10.4068],
    'Nugola': [43.5775, 10.4383],
    'Parrana San Martino': [43.5382, 10.4423],
    'Parrana San Giusto': [43.5285, 10.4573]
};

function updateTelemetry(features) {
    // I conteggi degli apparati provengono da data/stats.json (js/stats.js), generato da
    // scripts/compute_stats.py: nessun valore e' calcolato o scritto a mano qui.
    const stats = window.FTTH_STATS;
    if (!stats) {
        console.error('FTTH_STATS non disponibile: esegui scripts/compute_stats.py');
    }
    const eq = stats ? stats.equipment : null;
    const km = stats ? stats.length_km.total : 0;
    let cantieri = 0;
    let frazCounts = {};

    features.forEach(f => {
        if (f.properties.category.includes('cantiere')) cantieri++;
    });

    if (eq) {
        Object.keys(eq.by_frazione_municipal).forEach(fr => {
            frazCounts[fr] = eq.by_frazione_municipal[fr].totale;
        });
    }

    const elTot = document.getElementById('stat-tot');
    const elKm = document.getElementById('stat-km');
    const elArl = document.getElementById('stat-arl');
    const elArlo = document.getElementById('stat-arlo');
    const elCentrali = document.getElementById('stat-centrali');
    const elCantieri = document.getElementById('stat-cantieri');

    if (eq) {
        if (elTot) elTot.innerText = eq.total_municipal;
        if (elKm) elKm.innerText = km.toFixed(2);
        if (elArl) elArl.innerText = eq.by_category_municipal.arl || 0;
        if (elArlo) elArlo.innerText = eq.by_category_municipal.arlo || 0;
        if (elCentrali) elCentrali.innerText = eq.centrali_municipal;
    }
    if (elCantieri) elCantieri.innerText = cantieri;

    const navCont = document.getElementById('frazioni-nav');
    const statsCont = document.getElementById('frazioni-stats');
    if (navCont) navCont.innerHTML = '';
    if (statsCont) statsCont.innerHTML = '';

    // Ordine di visualizzazione prioritario delle frazioni
    const sortedFrazioni = Object.keys(frazCounts).sort((a, b) => frazCounts[b] - frazCounts[a]);

    sortedFrazioni.forEach(fr => {
        if (navCont && FRAZIONI_COORDS[fr]) {
            const btn = document.createElement('button');
            btn.className = "px-2.5 py-1 text-xs md:text-sm bg-white/5 hover:bg-white/15 rounded-full border border-cyber-border/50 transition-colors text-slate-300 whitespace-nowrap";
            btn.innerText = fr;
            btn.onclick = () => window.flyToFrazione(FRAZIONI_COORDS[fr][0], FRAZIONI_COORDS[fr][1]);
            navCont.appendChild(btn);
        }

        if (statsCont) {
            const maxF = Math.max(...Object.values(frazCounts));
            const pct = (frazCounts[fr] / maxF) * 100;
            
            statsCont.innerHTML += `
                <div class="mb-2">
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-white">${fr}</span>
                        <span class="text-cyber-neon font-bold">${frazCounts[fr]} app.</span>
                    </div>
                    <div class="w-full bg-black/40 rounded-full h-1.5">
                        <div class="bg-cyber-neon h-1.5 rounded-full" style="width: ${pct}%"></div>
                    </div>
                </div>
            `;
        }
    });

    renderList(features);
    
    const searchInput = document.getElementById('search-elements');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = features.filter(f => f.properties.name.toLowerCase().includes(term) || f.properties.category.includes(term) || (f.properties.frazione && f.properties.frazione.toLowerCase().includes(term)));
            renderList(filtered);
        });
    }
}

function renderList(features) {
    const listCont = document.getElementById('elements-list');
    if (!listCont) return;
    listCont.innerHTML = '';
    
    features.forEach(f => {
        const p = f.properties;
        const item = document.createElement('div');
        item.className = "flex items-center justify-between p-2 hover:bg-white/10 rounded cursor-pointer transition-colors border-b border-white/5 last:border-0";
        item.innerHTML = `
            <div class="flex items-center gap-2 overflow-hidden">
                <div class="w-2 h-2 rounded-full flex-shrink-0" style="background: ${p.color}; box-shadow: 0 0 5px ${p.color}"></div>
                <div class="text-sm text-slate-200 truncate" title="${p.name}">${p.name}</div>
            </div>
            <div class="text-xs text-slate-400 font-medium ml-2 flex-shrink-0">${p.frazione || ''}</div>
        `;
        item.onclick = () => {
            if (f.geometry.type === 'Point') {
                window.flyToFrazione(f.geometry.coordinates[1], f.geometry.coordinates[0]);
                if (geojsonLayer) {
                    geojsonLayer.eachLayer(layer => {
                        if (layer.feature && layer.feature.id === f.id) {
                            layer.openPopup();
                        }
                    });
                }
            } else if (f.geometry.type === 'LineString' || f.geometry.type === 'Polygon') {
                let pts = f.geometry.type === 'LineString' ? f.geometry.coordinates : f.geometry.coordinates[0];
                if(pts && pts.length > 0) {
                    window.flyToFrazione(pts[0][1], pts[0][0]);
                }
            }
        };
        listCont.appendChild(item);
    });
}

window.updateTelemetry = updateTelemetry;
