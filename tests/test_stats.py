#!/usr/bin/env python3
"""
Test di coerenza dei conteggi (solo libreria standard).

    python3 -m unittest tests.test_stats -v      # oppure: python3 tests/test_stats.py

Verifica che:
  (a) i conteggi ricalcolati in modo indipendente dal KML coincidano con
      data/network_data.json e data/stats.json;
  (b) la somma delle ripartizioni sia uguale al totale;
  (c) nessuna cifra citata nei Markdown, nei CSV/XLSX o nei log dei rilievi diverga dai dati.
"""

import csv
import json
import math
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))


def p(*parts):
    return os.path.join(ROOT, *parts)


def load_json(rel):
    with open(p(rel), encoding="utf-8") as f:
        return json.load(f)


def read(rel):
    with open(p(rel), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- parser KML indipendente
FRAZ_BY_LETTER = {"C": "Collesalvetti", "V": "Vicarello", "S": "Stagno", "G": "Guasticce"}
RE_ARLO = re.compile(r"^([CVSG]) \[[^\]]+\] ARLO$")
RE_ARL = re.compile(r"^([CVSG]) \[[^\]]+\] ARL$")
RE_CENTRALE = re.compile(r"^Centrale (Comunale|di Frazione|Feeder)(?: \((.+)\))?$")


def strip_ns(tag):
    return tag.rsplit("}", 1)[-1]


def kml_summary(rel):
    """Conta direttamente dal KML, senza usare scripts/kml_to_geojson.py."""
    root = ET.parse(p(rel)).getroot()
    out = {"points": 0, "lines": 0, "polygons": 0, "arl": {}, "arlo": {},
           "centrali": {}, "feeder": 0, "length_km": 0.0, "placemarks": 0}
    for pm in root.iter():
        if strip_ns(pm.tag) != "Placemark":
            continue
        out["placemarks"] += 1
        name = ""
        geom = None
        for ch in pm:
            t = strip_ns(ch.tag)
            if t == "name":
                name = (ch.text or "").strip()
            elif t in ("Point", "LineString", "Polygon"):
                geom = t
                coords_el = next(e for e in ch.iter() if strip_ns(e.tag) == "coordinates")
                coords = [tuple(float(v) for v in c.split(",")[:2]) for c in coords_el.text.split()]
        if geom == "Point":
            out["points"] += 1
            m = RE_ARLO.match(name)
            if m:
                out["arlo"][FRAZ_BY_LETTER[m.group(1)]] = out["arlo"].get(FRAZ_BY_LETTER[m.group(1)], 0) + 1
            m = RE_ARL.match(name)
            if m:
                out["arl"][FRAZ_BY_LETTER[m.group(1)]] = out["arl"].get(FRAZ_BY_LETTER[m.group(1)], 0) + 1
            m = RE_CENTRALE.match(name)
            if m:
                if m.group(1) == "Feeder":
                    out["feeder"] += 1
                else:
                    fr = "Collesalvetti" if m.group(1) == "Comunale" else m.group(2)
                    out["centrali"][fr] = out["centrali"].get(fr, 0) + 1
        elif geom == "LineString":
            out["lines"] += 1
            for (lo1, la1), (lo2, la2) in zip(coords, coords[1:]):
                a = (math.sin(math.radians(la2 - la1) / 2) ** 2
                     + math.cos(math.radians(la1)) * math.cos(math.radians(la2))
                     * math.sin(math.radians(lo2 - lo1) / 2) ** 2)
                out["length_km"] += 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        elif geom == "Polygon":
            out["polygons"] += 1
    return out


class TestCountsFromKml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kml = kml_summary("data/snapshots/rilievo_snapshot3.kml")
        cls.net = load_json("data/network_data.json")
        cls.stats = load_json("data/stats.json")

    def test_feature_counts_match_kml(self):
        k, f = self.kml, self.stats["features"]
        self.assertEqual(k["placemarks"], len(self.net["features"]))
        self.assertEqual((k["points"], k["lines"], k["polygons"]),
                         (f["points"], f["lines"], f["polygons"]))
        self.assertEqual(f["points"] + f["lines"] + f["polygons"], f["total"])
        self.assertEqual(f["total"], len(self.net["features"]))

    def test_length_matches_kml(self):
        # 25 linee con arrotondamento a 3 decimali ciascuna: tolleranza 0.02 km
        self.assertAlmostEqual(self.kml["length_km"], self.stats["length_km"]["total"], delta=0.02)

    def test_equipment_matches_kml(self):
        k, e = self.kml, self.stats["equipment"]
        c = e["by_category_municipal"]
        self.assertEqual(sum(k["arl"].values()), c["arl"])
        self.assertEqual(sum(k["arlo"].values()), c["arlo"])
        self.assertEqual(k["feeder"], e["total_external"])
        self.assertEqual(sum(k["centrali"].values()),
                         c["centrale_comunale"] + c["centrale_frazione"])
        self.assertEqual(sum(k["arl"].values()) + sum(k["arlo"].values()) + sum(k["centrali"].values()),
                         e["total_municipal"])
        self.assertEqual(e["total_municipal"] + e["total_external"], e["total_all"])

    def test_equipment_by_frazione_matches_kml(self):
        """Armadi: frazione dalla lettera del nome (C/V/S/G). Le centrali di frazione non hanno la
        frazione nel KML (il convertitore la assegna per bounding box): se ne verifica solo il totale."""
        k, e = self.kml, self.stats["equipment"]["by_frazione_municipal"]
        for fr in set(k["arl"]) | set(k["arlo"]):
            self.assertEqual(k["arl"].get(fr, 0), e[fr]["arl"], fr)
            self.assertEqual(k["arlo"].get(fr, 0), e[fr]["arlo"], fr)
        for fr, v in e.items():
            if fr not in FRAZ_BY_LETTER.values():
                self.assertEqual((v["arl"], v["arlo"]), (0, 0), fr)
        self.assertEqual(sum(v["centrali"] for v in e.values()), sum(k["centrali"].values()))

    def test_network_data_matches_stats_recomputed(self):
        import compute_stats
        self.assertEqual(compute_stats.compute(self.net), self.stats)


class TestBreakdownSums(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = load_json("data/stats.json")

    def test_sums(self):
        s, e = self.s, self.s["equipment"]
        self.assertEqual(sum(e["by_category_municipal"].values()), e["total_municipal"])
        self.assertEqual(sum(v["totale"] for v in e["by_frazione_municipal"].values()), e["total_municipal"])
        for fr, v in e["by_frazione_municipal"].items():
            self.assertEqual(v["arl"] + v["arlo"] + v["centrali"], v["totale"], fr)
        self.assertEqual(sum(s["features"]["by_category"].values()), s["features"]["total"])
        self.assertEqual(e["cabinets_municipal"] + e["centrali_municipal"], e["total_municipal"])
        self.assertAlmostEqual(sum(s["length_km"]["by_frazione"].values()), s["length_km"]["total"], places=3)

    def test_js_mirror_is_in_sync(self):
        text = read("js/stats.js")
        payload = text.split("window.FTTH_STATS = ", 1)[1].rstrip().rstrip(";")
        self.assertEqual(json.loads(payload), self.s)


class TestDocuments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = load_json("data/stats.json")
        cls.e = cls.s["equipment"]
        cls.f = cls.s["features"]
        cls.km_it = f"{cls.s['length_km']['total']:.3f}".replace(".", ",")
        cls.km_en = f"{cls.s['length_km']['total']:.3f}"

    def test_auto_blocks_and_wiki_bundle_in_sync(self):
        import sync_docs
        for path, (lang, names) in sync_docs.TARGETS.items():
            old, new = sync_docs.sync_file(p(path), lang, names, self.s)
            self.assertEqual(old, new, f"{path}: blocco AUTO-STATS non allineato (python3 scripts/sync_docs.py)")
        md = read("wiki/collesalvetti.md")
        self.assertEqual(sync_docs.build_bundle(read("wiki/articles_data.js"), md),
                         read("wiki/articles_data.js"), "wiki/articles_data.js non rigenerato")

    def assertQuotes(self, rel, pattern, expected, flags=0):
        found = re.findall(pattern, read(rel), flags)
        self.assertTrue(found, f"{rel}: nessuna occorrenza di /{pattern}/")
        for v in found:
            self.assertEqual(str(v), str(expected), f"{rel}: /{pattern}/ = {v}, atteso {expected}")

    def test_hand_written_figures(self):
        f, e = self.f, self.e
        self.assertQuotes("wiki/collesalvetti.md", r"Rilievo GIS di campo: (\d+) feature", f["total"])
        self.assertQuotes("wiki/collesalvetti.md", r"([\d,]+) km di tracciato", self.km_it)
        self.assertQuotes("wiki/collesalvetti.md", r"km di tracciato, (\d+) apparati", e["total_municipal"])
        self.assertQuotes("wiki/collesalvetti.md", r"\| \*\*Totale Feature Geospaziali\*\* \| [^|]+ \| [^|]+ \| \*\*(\d+)\*\*", f["total"])
        self.assertQuotes("wiki/collesalvetti.md", r"\| \*\*Elementi Puntuali[^|]*\| [^|]+ \| [^|]+ \| \*\*(\d+)\*\*", f["points"])
        self.assertQuotes("wiki/collesalvetti.md", r"\| \*\*Elementi Lineari[^|]*\| [^|]+ \| [^|]+ \| \*\*(\d+)\*\*", f["lines"])
        self.assertQuotes("wiki/collesalvetti.md", r"\| \*\*Elementi Areali[^|]*\| [^|]+ \| [^|]+ \| \*\*(\d+)\*\*", f["polygons"])
        self.assertQuotes("wiki/collesalvetti.md", r"\| \*\*Chilometri Totali Tracciati\*\* \| [^|]+ \| [^|]+ \| \*\*([\d,]+) km", self.km_it)
        self.assertQuotes("README.md", r"\*\*Feature Geospaziali Totali\*\* \| \*\*(\d+)\*\*", f["total"])
        self.assertQuotes("README.md", r"(\d+) punti, \d+ linee, \d+ poligoni", f["points"])
        self.assertQuotes("README.md", r"\d+ punti, (\d+) linee, \d+ poligoni", f["lines"])
        self.assertQuotes("README.md", r"\d+ punti, \d+ linee, (\d+) poligoni", f["polygons"])
        self.assertQuotes("README.md", r"\*\*Estensione Tracciati Rete\*\* \| \*\*([\d,]+) km", self.km_it)
        self.assertQuotes("README_EN.md", r"\*\*Total Geospatial Features\*\* \| \*\*(\d+)\*\*", f["total"])
        self.assertQuotes("README_EN.md", r"(\d+) point elements, \d+ line traces, \d+ area polygons", f["points"])
        self.assertQuotes("README_EN.md", r"\d+ point elements, (\d+) line traces, \d+ area polygons", f["lines"])
        self.assertQuotes("README_EN.md", r"\d+ point elements, \d+ line traces, (\d+) area polygons", f["polygons"])
        self.assertQuotes("README_EN.md", r"\*\*Total Mapped Route Length\*\* \| \*\*([\d.]+) km", self.km_en)
        self.assertQuotes("docs/HANDOFF_REDESIGN.md", r"sono (\d+) feature, [\d,]+ km, \d+ apparati", f["total"])
        self.assertQuotes("docs/HANDOFF_REDESIGN.md", r"sono \d+ feature, ([\d,]+) km, \d+ apparati", self.km_it)
        self.assertQuotes("docs/HANDOFF_REDESIGN.md", r"sono \d+ feature, [\d,]+ km, (\d+) apparati", e["total_municipal"])
        chg = read("data/snapshots/CHANGELOG_DATI.md").split("## Snapshot 2", 1)[0]
        self.assertEqual(re.findall(r"Feature totali censite:\*\* \*\*(\d+)\*\* \((\d+) punti, (\d+) linee, (\d+) poligoni\)", chg),
                         [tuple(str(x) for x in (f["total"], f["points"], f["lines"], f["polygons"]))])
        self.assertQuotes("data/snapshots/CHANGELOG_DATI.md", r"Apparati censiti \(Snapshot 3\):\*\* \*\*(\d+)\*\* nel territorio comunale", e["total_municipal"])

    def test_no_stale_equipment_counts_in_markdown(self):
        """Qualsiasi 'N apparati' nei documenti correnti deve valere il totale comunale (o con esterni)."""
        allowed = {str(self.e["total_municipal"]), str(self.e["total_all"])}
        for rel in ("README.md", "README_EN.md", "wiki/collesalvetti.md", "docs/HANDOFF_REDESIGN.md"):  # APPARATI_RECOUNT.md cita di proposito i vecchi valori
            for n, line in enumerate(read(rel).splitlines(), 1):
                if re.search(r"snapshot [12]\b|prima|before|storic|historical", line, re.I):
                    continue
                for v in re.findall(r"(?<![+\d])\b(\d+) (?:apparati|equipment items)", line):
                    self.assertIn(v, allowed, f"{rel}:{n}: '{v} apparati' non coincide con i dati")

    def test_historic_snapshot_figures_match_kml(self):
        log = read("data/snapshots/CHANGELOG_DATI.md")
        for n in (1, 2):
            k = kml_summary(f"data/snapshots/rilievo_snapshot{n}.kml")
            sect = log.split(f"## Snapshot {n}", 1)[1].split("\n## ", 1)[0]
            m = re.search(r"Feature totali censite:\*\* \*\*(\d+)\*\* \((\d+) punti, (\d+) linee, (\d+) poligoni\)", sect)
            self.assertEqual(tuple(int(x) for x in m.groups()),
                             (k["placemarks"], k["points"], k["lines"], k["polygons"]), f"Snapshot {n}")
        w = read("wiki/collesalvetti.md")
        for n, col in ((1, 0), (2, 1)):
            k = kml_summary(f"data/snapshots/rilievo_snapshot{n}.kml")
            for label, key in (("Totale Feature Geospaziali", "placemarks"), ("Elementi Puntuali", "points"),
                               ("Elementi Lineari", "lines"), ("Elementi Areali", "polygons")):
                row = re.search(rf"\| \*\*{label}[^|]*\| ([^|]+) \| ([^|]+) \|", w)
                self.assertEqual(int(row.group(col + 1).strip()), k[key], f"wiki Snapshot {n} {label}")
            row = re.search(r"\| \*\*di cui Apparati[^|]*\| ([^|]+) \| ([^|]+) \| \*\*(\d+)\*\*", w)
            self.assertEqual(int(row.group(col + 1).strip()),
                             sum(k["arl"].values()) + sum(k["arlo"].values()) + sum(k["centrali"].values()),
                             f"wiki Snapshot {n} apparati")


class TestExports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = load_json("data/stats.json")

    def _check_csv(self, rel, delimiter, encoding):
        with open(p(rel), encoding=encoding, newline="") as fh:
            rows = list(csv.DictReader(fh, delimiter=delimiter))
        self.assertEqual(len(rows), self.s["features"]["total"], rel)
        from collections import Counter
        tip = Counter(r["Tipologia"] for r in rows if r["Tipo Geometria"].lower().startswith("point") or r["Tipo Geometria"].lower().startswith("punt"))
        e = self.s["equipment"]["by_category_municipal"]
        self.assertEqual(tip.get("ARL (Rame)", 0), e["arl"], rel)
        self.assertEqual(tip.get("ARLO (Ottico FiberCop)", 0), e["arlo"], rel)
        self.assertEqual(tip.get("Centrale Telecom (Sede OLT)", 0), e["centrale_comunale"], rel)
        self.assertEqual(tip.get("Centrale di Frazione", 0), e["centrale_frazione"], rel)
        self.assertEqual(sum(tip.values()), self.s["features"]["points"], rel)

    def test_csv_standard(self):
        self._check_csv("data/rete_ftth_collesalvetti_standard.csv", ",", "utf-8")

    def test_csv_excel_it(self):
        self._check_csv("data/rete_ftth_collesalvetti_excel_it.csv", ";", "utf-8-sig")

    def test_xlsx_rows(self):
        with zipfile.ZipFile(p("data/rete_ftth_collesalvetti.xlsx")) as z:
            xml = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
        self.assertEqual(xml.count("<row "), self.s["features"]["total"] + 1)  # + intestazione


if __name__ == "__main__":
    unittest.main(verbosity=2)
