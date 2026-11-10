#!/usr/bin/env python3
"""Build the static acts archive from published PDFs and an optional Albo inbox."""

import argparse
from collections import defaultdict
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data/ordinanze"
PUBLIC_PDFS = ARCHIVE / "pdf"
MAX_BYTES = 2 * 1024 * 1024
DATE = r"\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2})\b"
NUMBER = r"n(?:r|umero)?\s*[.°º]?\s*"
REGISTRY = rf"\b(?:registro|reg\.?)\s+(?:generale|gen\.?)\s*{NUMBER}(\d+)(?:\s+del\s+({DATE}))?"
OPERATORS = {
    "FiberCop": r"fiber\s*cop", "Fastweb": r"fast\s*web", "TIM": r"tim|telecom\s+italia",
    "Open Fiber": r"open\s*fiber", "WindTre": r"wind\s*tre|wind",
    "Estracom": r"estracom", "Ultranet": r"ultranet",
}
AREAS = ("STAGNO", "VICARELLO", "GUASTICCE", "NUGOLA", "COLLESALVETTI")
STREET = r"\b(?:via(?:le)?|piazza|piazzale|vicolo|corso|strada comunale)\s+[^,;:()–—\n]+"
ROAD = r"\b(?:S\.?\s*[PRS]\.?\s*(?:n\.?\s*)?0*\d{1,3}|strada\s+(?:provinciale|regionale|statale)\s+(?:n\.?\s*)?0*\d{1,3})\b"


def find(pattern, text):
    return re.search(pattern, text, re.IGNORECASE)


def iso(value):
    if value:
        day, month, year = map(int, re.split(r"[/.-]", value))
        try:
            return date(year + 2000 if year < 100 else year, month, day).isoformat()
        except ValueError:
            pass
    return None


def key(value):
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return " ".join(re.findall(r"[a-z0-9]+", ascii_value.lower()))


def extract_text(path):
    # Layout retains headings, bullet rows and form-feed page boundaries.
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        capture_output=True, encoding="utf-8", timeout=90,
    )
    if result.returncode:
        raise ValueError(f"{path.name}: {result.stderr.strip()}")
    return result.stdout


def streets(text):
    found = {}
    segments = re.split(r"\s+(?:-|e|ed|angolo)\s+(?=(?:via(?:le)?|piazza)\b)", text, flags=re.I)
    for match in (m for segment in segments for m in re.finditer(STREET, segment, re.I)):
        value = re.split(
            r"\s+(?:-|e$|lato\b|angolo\b|civico\b|dal\b|all.altezza\b|da\b|al\b|tra\b|per\b|"
            r"fraz\b|collesalvetti\b|stagno\b|vie\b|divieto\b|limitata\w*|interessat\w*|"
            r"int\b|snc\b|n\.\s*\d|\d+\b)",
            match[0], maxsplit=1, flags=re.I,
        )[0].strip(" .-")
        if key(value) not in {"via varie", "via", "via pec", "via mail"}:
            found.setdefault(key(value), value.title() if value.isupper() else value[0].upper() + value[1:])
    for match in re.finditer(ROAD, text, re.I):
        route = re.sub(r"strada\s+provinciale|strada\s+regionale|strada\s+statale",
                       lambda m: {"p": "SP", "r": "SR", "s": "SS"}[m[0].split()[1][0].lower()], match[0], flags=re.I)
        route = re.sub(r"[.\s]", "", route.upper()).replace("N", "")
        route = re.sub(r"^([A-Z]+)0+(?=\d)", r"\1", route)
        found[route.lower()] = route
    return list(found.values())


