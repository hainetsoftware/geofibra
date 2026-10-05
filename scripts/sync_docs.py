#!/usr/bin/env python3
"""
sync_docs.py - Rigenera i blocchi auto-generati dei documenti Markdown da data/stats.json
e ricostruisce la voce 'collesalvetti' di wiki/articles_data.js.

I blocchi sono delimitati da:
    <!-- AUTO-STATS:BEGIN nome -->  ...  <!-- AUTO-STATS:END nome -->
Il contenuto tra i marcatori viene sovrascritto: non modificarlo a mano.

Uso (dalla radice del repository):
    python3 scripts/sync_docs.py            # riscrive i blocchi
    python3 scripts/sync_docs.py --check    # esce con 1 se qualcosa non e' allineato
"""

import json
import re
import sys

STATS = "data/stats.json"
BUNDLE = "wiki/articles_data.js"
BUNDLE_KEY = "window.WIKI_ARTICLES_DATA = "

# file -> (lingua, [nomi blocco])
TARGETS = {
    "README.md": ("it", ["equipment", "frazioni"]),
    "README_EN.md": ("en", ["equipment", "frazioni"]),
    "wiki/collesalvetti.md": ("it", ["equipment", "frazioni"]),
}

FRAZIONE_ORDER = [
    "Stagno", "Collesalvetti", "Vicarello", "Guasticce",
    "Nugola", "Parrana San Martino", "Parrana San Giusto",
]

T = {
    "it": {
        "dec": ",",
        "eq_head": "| Tipologia | Categoria GIS | Quantità | Note |",
        "arl": "Armadio Ripartilinea (ARL, rame)",
        "arlo": "Armadio Ripartilinea Ottico (ARLO)",
        "cc": "Centrale Comunale",
        "cf": "Centrali di Frazione",
        "cabs": "Totale armadi (ARL + ARLO)",
        "tot": "Totale apparati sul territorio comunale",
        "ext": "Apparati esterni al Comune (non inclusi nel totale)",
        "ext_note": "fuori dal territorio comunale",
        "excl": "Punti non-apparato (esclusi dal conteggio)",
        "excl_note": "punto di infrastruttura, non apparato",
        "intro": "Apparati = punti di rete censiti (armadi ARL/ARLO e centrali) sul suolo comunale. Linee, poligoni e punti di infrastruttura non sono apparati.",
        "fr_head": "| Frazione | Apparati | ARLO | ARL | Centrali | Tratte (km) | Quota % km |",
        "fr_other": "Altro / non attribuito",
        "fr_tot": "Totale",
        "fr_note": "Gli apparati sono contati per frazione dal solo territorio comunale; i km delle tratte comprendono anche la dorsale INFRATEL BUL e le tratte senza frazione (`Altro`).",
    },
    "en": {
        "dec": ".",
        "eq_head": "| Equipment type | GIS category | Quantity | Notes |",
        "arl": "Copper cabinet (ARL)",
        "arlo": "Optical cabinet (ARLO)",
        "cc": "Municipal central office",
        "cf": "Fraction central offices",
        "cabs": "Total cabinets (ARL + ARLO)",
        "tot": "Total equipment within the municipality",
        "ext": "Equipment outside the municipality (not included in the total)",
        "ext_note": "outside the municipal territory",
        "excl": "Non-equipment points (excluded from the count)",
        "excl_note": "infrastructure point, not equipment",
        "intro": "Equipment = surveyed network points (ARL/ARLO cabinets and central offices) inside the municipality. Lines, polygons and infrastructure points are not equipment.",
        "fr_head": "| Fraction | Equipment | ARLO | ARL | Central offices | Routes (km) | Share % km |",
        "fr_other": "Other / unassigned",
        "fr_tot": "Total",
        "fr_note": "Equipment is counted per fraction inside the municipality only; route km also include the INFRATEL BUL backbone and routes with no fraction (`Altro`).",
    },
}


def num(x, lang, nd=3):
    return f"{x:.{nd}f}".replace(".", T[lang]["dec"])


