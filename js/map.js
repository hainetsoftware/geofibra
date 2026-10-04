let map;
let geojsonLayer;

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
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2" ry="2"></rect><circle cx="12" cy="12" r="3"></circle><line x1="12" y1="3" x2="12" y2="6"></line></svg>`;
    } else if (iconName === 'building-tower') {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="14" rx="2" ry="2"></rect><path d="M12 10V2"></path><path d="M8 6h8"></path></svg>`;
    } else if (iconName === 'building-small') {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="16" rx="2" ry="2"></rect><path d="M4 8l8-6 8 6"></path></svg>`;
    } else {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
    }
    
    return `<div class="pulse-marker" style="color: ${color}; background: rgba(10, 13, 20, 0.85); border: 1px solid ${color}; border-radius: 50%; padding: 3px;">${svg}</div>`;
}

function initMap() {
    const center = [43.5884, 10.4770];
    
    map = L.map('map', {
        zoomControl: false,
        attributionControl: false,
        // Limita rigorosamente la mappa ai confini della Toscana
        maxBounds: TOSCANA_BOUNDS,
        maxBoundsViscosity: 1.0, // Blocca completamente il panning oltre i confini
        minZoom: 9,              // Impedisce di zoomare indietro oltre la Toscana
        maxZoom: 19
    }).setView(center, 15);

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Layer 1: Cyber Dark (Esri Dark Canvas - 100% stabile, nessun token o API key richiesta)
    const darkBase = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', { 
        maxZoom: 19,
        bounds: TOSCANA_BOUNDS
    });
    const darkRef = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', { 
        maxZoom: 19,
        bounds: TOSCANA_BOUNDS
    });
    const darkGroup = L.layerGroup([darkBase, darkRef]);

    // Layer 2: Satellite HD (Esri World Imagery)
    const satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { 
        maxZoom: 19,
        bounds: TOSCANA_BOUNDS
    });

    // Layer 3: Topografico OpenStreetMap
    const topoLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
        maxZoom: 19,
        subdomains: ['a', 'b', 'c'],
        bounds: TOSCANA_BOUNDS
    });

    const layers = {
        dark: darkGroup,
        satellite: satLayer,
        topo: topoLayer
    };

    // Imposta OpenStreetMap di default per massima nitidezza zoom
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
}

function loadData() {
    if (!window.FTTH_NETWORK_DATA) return;
    
    geojsonLayer = L.geoJSON(window.FTTH_NETWORK_DATA, {
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
                    opacity: 0.9,
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
            
            let popupContent = `
                <div>
                    <span class="badge" style="background: ${props.color}33; color: ${props.color}; border: 1px solid ${props.color}">${props.category.replace('_', ' ')}</span>
                    <h3>${props.name}</h3>
                    <div class="text-xs text-slate-400 mb-2">📍 Frazione: <b>${props.frazione}</b></div>
            `;
            
            if (props.description) {
                popupContent += `<div class="notes border-l-2 pl-2" style="border-color: ${props.color}">${props.description}</div>`;
            }
            
            if (props.length_m > 0) popupContent += `<div class="text-sm mt-2">📏 Tratta: <b>${props.length_m} m</b> (${props.length_km} km)</div>`;
            if (props.area_m2 > 0) popupContent += `<div class="text-sm mt-2">📐 Superficie: <b>${props.area_km2} km²</b></div>`;
            
            // Dettagli dinamici cantiere Albo Pretorio
            if (props.cantiere) {
                const cInfo = props.cantiere;
                let statusInfo = null;
                if (window.calculateCantiereStatus) {
                    statusInfo = window.calculateCantiereStatus({
                        inizio: cInfo.inizio_lavori,
                        fine: cInfo.fine_lavori,
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
                        <div class="bg-black/40 p-2.5 rounded border border-white/10 mb-2.5">
                            <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Vie Autorizzate dallo Scavo:</div>
                            <ul class="list-disc list-inside space-y-0.5 text-slate-300 text-[11px]">
                                ${cInfo.vie_interessate.map(v => `<li>${v}</li>`).join('')}
                            </ul>
                        </div>
                        <a href="${cInfo.file_pdf}" target="_blank" download class="w-full bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/50 text-amber-300 py-1.5 px-2 rounded text-xs font-bold flex items-center justify-center gap-1.5 transition-colors mb-2">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Scarica PDF Ordinanza Ufficiale
                        </a>
                    </div>
                `;
            }

            let mapsTarget = feature.geometry.type === 'Point' ? `${feature.geometry.coordinates[1]},${feature.geometry.coordinates[0]}` : '';
            
            popupContent += `
                    <div class="mt-3 flex gap-2">
                        `;
            if (mapsTarget) {
                popupContent += `<a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${mapsTarget}" target="_blank" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-1 px-2 rounded text-xs text-center border border-white/20 transition-colors flex items-center justify-center">Street View</a>`;
            }
            popupContent += `</div></div>`;
            
            layer.bindPopup(popupContent, { minWidth: 280, maxWidth: 340 });
        }
    }).addTo(map);
    
    if(window.updateTelemetry) window.updateTelemetry(window.FTTH_NETWORK_DATA.features);
}

window.flyToFrazione = (lat, lng) => {
    map.flyTo([lat, lng], 16, { duration: 1.8 });
};
