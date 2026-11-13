// @ts-check
(() => {
    /** @typedef {import("../src/types/ordinanza").OrdinanzaAtto} Atto */
    /** @typedef {import("../src/types/ordinanza").StatoAtto} StatoAtto */

    const dialog = /** @type {HTMLDialogElement} */ (document.getElementById("archivio-atti"));
    const pdfDialog = /** @type {HTMLDialogElement} */ (document.getElementById("archivio-pdf"));
    const frame = /** @type {HTMLIFrameElement} */ (pdfDialog.querySelector("iframe"));
    const pdfLink = /** @type {HTMLAnchorElement} */ (pdfDialog.querySelector("a"));
    const search = /** @type {HTMLInputElement} */ (dialog.querySelector("input[type=search]"));
    const filters = /** @type {HTMLElement} */ (dialog.querySelector(".archivio-filters"));
    const sort = /** @type {HTMLSelectElement} */ (dialog.querySelector("select"));
    const results = /** @type {HTMLElement} */ (dialog.querySelector(".archivio-results"));
    const summary = /** @type {HTMLElement} */ (dialog.querySelector("[role=status]"));
    const more = /** @type {HTMLButtonElement} */ (dialog.querySelector(".archivio-more"));
    const pageSize = 20;
    const todayRome = () => new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Rome" }).format(new Date());
    const types = {
        ORDINANZA_VIABILITA: "Ordinanza di viabilità", CONCESSIONE_SUOLO: "Concessione suolo",
        AUTORIZZAZIONE_SCAVO: "Autorizzazione scavo", PROROGA: "Proroga",
        RIPRISTINO: "Ripristino", ALTRO: "Altro atto o allegato",
    };
    const states = {
        PROGRAMMATA: "Programmata", IN_CORSO: "In corso di validità",
        TERMINATA: "Validità terminata", NON_DOCUMENTATA: "Validità non rilevata",
        COMPLETATA: "Opere civili completate", PROROGA: "Proroga", DECADUTA: "Decaduta",
    };
    const areas = {
        COLLESALVETTI: "Collesalvetti Capoluogo", STAGNO: "Stagno", VICARELLO: "Vicarello",
        GUASTICCE: "Guasticce", NUGOLA: "Nugola", EXTRAURBANO: "Extraurbano",
    };

    /** @type {Atto[]} */
    let acts = [];
    /** @type {Promise<Atto[]> | undefined} */
    let pendingActs;
    /** @type {Promise<void> | undefined} */
    let pendingOffline;
    /** @type {Promise<Record<string, string>> | undefined} */
    let pendingText;
    /** @type {Record<string, string>} */
    let fullText = {};
    let textReady = false;
    let limit = pageSize;
    /** @type {string | null} */
    let selectedAct = null;
    /** @type {string | undefined} */
    let originFeatureId;
    /** @type {Map<string, {act: Atto, candidate: boolean}[]>} */
    const byFeature = new Map();

    /** @param {string} value */
    function normalize(value) {
        return value.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase()
            .replace(/[^a-z0-9]+/g, " ").trim();
    }

    function offline() {
        pendingOffline ??= new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src = "data/ordinanze/offline.js";
            script.onload = () => resolve(undefined);
            script.onerror = () => reject(new Error("Archivio offline non disponibile"));
            document.head.append(script);
        }).catch(error => {
            pendingOffline = undefined;
            throw error;
        });
        return pendingOffline;
    }

    /** @template T @param {string} path @param {() => T | undefined} fallback @returns {Promise<T>} */
    async function read(path, fallback) {
        if (location.protocol !== "file:") {
            try {
                const response = await fetch(path);
                if (response.ok) return await response.json();
            } catch {
                // The static fallback also supports use from a local file.
            }
        }
        await offline();
        const data = fallback();
        if (!data) throw new Error("Dati archivio non disponibili");
        return data;
    }

    function loadActs() {
        pendingActs ??= read("data/ordinanze/ordinanze.json", () => window.ARCHIVIO_ATTI).then(data => {
            acts = data;
            for (const act of acts) {
                const { matched_feature_ids, candidate_feature_ids } = act.localizzazione;
                for (const id of [...matched_feature_ids, ...candidate_feature_ids]) {
                    const matches = byFeature.get(id) ?? [];
                    matches.push({ act, candidate: candidate_feature_ids.includes(id) });
                    byFeature.set(id, matches);
                }
            }
            return acts;
        }).catch(error => {
            pendingActs = undefined;
            throw error;
        });
        return pendingActs;
    }

    /** @param {Atto} act @param {string} today @returns {StatoAtto} */
    function status(act, today) {
        const { dal, al, periodi } = act.validita;
        const windows = periodi ?? (dal && al ? [{ dal, al }] : []);
        if (!windows.length) return "NON_DOCUMENTATA";
        if (windows.some(window => window.dal <= today && today <= window.al)) return "IN_CORSO";
        return windows.some(window => today < window.dal) ? "PROGRAMMATA" : "TERMINATA";
    }

    /** @param {Atto} act */
    function title(act) {
        return act.numero_atto ? `${types[act.tipologia]} n. ${act.numero_atto}` : act.oggetto ?? act.file_pdf.nome_file.split("/").at(-1) ?? act.id;
    }

    /** @param {string | null} date */
    function formatDate(date) {
        return date ? date.split("-").reverse().join("/") : "—";
    }

    /** @param {string} tag @param {string} value @param {string} [className] */
    function element(tag, value, className) {
        const node = document.createElement(tag);
        node.textContent = value;
        if (className) node.className = className;
        return node;
    }

    /** @param {string} label @param {() => void} action */
    function button(label, action) {
        const node = /** @type {HTMLButtonElement} */ (element("button", label));
        node.type = "button";
        node.addEventListener("click", action);
        return node;
    }

    /** @param {Atto} act */
    function pdfUrl(act) {
        const url = new URL(act.file_pdf.url_path, document.baseURI);
        const root = new URL("data/ordinanze/", document.baseURI);
        return url.protocol === root.protocol && url.host === root.host &&
            url.pathname.startsWith(root.pathname) && url.pathname.endsWith(".pdf") ? url.href : null;
    }

    /** @param {Atto} act */
    function preview(act) {
        const url = pdfUrl(act);
        if (!url) return;
        pdfDialog.querySelector("h2")?.replaceChildren(title(act));
        pdfLink.href = url;
        frame.src = url;
        pdfDialog.showModal();
    }

    /** @param {string | null} [id] */
    async function openArchive(id = null) {
        selectedAct = id;
        limit = pageSize;
        if (!dialog.open) dialog.showModal();
        summary.textContent = "Caricamento dell’archivio…";
        try {
            await loadActs();
        } catch {
            summary.textContent = "Impossibile caricare l’archivio.";
            results.replaceChildren(button("Riprova", () => void openArchive(id)));
            return;
        }
        if (!filters.hasChildNodes()) buildFilters();
        update();
        if (!id) void loadSearchText();
    }

    /** @param {string} label @param {string} key @param {[string, string][]} options */
    function filter(label, key, options) {
        const group = document.createElement("details");
        group.append(element("summary", label));
        for (const [value, text] of options) {
            const input = document.createElement("input");
            input.type = "checkbox";
            input.name = key;
            input.value = value;
            const option = document.createElement("label");
            option.append(input, text);
            group.append(option);
        }
        return group;
    }

    function buildFilters() {
        const years = new Set(acts.map(a => a.data_emissione?.slice(0, 4) ?? "ND"));
        const lastYear = Math.max(Number(todayRome().slice(0, 4)), ...[...years].filter(year => year !== "ND").map(Number));
        for (let year = 2020; year <= lastYear; year++) years.add(String(year));
        const operators = new Set(acts.flatMap(a => [a.operator_target, a.richiedente]).filter(
            /** @returns {value is string} */ (value) => Boolean(value)
        ));
        filters.append(
            filter("Anno", "anno", [...years].sort().map(year => [year, year === "ND" ? "Senza data" : year])),
            filter("Area", "area", Object.entries(areas)),
            filter("Operatore / richiedente", "operatore", [...operators].sort().map(name => [name, name])),
            filter("Stato", "stato", Object.entries(states)),
        );
    }

    /** @param {Atto} act @param {string} today */
    function card(act, today) {
        const loc = act.localizzazione;
        const current = status(act, today);
        const article = document.createElement("article");
        article.className = "archivio-card";
        article.dataset.status = current;
        article.append(element("h3", title(act)));
        const tags = document.createElement("div");
        tags.className = "archivio-tags";
        tags.append(element("span", states[current], `archivio-badge ${current}`));
        if (act.tipologia === "PROROGA" || act.tipologia === "RIPRISTINO") {
            tags.append(element("span", types[act.tipologia], "archivio-badge"));
        }
        if (act.stato_opera && act.stato_opera !== current) {
            tags.append(element("span", `Opera · ${states[act.stato_opera]}`, "archivio-badge"));
        }
        if (act.ocr_required) tags.append(element("span", "OCR necessario", "archivio-badge"));
        article.append(tags);
        const issuer = act.ente === "COMUNE_COLLESALVETTI" ? "Comune di Collesalvetti" :
            act.ente === "PROVINCIA_LIVORNO" ? "Provincia di Livorno" : null;
        const metadata = [act.data_emissione && formatDate(act.data_emissione), issuer,
            act.registro_generale && `Reg. Gen. ${act.registro_generale}`, act.richiedente,
            act.operator_target !== act.richiedente && act.operator_target,
            loc.area && areas[loc.area]].filter(Boolean);
        if (metadata.length) article.append(element("p", metadata.join(" · "), "archivio-meta"));
        if (act.oggetto && act.oggetto !== title(act)) {
            const subject = element("details", "", "archive-subject");
            subject.append(element("summary", "Oggetto dell’atto"), element("p", act.oggetto));
            article.append(subject);
        }
        if (loc.strade.length) {
            const streets = element("p", "", "archive-streets");
            streets.append(element("strong", "Vie interessate"), loc.strade.join(" · "));
            article.append(streets);
        }
        if (loc.prog_chilometrica) {
            const { dal_km, al_km } = loc.prog_chilometrica;
            article.append(element("p", `Progressiva km ${dal_km} – ${al_km}`, "archivio-meta"));
        }
        const windows = act.validita.periodi ?? [act.validita];
        for (const { dal, al } of windows.filter(({ dal, al }) => dal || al)) {
            const validity = element("p", "", "archive-validity");
            const dates = [formatDate(dal), formatDate(al)].join(" → ");
            validity.append(element("strong", "Validità"), [dates, act.validita.orario].filter(Boolean).join(" · "));
            article.append(validity);
        }
        if (act.note_tecniche) article.append(element("p", act.note_tecniche));
        const actions = document.createElement("div");
        actions.className = "archivio-actions";
        const url = pdfUrl(act);
        if (url) {
            const previewButton = button("Anteprima PDF", () => preview(act));
            previewButton.classList.add("archive-primary");
            actions.append(previewButton);
            const link = /** @type {HTMLAnchorElement} */ (element("a", "Apri PDF ↗"));
            link.href = url;
            link.target = "_blank";
            link.rel = "noopener";
            actions.append(link);
        }
        if (window.showArchivioFeatures) {
            /** @type {[string, string[]][]} */
            const mapActions = [["Mostra sulla mappa", loc.matched_feature_ids],
                ["Mostra corrispondenze per strada", loc.candidate_feature_ids]];
            for (const [label, ids] of mapActions) {
                if (ids.length) actions.append(button(label, () => {
                    dialog.close();
                    window.showArchivioFeatures?.(ids, originFeatureId);
                }));
            }
        }
        article.append(actions);

        const related = acts.filter(other => other !== act && (
            act.atti_collegati.includes(other.id) || other.atti_collegati.includes(act.id) ||
            (act.cluster_id && other.cluster_id === act.cluster_id)
        ));
        if (related.length || act.riferimenti.length || act.protocollo) {
            const details = document.createElement("details");
            details.append(element("summary", "Protocollo e atti collegati"));
            if (act.protocollo) {
                details.append(element("p", `Prot. ${act.protocollo}${act.data_protocollo ? ` · ${formatDate(act.data_protocollo)}` : ""}`));
            }
            for (const ref of act.riferimenti) {
                details.append(element("p", `${ref.tipo.toLowerCase()} ${ref.numero}${ref.data ? ` · ${formatDate(ref.data)}` : ""}`));
            }
            const links = document.createElement("div");
            links.className = "archivio-actions";
            for (const other of related) links.append(button(title(other), () => void openArchive(other.id)));
            details.append(links);
            article.append(details);
        }
        return article;
    }

    function update() {
        const tokens = normalize(search.value).split(" ").filter(Boolean);
        const today = todayRome();
        const active = [...filters.querySelectorAll("input:checked")].map(
            input => /** @type {HTMLInputElement} */ (input)
        );
        /** @param {string} name @param {(string | null)[]} values */
        const passes = (name, values) => {
            const group = active.filter(input => input.name === name);
            return !group.length || group.some(input => values.includes(input.value));
        };
        const filtered = acts.filter(act => {
            if (selectedAct) return act.id === selectedAct;
            if (!passes("anno", [act.data_emissione?.slice(0, 4) ?? "ND"]) ||
                !passes("area", [act.localizzazione.area]) ||
                !passes("operatore", [act.operator_target, act.richiedente]) ||
                !passes("stato", [status(act, today), act.stato_opera, act.tipologia])) return false;
            if (!tokens.length) return true;
            const corpus = normalize([act.id, act.oggetto, act.numero_atto, act.registro_generale, act.protocollo,
                act.richiedente, act.operator_target, act.localizzazione.area, ...act.localizzazione.strade,
                act.file_pdf.nome_file, act.cluster_id, types[act.tipologia], fullText[act.id]].join(" "));
            return tokens.every(token => corpus.includes(token));
        });
        if (sort.value === "older") filtered.sort((a, b) =>
            (a.data_emissione ?? "9999").localeCompare(b.data_emissione ?? "9999"));
        if (sort.value === "number") filtered.sort((a, b) =>
            (a.numero_atto ?? "zz").localeCompare(b.numero_atto ?? "zz", "it", { numeric: true }));
        results.replaceChildren(...filtered.slice(0, limit).map(act => card(act, today)));
        if (!filtered.length) results.append(element("p", "Nessun atto corrisponde ai criteri selezionati."));
        more.hidden = limit >= filtered.length;
        summary.textContent = `${filtered.length} ${filtered.length === 1 ? "atto" : "atti"}`;
        if (filtered.length > limit) summary.append(` · primi ${limit} risultati`);
        if (selectedAct) summary.append(" · ", button("Torna ai risultati", () => void openArchive()));
        if (tokens.length && !selectedAct && !textReady) {
            summary.append(" · Ricerca nel testo…");
        }
    }

    async function loadSearchText() {
        if (!normalize(search.value) || pendingText || textReady) return;
        pendingText = read("data/ordinanze/testo.json", () => window.ARCHIVIO_TESTI);
        try {
            fullText = await pendingText;
            textReady = true;
            update();
        } catch {
            pendingText = undefined;
            if (search.value && !selectedAct) summary.append(" · Testo integrale non disponibile.");
        }
    }

    for (const trigger of document.querySelectorAll("[data-open-archivio]")) {
        trigger.addEventListener("click", () => {
            originFeatureId = undefined;
            void openArchive();
        });
    }
    search.addEventListener("input", () => {
        selectedAct = null;
        limit = pageSize;
        update();
        void loadSearchText();
    });
    filters.addEventListener("change", () => {
        selectedAct = null;
        limit = pageSize;
        update();
    });
    sort.addEventListener("change", update);
    more.addEventListener("click", () => {
        limit += pageSize;
        update();
    });
    dialog.querySelector("[data-clear-archivio]")?.addEventListener("click", () => {
        search.value = "";
        sort.value = "newer";
        for (const input of filters.querySelectorAll("input")) input.checked = false;
        void openArchive();
    });
    pdfDialog.addEventListener("close", () => frame.removeAttribute("src"));

    window.appendArchivioLinks = (container, id, { includePdf = true } = {}) => {
        return loadActs().then(() => {
            const matches = byFeature.get(id) ?? [];
            if (!matches.length) return;
            const related = element("details", "", "archive-candidates");
            const candidates = matches.filter(match => match.candidate).length;
            related.append(element("summary", `Corrispondenze per strada (${candidates})`));
            container.append(element("strong", "Archivio atti"));

            for (const { act, candidate } of matches) {
                const row = document.createElement("div");
                row.append(button(title(act), () => {
                    originFeatureId = id;
                    void openArchive(act.id);
                }));
                const url = pdfUrl(act);
                if (url && (includePdf || candidate)) {
                    const link = /** @type {HTMLAnchorElement} */ (element("a", "PDF ↗"));
                    link.href = url;
                    link.target = "_blank";
                    link.rel = "noopener";
                    row.append(link);
                }
                (candidate ? related : container).append(row);
            }
            if (candidates) container.append(related);
        }).catch(() => {});
    };
})();
