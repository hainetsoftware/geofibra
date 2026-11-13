const MAP_START_CENTER = [43.591, 10.4770];

const FEATURE_TYPES = {
    arl: 'Armadio rame',
    arlo: 'Armadio fibra',
    centrale_comunale: 'Centrale comunale',
    centrale_frazione: 'Centrale di frazione',
    centrale_feeder: 'Centrale feeder',
    copertura_ok: 'Area coperta',
    copertura_no: 'Area non coperta',
    infrastruttura: 'Infrastruttura',
    materials_depot: 'Materiali sul campo',
    infratel: 'Rete Infratel',
    rete_sanita: 'Sanità connessa',
    rete_scuole: 'Scuole connesse',
    tratta_backbone: 'Dorsale',
    tratta_stagno: 'Tratta di rete'
};

const lengthFormat = new Intl.NumberFormat('it-IT', { maximumFractionDigits: 3 });
const surveyDateFormat = new Intl.DateTimeFormat('it-IT', {
    day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Rome'
});

function dateLabel(value) {
    const date = new Date(value);
    return value && Number.isFinite(date.getTime()) ? surveyDateFormat.format(date) : '';
}

function featureType(props) {
    return FEATURE_TYPES[props.category] || 'Tratta di cantiere';
}

function featureStatus(props) {
    if (props.category.startsWith('copertura_')) return '';
    if (props.cantiere?.stato_base === 'staged_for_digging') return 'Scavi da avviare';
    return props.status_label;
}

function updateTelemetry() {
    const stats = window.FTTH_STATS;
    if (!stats) return;
    const equipment = stats.equipment;
    const values = {
        'stat-tot': equipment.total_municipal,
        'stat-km': lengthFormat.format(stats.length_km.total),
        'stat-arl': equipment.by_category_municipal.arl || 0,
        'stat-arlo': equipment.by_category_municipal.arlo || 0,
        'stat-centrali': equipment.centrali_municipal,
        'stat-cantieri': window.FTTH_NETWORK_DATA.features.filter(f => f.properties.category.startsWith('cantiere_')).length,
        'stat-arlo-stagno': equipment.by_frazione_municipal.Stagno?.arlo ?? 0
    };
    for (const [id, value] of Object.entries(values)) {
        document.getElementById(id).textContent = value;
    }

    const entries = Object.entries(equipment.by_frazione_municipal);
    entries.sort((a, b) => b[1].totale - a[1].totale);
    const statsList = document.getElementById('frazioni-stats');
    for (const [name, counts] of entries) {
        const row = document.createElement('div');
        row.append(textElement('dt', name), textElement('dd', counts.totale));
        if (counts.arlo) row.lastElementChild.append(` · ${counts.arlo} ARLO`);
        statsList.append(row);
    }
}

function textElement(tag, text, className) {
    const node = document.createElement(tag);
    node.textContent = text;
    if (className) node.className = className;
    return node;
}

function renderList(features) {
    const list = document.getElementById('elements-list');
    document.getElementById('map-results-count').textContent =
        features.length === 1 ? '1 risultato' : `${features.length} risultati`;
    list.replaceChildren();

    if (!features.length) {
        list.append(textElement('li', 'Nessun elemento corrisponde alla ricerca e ai filtri.', 'empty-results'));
        return;
    }

    for (const feature of features) {
        const props = feature.properties;
        const item = document.createElement('li');
        const button = textElement('button', '', 'result-button');
        button.type = 'button';
        button.dataset.featureId = feature.id;

        const title = textElement('span', '', 'result-title');
        const swatch = textElement('span', '', 'map-swatch');
        if (props.status === 'riuso_previsto') swatch.classList.add('swatch-dashed');
        swatch.style.setProperty('--swatch', featureColor(props));
        swatch.setAttribute('aria-hidden', 'true');
        title.append(swatch, document.createTextNode(props.name));

        const meta = [props.frazione, featureType(props)];
        if (props.length_m > 0) meta.push(`${lengthFormat.format(props.length_m)} m`);
        button.append(title, textElement('span', meta.filter(Boolean).join(' · '), 'result-meta'));
        const status = featureStatus(props);
        if (status) {
            button.append(textElement('span', status, 'status-tag'));
        }
        button.addEventListener('click', () => selectMapFeature(feature, true));
        item.append(button);
        list.append(item);
    }
}

