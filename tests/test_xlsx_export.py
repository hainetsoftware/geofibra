#!/usr/bin/env python3
"""
Test di integrità e correttezza per l'esportazione Excel (data/rete_ftth_collesalvetti.xlsx).
Verifica:
1. Integrità del pacchetto OOXML/ZIP e validità sintattica XML di tutti i componenti.
2. Nomi dei fogli conformi (max 31 caratteri, nessun carattere vietato, unici).
3. Coerenza dei conteggi e totali con data/network_data.json e data/stats.json.
4. Assenza di formula injection (=, +, -, @ non intenzionali o non quotati).
5. Assenza di caratteri di controllo non validi XML e rispetto dei limiti dimensionali.
6. Presenza e correttezza del foglio informativo (README / Info).
7. Congruenza dell'intervallo autofilter e freeze pane.
"""

import json
import os
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def p(rel):
    return os.path.join(BASE_DIR, rel)

class TestXlsxExport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xlsx_path = p("data/rete_ftth_collesalvetti.xlsx")
        cls.json_path = p("data/network_data.json")
        cls.stats_path = p("data/stats.json")

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.net_data = json.load(f)

        if os.path.exists(cls.stats_path):
            with open(cls.stats_path, "r", encoding="utf-8") as f:
                cls.stats_data = json.load(f)
        else:
            cls.stats_data = None

    def test_file_exists_and_valid_zip(self):
        """Verifica che il file esista e sia un archivio ZIP valido."""
        self.assertTrue(os.path.exists(self.xlsx_path), "File XLSX non trovato")
        self.assertTrue(zipfile.is_zipfile(self.xlsx_path), "Il file non è un archivio zip valido")

    def test_xml_parts_well_formed(self):
        """Verifica che ogni file XML interno al pacchetto OOXML sia ben formato e parsabile."""
        with zipfile.ZipFile(self.xlsx_path, "r") as zf:
            namelist = zf.namelist()
            expected_parts = [
                "[Content_Types].xml",
                "_rels/.rels",
                "xl/workbook.xml",
                "xl/_rels/workbook.xml.rels",
                "xl/styles.xml",
                "xl/worksheets/sheet1.xml",
                "xl/worksheets/sheet2.xml"
            ]
            for part in expected_parts:
                self.assertIn(part, namelist, f"Manca il componente atteso {part} nel pacchetto XLSX")

            for name in namelist:
                if name.endswith(".xml") or name.endswith(".rels"):
                    content = zf.read(name)
                    try:
                        ET.fromstring(content)
                    except ET.ParseError as err:
                        self.fail(f"Componente {name} non ben formato: {err}")

    def test_sheet_names_validity(self):
        """Verifica che i nomi dei fogli rispettino le specifiche Excel (max 31 caratteri, caratteri ammessi)."""
        forbidden_chars = {'[', ']', ':', '*', '?', '/', '\\'}
        with zipfile.ZipFile(self.xlsx_path, "r") as zf:
            root = ET.fromstring(zf.read("xl/workbook.xml"))
            ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            sheets = root.findall(".//s:sheet", ns)
            self.assertGreaterEqual(len(sheets), 1, "Il workbook deve contenere almeno un foglio")

            seen_names = set()
            for s in sheets:
                name = s.get("name")
                self.assertIsNotNone(name, "Nome foglio non definito")
                self.assertLessEqual(len(name), 31, f"Nome foglio '{name}' supera 31 caratteri ({len(name)})")
                self.assertFalse(any(c in forbidden_chars for c in name),
                                 f"Nome foglio '{name}' contiene caratteri non ammessi")
                self.assertNotIn(name.lower(), seen_names, f"Nome foglio duplicato (case-insensitive): {name}")
                seen_names.add(name.lower())

    def test_row_counts_and_features_match(self):
        """Verifica che il numero di righe di sheet1 corrisponda al numero di feature in network_data.json."""
        with zipfile.ZipFile(self.xlsx_path, "r") as zf:
            root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
            ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            rows = root.findall(".//s:row", ns)
            
            # Riga 1 = intestazioni, rimanenti = record dati
            header_row = rows[0]
            data_rows = rows[1:]
            
            expected_total = len(self.net_data["features"])
            self.assertEqual(len(data_rows), expected_total,
                             f"Numero di righe dati ({len(data_rows)}) non corrisponde a feature JSON ({expected_total})")

            # Verifica intestazioni: 19 colonne
            headers = [c.find(".//s:t", ns).text for c in header_row.findall("s:c", ns)]
            self.assertEqual(len(headers), 19, f"Numero intestazioni inatteso: {len(headers)}")
            self.assertEqual(headers[0], "ID")
            self.assertEqual(headers[1], "Nome Apparato")

    def test_equipment_figures_match_stats(self):
        """Verifica che i dati di conteggio apparati nel foglio INFO corrispondano a stats.json."""
        if not self.stats_data:
            self.skipTest("stats.json non presente")

        with zipfile.ZipFile(self.xlsx_path, "r") as zf:
            root = ET.fromstring(zf.read("xl/worksheets/sheet2.xml"))
            ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            
            info_dict = {}
            for row in root.findall(".//s:row", ns):
                cells = row.findall("s:c", ns)
                if not cells:
                    continue
                k_el = cells[0].find(".//s:t", ns)
                key = k_el.text if k_el is not None else ""
                val = ""
                if len(cells) > 1:
                    v_el = cells[1].find("s:v", ns)
                    t_el = cells[1].find(".//s:t", ns)
                    val = v_el.text if v_el is not None else (t_el.text if t_el is not None else "")
                if key:
                    info_dict[key] = val

            eq_stats = self.stats_data.get("equipment", {})
            self.assertEqual(int(info_dict.get("Armadi comunali (ARL + ARLO)", -1)), eq_stats.get("cabinets_municipal"))
            self.assertEqual(int(info_dict.get("Centrali comunali (Telecom Sede OLT + Frazione)", -1)), eq_stats.get("centrali_municipal"))
            self.assertEqual(int(info_dict.get("Totale apparati nel territorio comunale", -1)), eq_stats.get("total_municipal"))
            self.assertEqual(int(info_dict.get("Apparati di raccordo esterno (Feeder)", -1)), eq_stats.get("total_external"))
            self.assertEqual(int(info_dict.get("Totale feature rilevate", -1)), len(self.net_data["features"]))

    def test_no_formula_injection_and_no_control_chars(self):
        """Verifica che nessuna cella contenga injection formule (=, +, -, @) o caratteri di controllo vietati."""
        forbidden_ctrl = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
        with zipfile.ZipFile(self.xlsx_path, "r") as zf:
            for sname in ["xl/worksheets/sheet1.xml", "xl/worksheets/sheet2.xml"]:
                root = ET.fromstring(zf.read(sname))
                ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
                for r_idx, row in enumerate(root.findall(".//s:row", ns)):
                    for c in row.findall("s:c", ns):
                        t_el = c.find(".//s:t", ns)
                        if t_el is not None and t_el.text:
                            text = t_el.text
                            # Control chars check
                            self.assertFalse(forbidden_ctrl.search(text),
                                             f"Trovato carattere di controllo in {sname} cella {c.get('r')}: {repr(text)}")
                            # Formula check (se non è formula <f>)
                            if r_idx > 0:  # Salta le intestazioni
                                self.assertFalse(
                                    text.startswith(("=", "+", "-", "@")) and not text.startswith("'"),
                                    f"Possibile formula non intenzionale o non sanificata in {sname} cella {c.get('r')}: {text}"
                                )
                            self.assertLessEqual(len(text), 32767,
                                                 f"Stringa supera il limite Excel in {sname} cella {c.get('r')}")

    def test_autofilter_and_freeze_pane(self):
        """Verifica che l'autofilter e il blocco riquadri (freeze pane) siano configurati coerentemente."""
        with zipfile.ZipFile(self.xlsx_path, "r") as zf:
            root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
            ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            
            # Freeze pane
            pane = root.find(".//s:pane", ns)
            self.assertIsNotNone(pane, "Manca la configurazione del blocco riga di intestazione (<pane>)")
            self.assertEqual(pane.get("state"), "frozen")
            self.assertEqual(pane.get("ySplit"), "1")
            
            # Autofilter range
            af = root.find(".//s:autoFilter", ns)
            self.assertIsNotNone(af, "Manca il tag <autoFilter>")
            total_rows = len(self.net_data["features"]) + 1
            expected_ref = f"A1:S{total_rows}"
            self.assertEqual(af.get("ref"), expected_ref,
                             f"L'intervallo dell'autofilter ({af.get('ref')}) non corrisponde a quello atteso ({expected_ref})")

if __name__ == "__main__":
    unittest.main(verbosity=2)
