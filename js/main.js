const dashboard = document.getElementById('desktop-app-container');
const sidebar = document.getElementById('map-sidebar');
const toggleSidebar = document.getElementById('toggle-map-sidebar');
const search = document.getElementById('search-elements');
const frazione = document.getElementById('frazioni-nav');
const filterButtons = [...document.querySelectorAll('.cantiere-filter-btn')];
let activeFilter = 'all';

function setSidebarOpen(open) {
    if (sidebar.hidden === !open) return;
    sidebar.hidden = !open;
    toggleSidebar.setAttribute('aria-expanded', String(open));
    toggleSidebar.lastElementChild.textContent = open ? 'Nascondi pannello' : 'Mostra pannello';
    dashboard.classList.toggle('sidebar-closed', !open);
    map.invalidateSize({ pan: true });
}

function showSidebarView(id) {
    for (const view of sidebar.children) view.hidden = view.id !== id;
    setSidebarOpen(true);
}

function normalizeMapSearch(value) {
    return value.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '');
}

function refreshMapResults() {
    const terms = normalizeMapSearch(search.value.trim()).split(/\s+/).filter(Boolean);
    const territory = window.FTTH_NETWORK_DATA.features.filter(feature =>
        !frazione.value || feature.properties.frazione === frazione.value);
    const matching = territory.filter(feature => {
        const props = feature.properties;
        const searchable = normalizeMapSearch([
            props.name, props.frazione, featureType(props), props.status_label,
            ...(props.streets ?? []), props.wholesale?.element_id, props.wholesale?.acl
        ].join(' '));
        return terms.every(term => searchable.includes(term));
    });

    for (const button of filterButtons) {
        const filter = button.dataset.filter;
        const count = button.querySelector('[data-filter-count]');
        if (count) count.textContent = matching.filter(feature => featureMatchesFilter(feature, filter)).length;
        button.setAttribute('aria-pressed', String(filter === activeFilter));
    }
    document.getElementById('reset-map-filters').hidden = !(terms.length || frazione.value || activeFilter !== 'all');
    const results = matching.filter(feature => featureMatchesFilter(feature, activeFilter));
    clearMapSelection();
    loadData(results);
    renderList(results);
}

function frameMapResults() {
    if (mapResults.length) {
        map.fitBounds(geojsonLayer.getBounds(), { padding: [28, 28], maxZoom: 17 });
    }
}

function resetMapFilters() {
    search.value = '';
    frazione.value = '';
    activeFilter = 'all';
    refreshMapResults();
}

function initMapControls() {
    const places = new Set(window.FTTH_NETWORK_DATA.features.map(f => f.properties.frazione).filter(Boolean));
    for (const name of [...places].sort((a, b) => a.localeCompare(b, 'it'))) {
        frazione.add(new Option(name, name));
    }

    toggleSidebar.addEventListener('click', () => setSidebarOpen(sidebar.hidden));
    document.getElementById('open-survey').addEventListener('click', () => {
        showSidebarView('telemetry-panel');
        document.getElementById('survey-heading').focus();
    });
    for (const button of document.querySelectorAll('[data-back-to-map-results]')) {
        button.addEventListener('click', () => {
            const result = [...document.querySelectorAll('[data-feature-id]')].find(row => row.dataset.featureId === selectedFeature?.id);
            showSidebarView('map-explore');
            clearMapSelection();
            (result || search).focus();
        });
    }
    search.addEventListener('input', refreshMapResults);
    frazione.addEventListener('change', () => {
        refreshMapResults();
        frameMapResults();
    });
    for (const button of filterButtons) {
        button.addEventListener('click', () => {
            activeFilter = button.dataset.filter;
            refreshMapResults();
            if (activeFilter !== 'all') frameMapResults();
        });
    }
    document.getElementById('reset-map-filters').addEventListener('click', () => {
        resetMapFilters();
        map.setView(MAP_START_CENTER, 15);
        search.focus();
    });
    refreshMapResults();
}

function initApp() {
    const { source_snapshot: snapshot, generated_at: date } = window.FTTH_NETWORK_DATA.metadata;
    const label = [snapshot, dateLabel(date)].filter(Boolean).join(' · ');
    document.getElementById('snapshot-nav-label').textContent = label;
    document.getElementById('snapshot-survey-label').textContent = label;

    initMap();
    initMapControls();
    updateTelemetry();

    const tracker = document.getElementById('modal-cantieri');
    document.getElementById('btn-open-cantieri').addEventListener('click', () => {
        window.initCantieriTracker();
        tracker.showModal();
    });
    window.initCantieriTracker();
    document.getElementById('map-loading').hidden = true;
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