function inspectionSection(title, lines, tone) {
    const section = textElement('section', '', 'inspection-block');
    section.dataset.tone = tone;
    section.append(textElement('h3', title));
    for (const line of lines.filter(Boolean)) section.append(textElement('p', line));
    return section;
}

function detailLink(label, emoji, url) {
    const link = textElement('a', '', 'ui-button');
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener';
    const icon = textElement('span', emoji, 'emoji');
    icon.setAttribute('aria-hidden', 'true');
    link.append(icon, document.createTextNode(` ${label}`));
    return link;
}

function showMapInspection(feature) {
    const props = feature.properties;
    const worksite = props.cantiere;
    const content = document.getElementById('inspection-content');
    const title = textElement('h2', props.name);
    title.tabIndex = -1;
    const meta = [props.frazione, featureType(props), props.operatore].filter(Boolean);
    if (props.length_m > 0) meta.push(`${lengthFormat.format(props.length_m)} m`);
    if (props.area_m2 > 0) meta.push(`${lengthFormat.format(props.area_m2)} m²`);
    content.replaceChildren(title, textElement('p', meta.join(' · '), 'muted'));

    const date = dateLabel(props.data_rilevamento);
    const staged = worksite?.stato_base === 'staged_for_digging';
    const observation = staged
        ? 'Marcature stradali e bobine di microtubi Fender rilevate sul posto.'
        : props.description;
    const fieldStatus = featureStatus(props);
    const field = inspectionSection('Rilievo sul campo', [date], 'blue');
    if (fieldStatus) field.append(textElement('span', fieldStatus, 'status-tag'));
    if (observation) field.append(textElement('p', observation));
    content.append(field);

    if (worksite || props.ordinanza) {
        const start = dateLabel(worksite?.inizio_lavori);
        const end = dateLabel(worksite?.fine_lavori);
        const period = [start, end].filter(Boolean).join(' – ');
        const streets = worksite?.vie_interessate ?? props.streets;
        const ordinance = inspectionSection('Ordinanza', [
            worksite?.codice_ordinanza ?? props.ordinanza,
            [period, worksite?.orario_giornaliero].filter(Boolean).join(' · '),
            worksite?.richiedente && `Richiedente: ${worksite.richiedente}`,
            streets?.length ? `Vie interessate: ${streets.join(', ')}` : '',
            !staged && worksite?.note_slittamento !== observation ? worksite?.note_slittamento : ''
        ], 'amber');
        if (worksite?.file_pdf) ordinance.append(detailLink('Apri PDF', '📄', worksite.file_pdf));
        content.append(ordinance);
    }

    if (props.wholesale) {
        const { element_id, acl, central_office, status, availability_date } = props.wholesale;
        const rollout = props.commercial_rollout;
        const imminent = rollout?.status === 'in_vendibilita_imminente';
        content.append(inspectionSection('Disponibilità FiberCop Wholesale', [
            `CRO ${element_id} · ${status}`,
            `Centrale ${central_office} · ACL ${acl}`,
            dateLabel(availability_date),
            imminent && 'In arrivo la rete ultraveloce',
            imminent && rollout.streets?.join(', '),
            imminent && rollout.operators_reported && `${rollout.operators_reported} operatori segnalati`,
            imminent && rollout.reported_active_address && `Attivazione segnalata al civico ${rollout.reported_active_address}`
        ], 'green'));
    }

    if (feature.geometry.type === 'LineString' || props.category === 'arlo') {
        const links = textElement('div', '', 'archivio-popup');
        content.append(links);
        window.appendArchivioLinks?.(links, feature.id, { includePdf: !worksite?.file_pdf });
    }
    if (feature.geometry.type === 'Point') {
        const [lng, lat] = feature.geometry.coordinates;
        content.append(detailLink('Street View', '📍', `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}`));
    }

    showSidebarView('map-inspection');
    title.focus();
}