def parse(text, digest, source_entity):
    flat = " ".join(text.split())
    subject_match = re.search(r"(?im)^\s*oggetto\s*:", text)
    header = " ".join(text[:subject_match.start()].split()) if subject_match else ""
    subject = ""
    if subject_match:
        subject = re.split(r"\n\s*\n", text[subject_match.end():].lstrip(), maxsplit=1)[0]
        subject = " ".join(subject.split())
    registry = find(REGISTRY, header)
    heading = find(rf"(?<![\w.]){NUMBER}(\d+)(?:/\d{{4}})?\s+del\s+({DATE})", re.sub(REGISTRY, "", header, flags=re.I))
    issued = iso(heading[2]) if heading else iso(registry[2]) if registry else None
    police = bool(find(r"polizia (?:municipale|locale)", header))
    entity = source_entity
    if find(r"\bprovincia di livorno\b", header):
        entity = "PROVINCIA_LIVORNO"
    elif find(r"\bcomune di collesalvetti\b", header):
        entity = "COMUNE_COLLESALVETTI"
    sector = "POLIZIA_LOCALE" if police else None
    if find(r"lavori pubblici|settore tecnico", header):
        sector = "LAVORI_PUBBLICI"
    elif find(r"economico.finanziar|economica finanziaria|patrimonio|tributi", header):
        sector = "PATRIMONIO_TRIBUTI"
    elif find(r"settore strategico", header):
        sector = "STRATEGICO"

    kind = "ALTRO"
    if find(r"\bproroga\b", subject):
        kind = "PROROGA"
    elif find(r"\bripristin\w*\b", subject):
        kind = "RIPRISTINO"
    elif find(r"\bordinanza\b", header):
        kind = "ORDINANZA_VIABILITA"
    elif find(r"\bconcessione\b.{0,90}\bsuolo pubblico\b", subject):
        kind = "CONCESSIONE_SUOLO"
    elif find(r"\bautorizzazione\b.{0,100}\bscav\w*", subject):
        kind = "AUTORIZZAZIONE_SCAVO"
    own_number = find(rf"\b{NUMBER}(\d+/\d{{4}})", subject) if kind in {"CONCESSIONE_SUOLO", "AUTORIZZAZIONE_SCAVO"} else None
    number = own_number[1] if own_number else f"{heading[1]}/{issued[:4]}" if heading and issued else None
    entity_code = {"COMUNE_COLLESALVETTI": "COLLE", "PROVINCIA_LIVORNO": "PROVLI"}.get(entity)
    record_id = f"DOC-{digest[:16]}"
    if entity_code and issued and number:
        series = "PM" if police else kind
        record_id = f"{series}-{entity_code}-{'ORD-' if police else ''}{number.replace('/', '-')}"

    # Extract the operative clause. Dates in the preamble often refer to
    # older authorizations, unrelated laws, or the application itself.
    operative = re.split(r"(?im)^\s*(?:ORDINA|DISPONE|DETERMINA|CONCEDE)\s*$", text, maxsplit=1)
    body = " ".join(operative[-1].split()) if len(operative) > 1 else ""
    body = re.split(r"\b(?:all.albo pretorio|avverso il presente|contro il presente)\b", body, maxsplit=1, flags=re.I)[0]
    date_range = (
        rf"\b(?:dal(?:\s+giorno)?|a partire dal(?:\s+giorno)?)\s+({DATE})\s*[-–—]?\s*"
        rf"(?:al(?:\s+giorno)?|fino al(?:\s+giorno)?|e fino al termine dei lavori previsto per il)\s+({DATE})"
    )
    periods = body[:1500] if kind != "ALTRO" else ""
    if kind == "CONCESSIONE_SUOLO" and body:
        # The validity cells span several lines in the left column.
        column = [re.split(r" {2,}", line.strip(), maxsplit=1)[0] for line in operative[-1].splitlines()[:30]]
        periods = " ".join(column)
    windows = []
    for pair in re.findall(date_range, periods, re.I):
        start, end = map(iso, pair)
        if start and end and start <= end and {"dal": start, "al": end} not in windows:
            windows.append({"dal": start, "al": end})
    hours = find(
        r"\b(?:(?:dalle|tra le)\s+ore\s+|fascia oraria\s+)(\d{1,2})[:.](\d{2})\s*"
        r"(?:[-–]|alle(?:\s+ore)?|e le ore)\s*(\d{1,2})[:.](\d{2})", body[:1500]
    )
    clock = None
    if hours and all(int(hours[i]) < limit for i, limit in enumerate((24, 60, 24, 60), 1)):
        clock = f"{int(hours[1]):02}:{hours[2]} - {int(hours[3]):02}:{hours[4]}"

    protocol = find(rf"\bprot(?:ocollo)?\.?\s*(?:{NUMBER})?(\d{{3,}})(?:\s+del\s+({DATE}))?", flat)
    protocol_date = iso(protocol[2]) if protocol else None
    if protocol and not protocol_date:
        adjacent = find(rf"({DATE})\s+(?:al\s+)?{re.escape(protocol[0])}", flat)
        protocol_date = iso(adjacent[1]) if adjacent else None
    stamped = find(rf"\b(\d{{5,}})\s*-\s*(?:ingresso|uscita)\s*-\s*({DATE})", header)
    officer = re.search(r"(?i:\bsottoscritt[oa]\s+(?:(?:dott\.?ssa|dott\.?|ing\.?|arch\.?)\s+)?)([A-ZÀ-Ý][\w’'-]+\s+[A-ZÀ-Ý][\w’'-]+)", flat)
    officer_name = officer[1] if officer else None

    applicant = None
    target = None
    applicant_clause = find(r"\b(?:societ[àa]|ditta|richiedente|in favore di|per conto di)\s+([^,;]{1,100})", subject)
    request = find(r"\bistanza\b(.{0,250}?)(?:\bchiede\b|\bper\s+(?:l.occupazione|eseguire))", flat)
    for passage in (applicant_clause[1] if applicant_clause else "", subject, request[1] if request else ""):
        for operator, pattern in OPERATORS.items():
            match = find(rf"\b(?:{pattern})\b", passage)
            if match and (applicant is None or (operator == "Fastweb" and applicant == "FiberCop")):
                applicant = operator
    if applicant:
        target = "FiberCop" if find(r"\bfiber\s*cop\b", subject) else applicant

    location_text = re.sub(r"\bcomune di collesalvetti\b", "", subject, flags=re.I).replace("COLLESLVETTI", "COLLESALVETTI")
    area = next((area for area in AREAS if find(rf"\b{area}\b", location_text)), None)
    if not area and find(ROAD, location_text):
        area = "EXTRAURBANO"
    # Prefer the subject and operative bullet headings to incidental addresses.
    street_lines = re.findall(
        r"(?im)^[^\S\n]*[•●–-][^\S\n]*(?:in )?((?:via(?:le)?|piazza|S\.?\s*[PR]\.?\s*\d)[^\n:]{1,100})",
        operative[-1] if body and kind != "ALTRO" else "",
    )
    street_text = "\n".join([subject, *street_lines])
    km = find(r"\b(?:dal\s+)?km\.?\s*(\d+(?:[+,.]\d+)?).*?\b(?:al\s+)?km\.?\s*(\d+(?:[+,.]\d+)?)", subject)
    km_pair = None
    if km:
        values = [float(v.replace("+", ".").replace(",", ".")) for v in km.groups()]
        if values[0] <= values[1]:
            km_pair = dict(zip(("dal_km", "al_km"), values))

    refs = {}
    preamble = " ".join(operative[0][subject_match.end():].split()) if subject_match else ""
    for match in re.finditer(
        rf"\b(autorizzazione(?: tecnica)?|ordinanza(?: di polizia municipale)?|concessione(?: (?:di )?suolo)?)"
        rf"[^;:.\d]{{0,100}}?\s*{NUMBER}(\d+)(?:/(\d{{4}}))?"
        rf"(?:[^;]{{0,90}}?\b(?:del|in data|il)\s+({DATE}))?",
        preamble, re.I,
    ):
        kind_ref = match[1].split()[0].upper()
        date_ref = iso(match[4])
        year = match[3] or (date_ref[:4] if date_ref else None)
        own_type = {"AUTORIZZAZIONE_SCAVO": "AUTORIZZAZIONE", "CONCESSIONE_SUOLO": "CONCESSIONE"}.get(
            kind, "ORDINANZA" if police else None
        )
        if year and (number, own_type) != (f"{match[2]}/{year}", kind_ref):
            authority = "PROVINCIA_LIVORNO" if find(r"provincia di livorno", match[0]) else entity
            refs[(kind_ref, match[2], year, authority)] = {
                "tipo": kind_ref, "numero": f"{match[2]}/{year}", "data": date_ref, "ente": authority,
            }
    return {
        "id": record_id, "ente": entity, "settore": sector, "funzionario": officer_name,
        "tipologia": kind, "numero_atto": number, "registro_generale": registry[1] if registry else None,
        "data_emissione": issued, "data_registrazione": iso(registry[2]) if registry else iso(stamped[2]) if stamped else None,
        "protocollo": protocol[1] if protocol else stamped[1] if stamped else None,
        "data_protocollo": protocol_date or (iso(stamped[2]) if stamped and not protocol else None),
        "oggetto": subject or None, "richiedente": applicant, "operator_target": target,
        "validita": {
            **(windows[0] if len(windows) == 1 else {"dal": None, "al": None}),
            "orario": clock,
            **({"periodi": windows} if len(windows) > 1 else {}),
        },
        "localizzazione": {"area": area, "strade": streets(street_text), "prog_chilometrica": km_pair},
        "riferimenti": list(refs.values()), "ocr_required": len(re.findall(r"\w", flat)) < 80,
        "stato_opera": None,
    }


