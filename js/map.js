let map;
let geojsonLayer;
let currentCantiereFilter = 'all';

// Limiti geografici della Toscana (Sud-Ovest e Nord-Est)
const TOSCANA_BOUNDS = L.latLngBounds(
    [42.15, 9.55], // Maremma sud / Arcipelago
    [44.55, 12.45]  // Lunigiana / Appennino / confini est
);

function getIconHtml(iconName, color) {
    let svg = '';
    if (iconName === 'copper-cabinet') {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="6" width="16" height="16" rx="2" ry="2"></rect><path d="M4 6L12 2L20 6"></path><line x1="12" y1="11" x2="12" y2="17"></line></svg>`;
    } else if (iconName === 'optical-cabinet') {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2" ry="2"></rect><circle cx="12" cy="12" r="3"></circle><line x1="12" y1="3" x2="12" y2="6"></line></svg>`;
    } else if (iconName === 'building-tower') {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="14" rx="2" ry="2"></rect><path d="M12 10V2"></path><path d="M8 6h8"></path></svg>`;
    } else if (iconName === 'building-small') {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="16" rx="2" ry="2"></rect><path d="M4 8l8-6 8 6"></path></svg>`;
    } else {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
    }
    
    return `<div class="pulse-marker" style="color: ${color}; background: rgba(10, 13, 20, 0.9); border: 1.5px solid ${color}; border-radius: 50%; padding: 3px; box-shadow: 0 0 8px ${color}66;">${svg}</div>`;
}

function initMap() {
    const center = [43.5884, 10.4770];
    
    map = L.map('map', {
        zoomControl: false,
        attributionControl: true,
        maxBounds: TOSCANA_BOUNDS,
        maxBoundsViscosity: 1.0,
        minZoom: 9,
        maxZoom: 19
    }).setView(center, 15);

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Layer 1: Cyber Dark (Esri Dark Canvas)
    const darkBase = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', { 
        maxZoom: 19,
        bounds: TOSCANA_BOUNDS,
        attribution: 'Tiles &copy; Esri'
    });
    const darkRef = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', { 
        maxZoom: 19,
        bounds: TOSCANA_BOUNDS
    });
    const darkGroup = L.layerGroup([darkBase, darkRef]);

    // Layer 2: Satellite HD (Esri World Imagery)
    const satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { 
        maxZoom: 19,
        bounds: TOSCANA_BOUNDS,
        attribution: 'Tiles &copy; Esri'
    });

    // Layer 3: Topografico OpenStreetMap
    const topoLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
        maxZoom: 19,
        subdomains: ['a', 'b', 'c'],
        bounds: TOSCANA_BOUNDS,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors'
    });

    const layers = {
        dark: darkGroup,
        satellite: satLayer,
        topo: topoLayer
    };

    topoLayer.addTo(map);

    document.querySelectorAll('.layer-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.layer-btn').forEach(b => b.classList.remove('active-layer'));
            e.target.classList.add('active-layer');
            const l = e.target.dataset.layer;
            
            Object.values(layers).forEach(layer => map.removeLayer(layer));
            layers[l].addTo(map);
        });
    });

    loadData();
    initLegendFilters();
}

function featureMatchesFilter(feature, filter) {
    if (!filter || filter === 'all') return true;
    const p = feature.properties;
    const s = p.status || '';
    const cat = p.category || '';
    const nameLower = (p.name || '').toLowerCase();

    // Se stiamo filtrando i cantieri, gli elementi non-cantiere (es. coperture, scuole, sanità) restano visibili solo se 'all'
    if (filter === 'completati') {
        return s === 'completato' || cat === 'cantiere_eseguito' || nameLower.includes('eseguito') || nameLower.includes('aggiunto');
    }
    if (filter === 'in_completamento') {
        return s === 'in_completamento' || (cat.includes('cantiere') && (nameLower.includes('cantiere 2') && !nameLower.includes('eseguito')));
    }
    if (filter === 'autorizzati') {
        return s === 'autorizzato' || s === 'planned' || (cat.includes('cantiere') && (nameLower.includes('cantiere 3') || nameLower.includes('cantiere 4')));
    }
    if (filter === 'in_attesa_proroga') {
        return s === 'in_attesa_proroga' || cat === 'cantiere_non_eseguito' || nameLower.includes('non eseguito');
    }
    return true;
}

