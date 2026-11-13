let map;
let geojsonLayer;
let archivioHighlight;
let mapResults = [];
let selectedFeature;

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
    } else if (iconName === 'cable-reel') {
        svg = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="10" r="7"></circle><circle cx="12" cy="10" r="3"></circle><path d="M12 17v3h8"></path></svg>`;
    } else {
        svg = `<svg xmlns="http://www.w3.org/2005/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
    }
    
    return `<span class="network-marker" style="--marker-color: ${color}">${svg}</span>`;
}

function initMap() {
    map = window.map = L.map('map', {
        zoomControl: false,
        attributionControl: true,
        maxBounds: TOSCANA_BOUNDS,
        maxBoundsViscosity: 1.0,
        minZoom: 9,
        maxZoom: 19
    }).setView(MAP_START_CENTER, 15);

    map.createPane('polygonsPane').style.zIndex = 350;
    map.createPane('linesPane').style.zIndex = 450;
    map.createPane('markersPane').style.zIndex = 600;
    const highlightPane = map.createPane('archivioHighlightPane');
    highlightPane.style.zIndex = 440;
    highlightPane.style.pointerEvents = 'none';

    L.control.zoom({ position: 'topright' }).addTo(map);

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

    document.getElementById('map-basemap').addEventListener('change', event => {
        Object.values(layers).forEach(layer => map.removeLayer(layer));
        layers[event.currentTarget.value].addTo(map);
    });
}

function featureMatchesFilter(feature, filter) {
    if (!filter || filter === 'all') return true;
    const { status, category } = feature.properties;

    if (filter === 'completati') {
        return feature.geometry.type === 'LineString' && status === 'completato';
    }
    if (filter === 'autorizzati') {
        return status === 'autorizzato' || status === 'planned';
    }
    if (filter === 'progettazione_esecutiva') {
        return category === 'cantiere_progettazione_esecutiva';
    }
    return status === filter;
}

function featureColor(props) {
    if (props.geom_type !== 'Point') return props.color;
    if (props.category === 'arlo') return '#2563eb';
    if (props.category === 'arl') return '#111827';
    if (props.category.startsWith('centrale_')) return '#6b7280';
    return '#4b5563';
}

function loadData(features) {
    mapResults = features;
    archivioHighlight?.remove();
    geojsonLayer?.remove();

    geojsonLayer = L.geoJSON(features, {
        pointToLayer(feature, latlng) {
            const props = feature.properties;
            const icon = L.divIcon({
                className: 'custom-div-icon',
                html: getIconHtml(props.icon, featureColor(props)),
                iconSize: [26, 26],
                iconAnchor: [13, 13]
            });
            return L.marker(latlng, { icon, pane: 'markersPane', title: props.name, alt: props.name });
        },
        style(feature) {
            const props = feature.properties;
            const line = feature.geometry.type === 'LineString';
            return {
                pane: line ? 'linesPane' : 'polygonsPane',
                bubblingMouseEvents: false,
                color: props.color,
                dashArray: props.status === 'riuso_previsto' ? '5 7' : null,
                weight: line ? 4 : 2,
                fillOpacity: line ? 0 : 0.16,
                className: 'network-path'
            };
        },
        onEachFeature(feature, layer) {
            layer.on('click', event => {
                if (feature.geometry.type === 'LineString') L.DomEvent.stopPropagation(event);
                selectMapFeature(feature);
            });
        }
    }).addTo(map);
}

function highlightMapFeatures(features) {
    archivioHighlight?.remove();
    const style = { pane: 'archivioHighlightPane', interactive: false, color: '#111827', weight: 8, opacity: 0.85, fill: false };
    archivioHighlight = L.geoJSON(features, {
        style,
        pointToLayer: (_feature, latlng) => L.circleMarker(latlng, { ...style, radius: 17, weight: 3 })
    }).addTo(map);
    return archivioHighlight.getBounds();
}

function selectMapFeature(feature, center = false) {
    selectedFeature = feature;
    const bounds = highlightMapFeatures([feature]);
    showMapInspection(feature);
    if (center || !map.getBounds().contains(bounds)) {
        map.fitBounds(bounds, { padding: [35, 35], maxZoom: 17 });
    }
}

function clearMapSelection() {
    selectedFeature = null;
    archivioHighlight?.remove();
}

window.flyToFrazione = (lat, lng) => {
    map.setView([lat, lng], 16);
};

window.showArchivioFeatures = (ids, originFeatureId) => {
    if (!map) return;
    const requested = new Set(ids);
    if (selectedFeature?.id === originFeatureId && requested.has(originFeatureId)) return;

    const features = window.FTTH_NETWORK_DATA.features.filter(feature => requested.has(feature.id));
    if (!features.length) return;
    if (features.some(feature => !mapResults.includes(feature))) resetMapFilters();
    showSidebarView('map-explore');
    clearMapSelection();
    const bounds = highlightMapFeatures(features);
    map.fitBounds(bounds, { padding: [35, 35], maxZoom: 17 });
};