def merge(record, correction):
    for field, value in correction.items():
        if isinstance(value, dict) and isinstance(record.get(field), dict):
            merge(record[field], value)
        else:
            record[field] = value


def connect(records, network):
    series = {"AUTORIZZAZIONE_SCAVO": "AUTORIZZAZIONE", "CONCESSIONE_SUOLO": "CONCESSIONE"}
    refs_by_number = defaultdict(list)
    for act in records:
        if act["numero_atto"]:
            kind = series.get(act["tipologia"], "ORDINANZA" if act["settore"] == "POLIZIA_LOCALE" else None)
            if kind:
                refs_by_number[kind, act["ente"], act["numero_atto"]].append(act["id"])
    for act in records:
        parents = set(act.get("atti_collegati", []))
        for ref in act["riferimenti"]:
            matching = refs_by_number[ref["tipo"], ref["ente"], ref["numero"]]
            if len(matching) == 1 and matching[0] != act["id"]:
                ref["atto_id"] = matching[0]
                parents.add(matching[0])
        act["atti_collegati"] = sorted(parents)

    # Group a chain by its explicit technical authorization, scoped to
    # the issuing entity and area. Reviewed lot IDs can replace the key.
    for act in records:
        area = act["localizzazione"]["area"]
        refs = {(r["ente"], r["numero"]) for r in act["riferimenti"]
                if r["tipo"] == "AUTORIZZAZIONE" and r["ente"]}
        if act["tipologia"] == "AUTORIZZAZIONE_SCAVO" and act["ente"] and act["numero_atto"]:
            refs.add((act["ente"], act["numero_atto"]))
        if area and len(refs) == 1 and not act.get("cluster_id"):
            ente, number = refs.pop()
            act["cluster_id"] = f"AUT-{ente}-{area}-{number.replace('/', '-')}"
    by_act = {act["id"]: act for act in records}
    for act in records:
        for parent_id in act["atti_collegati"]:
            if parent_id not in by_act:
                raise ValueError(f"{act['id']}: unknown related act {parent_id}")
            parent = by_act[parent_id]
            if parent.get("cluster_id") and not act.get("cluster_id"):
                act["cluster_id"] = parent["cluster_id"]

    features = defaultdict(list)
    street_features = defaultdict(set)
    by_id = {}
    for feature in network["features"]:
        props = feature["properties"]
        geometry = feature["geometry"]["type"]
        if geometry not in {"LineString", "MultiLineString"} and not (
            geometry == "Point" and props.get("category") == "arlo"
        ):
            continue
        ident = feature["id"]
        by_id[ident] = feature
        site = props.get("cantiere") or {}
        if site.get("id_ordinanza"):
            features[site["id_ordinanza"]].append(ident)
        # Only use the leading explicit P.M. reference, never registry numbers
        # or other references embedded in notes.
        code = site.get("codice_ordinanza") or props.get("ordinanza") or ""
        number = find(rf"^ordinanza\s+p\.?m\.?\s*{NUMBER}(\d+)(?:/(\d{{4}})|\s+del\s+\d{{1,2}}/\d{{1,2}}/(\d{{4}}))", code)
        if number:
            features[f"PM-COLLE-ORD-{number[1]}-{number[2] or number[3]}"].append(ident)
        extension = find(rf"\bproroga\s+ord\.\s*{NUMBER}(\d+)(?:/(\d{{4}})|\s+del\s+\d{{1,2}}/\d{{1,2}}/(\d{{4}}))", code)
        if extension:
            features[f"PM-COLLE-ORD-{extension[1]}-{extension[2] or extension[3]}"].append(ident)
        for street in site.get("vie_interessate", []):
            name = re.split(r"\s*\(|\s+(?:nord|sud|est|ovest)$", street, maxsplit=1, flags=re.I)[0]
            street_features[key(props.get("frazione", "")), key(name)].add(ident)

    for act in records:
        loc = act["localizzazione"]
        verified = set(features[act["id"]]) | set(loc.get("matched_feature_ids", []))
        if verified - by_id.keys():
            raise ValueError(f"{act['id']}: unknown map features {sorted(verified - by_id.keys())}")
        candidates = set()
        for street in loc["strade"]:
            candidates.update(street_features[key(loc["area"] or ""), key(street)])
        loc["matched_feature_ids"] = sorted(verified)
        loc["candidate_feature_ids"] = sorted(candidates - verified)