def render_equipment(stats, lang):
    t = T[lang]
    eq = stats["equipment"]
    c = eq["by_category_municipal"]
    rows = [
        t["intro"], "", t["eq_head"], "|---|---|:---:|---|",
        f"| **{t['arl']}** | `arl` | **{c.get('arl', 0)}** | |",
        f"| **{t['arlo']}** | `arlo` | **{c.get('arlo', 0)}** | |",
        f"| *{t['cabs']}* | | *{eq['cabinets_municipal']}* | |",
        f"| **{t['cc']}** | `centrale_comunale` | **{c.get('centrale_comunale', 0)}** | |",
        f"| **{t['cf']}** | `centrale_frazione` | **{c.get('centrale_frazione', 0)}** | |",
        f"| **{t['tot']}** | | **{eq['total_municipal']}** | |",
    ]
    for e in eq["external"]:
        rows.append(f"| {t['ext']}: {e['name']} | `{e['category']}` | {eq['total_external']} | {t['ext_note']} |")
    for e in eq["excluded_points"]:
        rows.append(f"| {t['excl']}: {e['name']} | `{e['category']}` | 1 | {t['excl_note']} |")
    return "\n".join(rows)


def render_frazioni(stats, lang):
    t = T[lang]
    eq = stats["equipment"]["by_frazione_municipal"]
    km = stats["length_km"]["by_frazione"]
    tot_km = stats["length_km"]["total"]
    names = [f for f in FRAZIONE_ORDER if f in eq or f in km]
    names += sorted(f for f in set(eq) | set(km) if f not in names and f != "Altro")
    rows = [t["fr_head"], "|---|:---:|:---:|:---:|:---:|:---:|:---:|"]

    def line(label, d, k):
        pct = (k / tot_km * 100) if tot_km else 0
        return (f"| **{label}** | {d['totale']} | {d['arlo']} | {d['arl']} | {d['centrali']} | "
                f"{num(k, lang)} km | {num(pct, lang, 1)}% |")

    zero = {"totale": 0, "arlo": 0, "arl": 0, "centrali": 0}
    for f in names:
        rows.append(line(f, eq.get(f, zero), km.get(f, 0.0)))
    if "Altro" in km:
        rows.append(line(t["fr_other"], zero, km["Altro"]))
    e = stats["equipment"]
    tot = {"totale": e["total_municipal"],
           "arlo": e["by_category_municipal"].get("arlo", 0),
           "arl": e["by_category_municipal"].get("arl", 0),
           "centrali": e["centrali_municipal"]}
    rows.append(line(t["fr_tot"], tot, tot_km).replace("| **", "| **", 1))
    rows.append("")
    rows.append(f"*{t['fr_note']}*")
    return "\n".join(rows)


RENDER = {"equipment": render_equipment, "frazioni": render_frazioni}


def block_re(name):
    return re.compile(
        rf"(<!-- AUTO-STATS:BEGIN {name} -->\n)(.*?)(\n<!-- AUTO-STATS:END {name} -->)", re.S
    )


def sync_file(path, lang, names, stats):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    new = text
    for n in names:
        rx = block_re(n)
        if not rx.search(new):
            raise SystemExit(f"{path}: blocco AUTO-STATS '{n}' mancante")
        body = RENDER[n](stats, lang)
        new = rx.sub(lambda m: m.group(1) + body + m.group(3), new)
    return text, new


def build_bundle(bundle_text, md_text):
    i = bundle_text.index(BUNDLE_KEY)
    head = bundle_text[: i + len(BUNDLE_KEY)]
    data = json.loads(bundle_text[i + len(BUNDLE_KEY):].rstrip().rstrip(";"))
    data["collesalvetti"] = md_text
    return head + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"


def main():
    check = "--check" in sys.argv
    with open(STATS, encoding="utf-8") as f:
        stats = json.load(f)
    bad = []
    for path, (lang, names) in TARGETS.items():
        old, new = sync_file(path, lang, names, stats)
        if old != new:
            bad.append(path)
            if not check:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new)
        if path == "wiki/collesalvetti.md":
            md = new
    with open(BUNDLE, encoding="utf-8", newline="") as f:
        old_b = f.read()
    new_b = build_bundle(old_b, md)
    if old_b != new_b:
        bad.append(BUNDLE)
        if not check:
            with open(BUNDLE, "w", encoding="utf-8", newline="") as f:
                f.write(new_b)
    if check:
        if bad:
            print("Non allineati (esegui python3 scripts/sync_docs.py):", ", ".join(bad))
            sys.exit(1)
        print("Documenti allineati a data/stats.json")
    else:
        print("Aggiornati:", ", ".join(bad) if bad else "nessuno (gia' allineati)")


if __name__ == "__main__":
    main()