function loadData() {
    if (!window.FTTH_NETWORK_DATA) return;
    
    if (geojsonLayer) {
        map.removeLayer(geojsonLayer);
    }

    geojsonLayer = L.geoJSON(window.FTTH_NETWORK_DATA, {
        filter: function(feature) {
            return featureMatchesFilter(feature, currentCantiereFilter);
        },
        pointToLayer: function (feature, latlng) {
            const props = feature.properties;
            const icon = L.divIcon({
                className: 'custom-div-icon',
                html: getIconHtml(props.icon, props.color),
                iconSize: [26, 26],
                iconAnchor: [13, 13]
            });
            return L.marker(latlng, { icon: icon });
        },
        style: function (feature) {
            const props = feature.properties;
            if (feature.geometry.type === 'LineString') {
                return {
                    color: props.color,
                    weight: 4,
                    opacity: 0.95,
                    className: 'neon-path'
                };
            }
            if (feature.geometry.type === 'Polygon') {
                return {
                    color: props.color,
                    weight: 2,
                    opacity: 1,
                    fillColor: props.color,
                    fillOpacity: 0.22
                };
            }
        },
        onEachFeature: function (feature, layer) {
            const props = feature.properties;
            
            // Badge di stato stilizzato
            let statusBadge = '';
            if (props.status_label) {
                let badgeBg = 'bg-blue-500/20 text-blue-300 border-blue-500/40';
                if (props.status === 'completato') badgeBg = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50';
                else if (props.status === 'in_completamento') badgeBg = 'bg-amber-500/20 text-amber-300 border-amber-500/50';
                else if (props.status === 'autorizzato') badgeBg = 'bg-amber-500/20 text-amber-400 border-amber-500/50';
                else if (props.status === 'planned') badgeBg = 'bg-orange-500/20 text-orange-400 border-orange-500/50';
                else if (props.status === 'in_attesa_proroga') badgeBg = 'bg-orange-500/20 text-orange-300 border-orange-500/50';
                else if (props.status === 'installato') badgeBg = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50';
                else if (props.status === 'infrastrutturato') badgeBg = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50';

                statusBadge = `
                    <div class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-bold border ${badgeBg} mb-2">
                        <span class="w-1.5 h-1.5 rounded-full bg-current animate-pulse"></span>
                        ${props.status_label}
                    </div>
                `;
            }

            let tagsHtml = `
                <div class="flex flex-wrap items-center gap-1.5 my-2 text-[10px]">
                    <span class="px-2 py-0.5 rounded bg-white/10 text-slate-300 border border-white/10">🏢 ${props.operatore || 'FiberCop'}</span>
                    <span class="px-2 py-0.5 rounded bg-white/10 text-slate-300 border border-white/10">📅 Rilievo: ${props.data_rilevamento || '2026-10-17'}</span>
                    ${props.ordinanza ? `<span class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">📋 ${props.ordinanza}</span>` : ''}
                </div>
            `;

            let popupContent = `
                <div>
                    <div class="flex items-center justify-between gap-2 mb-1">
                        <span class="badge" style="background: ${props.color}33; color: ${props.color}; border: 1px solid ${props.color}">${props.category.replace('_', ' ')}</span>
                        <span class="text-xs text-slate-400 font-mono">📍 ${props.frazione}</span>
                    </div>
                    <h3>${props.name}</h3>
                    ${statusBadge}
                    ${tagsHtml}
            `;
            
            if (props.description) {
                popupContent += `<div class="notes border-l-2 pl-2 text-xs leading-relaxed" style="border-color: ${props.color}">${props.description}</div>`;
            }
            
            if (props.length_m > 0) popupContent += `<div class="text-xs text-slate-300 mt-2">📏 Tratta: <b class="text-white">${props.length_m} m</b> (${props.length_km} km)</div>`;
            if (props.area_m2 > 0) popupContent += `<div class="text-xs text-slate-300 mt-2">📐 Superficie: <b class="text-white">${props.area_km2} km²</b> (${props.area_m2} m²)</div>`;
            
            // Dettagli dinamici cantiere Albo Pretorio
            if (props.cantiere) {
                const cInfo = props.cantiere;
                let statusInfo = null;
                if (window.calculateCantiereStatus) {
                    statusInfo = window.calculateCantiereStatus({
                        inizio: cInfo.inizio_lavori,
                        fine: cInfo.fine_lavori,
                        stato_base: cInfo.stato_base,
                        fasciaOraria: cInfo.orario_giornaliero
                    });
                }
                popupContent += `
                    <div class="mt-3 pt-2 border-t border-white/10 text-xs">
                        <div class="flex items-center gap-1.5 mb-1.5">
                            <span class="w-2 h-2 rounded-full ${statusInfo ? statusInfo.dotClass : 'bg-amber-400'}"></span>
                            <span class="font-bold px-2 py-0.5 rounded text-[11px] ${statusInfo ? statusInfo.badgeClass : 'bg-amber-500/20 text-amber-400 border border-amber-500/40'}">
                                ${statusInfo ? statusInfo.statusLabel : 'CANTIERE'}
                            </span>
                        </div>
                        <div class="text-[11px] text-cyber-neon font-mono mb-2">${statusInfo ? statusInfo.timingSummary : ''}</div>
                        <div class="text-slate-400 text-[11px] mb-1">📋 Ordinanza: <b class="text-white">${cInfo.codice_ordinanza}</b></div>
                        <div class="text-slate-400 text-[11px] mb-2">🏢 Richiedente: <b class="text-slate-200">${cInfo.richiedente}</b></div>
                        ${cInfo.vie_interessate && cInfo.vie_interessate.length ? `
                        <div class="bg-black/40 p-2 rounded border border-white/10 mb-2">
                            <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Vie Autorizzate:</div>
                            <ul class="list-disc list-inside space-y-0.5 text-slate-300 text-[11px]">
                                ${cInfo.vie_interessate.map(v => `<li>${v}</li>`).join('')}
                            </ul>
                        </div>` : ''}
                        ${cInfo.file_pdf ? `
                        <a href="${cInfo.file_pdf}" target="_blank" download class="w-full bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/50 text-amber-300 py-1.5 px-2 rounded text-xs font-bold flex items-center justify-center gap-1.5 transition-colors mb-2">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Scarica PDF Ordinanza Ufficiale
                        </a>` : ''}
                    </div>
                `;
            }

            let mapsTarget = feature.geometry.type === 'Point' ? `${feature.geometry.coordinates[1]},${feature.geometry.coordinates[0]}` : '';
            
            popupContent += `
                    <div class="mt-3 flex gap-2">
                        `;
            if (mapsTarget) {
                popupContent += `<a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${mapsTarget}" target="_blank" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-1 px-2 rounded text-xs text-center border border-white/20 transition-colors flex items-center justify-center gap-1">Street View</a>`;
            }
            popupContent += `</div></div>`;
            
            layer.bindPopup(popupContent, { minWidth: 280, maxWidth: 350 });
        }
    }).addTo(map);
    
    // Filtra la lista elementi nella telemetria se applicato
    if (window.FTTH_NETWORK_DATA && window.FTTH_NETWORK_DATA.features) {
        const filteredFeatures = window.FTTH_NETWORK_DATA.features.filter(f => featureMatchesFilter(f, currentCantiereFilter));
        if (window.updateTelemetry) window.updateTelemetry(filteredFeatures);
    }
}

function initLegendFilters() {
    const filterBtns = document.querySelectorAll('.cantiere-filter-btn');
    if (!filterBtns || filterBtns.length === 0) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const target = e.currentTarget;
            filterBtns.forEach(b => {
                b.classList.remove('active-filter');
                b.classList.remove('bg-cyber-neon/20', 'text-cyber-neon', 'border-cyber-neon/50');
            });
            target.classList.add('active-filter');
            target.classList.add('bg-cyber-neon/20', 'text-cyber-neon', 'border-cyber-neon/50');
            
            currentCantiereFilter = target.dataset.filter || 'all';
            loadData();
        });
    });
}

window.setCantieriFilter = (filterName) => {
    currentCantiereFilter = filterName;
    const filterBtns = document.querySelectorAll('.cantiere-filter-btn');
    filterBtns.forEach(b => {
        if (b.dataset.filter === filterName) {
            b.classList.add('active-filter', 'bg-cyber-neon/20', 'text-cyber-neon', 'border-cyber-neon/50');
        } else {
            b.classList.remove('active-filter', 'bg-cyber-neon/20', 'text-cyber-neon', 'border-cyber-neon/50');
        }
    });
    loadData();
};

window.flyToFrazione = (lat, lng) => {
    if (map) map.flyTo([lat, lng], 16, { duration: 1.8 });
};