def atomic_write(path, data):
    if path.exists() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        stream.write(data)
    Path(stream.name).replace(path)
    path.chmod(0o644)


def payload(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def canonical_name(act, digest):
    types = {
        "ORDINANZA_VIABILITA": "ORD", "CONCESSIONE_SUOLO": "CONC",
        "AUTORIZZAZIONE_SCAVO": "AUT", "PROROGA": "PROR", "RIPRISTINO": "RIP",
    }
    entity = {"COMUNE_COLLESALVETTI": "COLLE", "PROVINCIA_LIVORNO": "PROVLI"}.get(act["ente"], "ND")
    number = act["numero_atto"] or act["registro_generale"] or digest[:12]
    parts = [act["data_emissione"] or "UNDATED", entity, types.get(act["tipologia"], "ATTO"),
             number.split("/")[0], key(act["richiedente"] or "ND").title().replace(" ", ""),
             (act["localizzazione"]["area"] or "ND").title()]
    return "_".join(parts) + ".pdf"


def run(args):
    overrides = json.loads((ARCHIVE / "overrides.json").read_text(encoding="utf-8"))
    network = json.loads((ROOT / "data/network_data.json").read_text(encoding="utf-8"))
    sources = sorted(ARCHIVE.glob("*.pdf")) + sorted(PUBLIC_PDFS.glob("*.pdf"))
    if args.import_dir:
        if not args.import_dir.is_dir():
            raise ValueError(f"Inbox not found: {args.import_dir}")
        sources.extend(sorted(
            (p for p in args.import_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"),
            key=lambda path: (" (" in path.name, str(path)),
        ))
    seen, seen_ids, names = set(), set(), set()
    records, texts, copies = [], {}, []
    for path in sources:
        published = path.parent in (ARCHIVE, PUBLIC_PDFS)
        if path.stat().st_size > MAX_BYTES:
            if published:
                raise ValueError(f"Published PDF exceeds the size limit: {path.name}")
            print(f"Retained in inbox (> 2 MiB): {path.name}")
            continue
        data = path.read_bytes()
        digest = sha256(data).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)
        text = extract_text(path)
        source_entity = None if published else args.ente
        # Preserve provenance of already published files on subsequent runs.
        if not source_entity:
            if path.name.split("_")[1:2] == ["PROVLI"]:
                source_entity = "PROVINCIA_LIVORNO"
            elif path.parent == ARCHIVE or path.name.split("_")[1:2] == ["COLLE"]:
                source_entity = "COMUNE_COLLESALVETTI"
        act = parse(text, digest, source_entity)
        merge(act, overrides.get(act["id"], {}))
        if act["id"] in seen_ids:
            # A second copy of the same numbered act can contain a different
            # stamp or scan layer. Keep the published representative.
            print(f"Same numbered act {act['id']}: {path.name}")
            continue
        seen_ids.add(act["id"])
        if published:
            destination = path
        else:
            name = canonical_name(act, digest)
            if name in names:
                name = f"{Path(name).stem}_{digest[:12]}.pdf"
            destination = PUBLIC_PDFS / name
            copies.append((destination, data))
        names.add(destination.name)
        relative = destination.relative_to(ARCHIVE).as_posix()
        act["file_pdf"] = {"nome_file": relative, "url_path": "data/ordinanze/" + quote(relative)}
        records.append(act)
        texts[act["id"]] = " ".join(text.split()) if not act["ocr_required"] else ""

    if missing := overrides.keys() - seen_ids:
        raise ValueError(f"Overrides refer to missing documents: {', '.join(sorted(missing))}")
    records.sort(key=lambda r: (r["data_emissione"] or "", r["id"]), reverse=True)
    connect(records, network)
    index = payload(records)
    search = payload(dict(sorted(texts.items())))
    outputs = {
        ARCHIVE / "ordinanze.json": index,
        ROOT / "public/data/ordinanze.json": index,
        ARCHIVE / "testo.json": search,
        ARCHIVE / "offline.js": b"window.ARCHIVIO_ATTI = " + index.rstrip() +
            b";\nwindow.ARCHIVIO_TESTI = " + search.rstrip() + b";\n",
    }
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, data in outputs.items() if not p.exists() or p.read_bytes() != data]
        if copies or stale:
            raise ValueError("Archive needs regeneration: " + ", ".join(stale or ["new PDFs"]))
    else:
        for path, data in [*copies, *outputs.items()]:
            atomic_write(path, data)
    print(f"{len(records)} records, {sum(r['ocr_required'] for r in records)} require OCR, {len(copies)} new PDFs")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--import-dir", type=lambda p: Path(p).resolve())
    parser.add_argument("--ente", choices=("COMUNE_COLLESALVETTI", "PROVINCIA_LIVORNO"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not shutil.which("pdftotext"):
        parser.error("Install Poppler (pdftotext) before running ingestion.")
    try:
        run(args)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
