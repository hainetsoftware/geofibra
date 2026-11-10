import json
import unittest
from urllib.parse import unquote

from scripts.parse_ordinanze import ARCHIVE, ROOT, parse


class TestOrdinanze(unittest.TestCase):
    def test_emission_and_operating_dates_are_distinct(self):
        text = """
Registro Generale nr. 125
ORDINANZA
POLIZIA MUNICIPALE
N. 118 DEL 09/11/2026

OGGETTO: FIBERCOP – COLLESALVETTI, VIE VARIE

Vista l’istanza pervenuta in data 09/11/2026 al prot.25107 con la quale la Società Fastweb Spa chiede un provvedimento.
Vista l’Autorizzazione n.28/2026 rilasciata dal Settore Tecnico in data 28/10/2026.

ORDINA

Dal giorno 16/11/2026 al giorno 04/12/2026, nella fascia oraria compresa tra le ore 8.00 e le ore 18.00:
    Via Roma: divieto di sosta
    Via del Valico a Pisa: restringimento della carreggiata
"""
        act = parse(text, "unused", "COMUNE_COLLESALVETTI")
        self.assertEqual(act["id"], "PM-COLLE-ORD-118-2026")
        self.assertEqual(act["registro_generale"], "125")
        self.assertEqual(act["protocollo"], "25107")
        self.assertEqual(act["data_protocollo"], "2026-11-09")
        self.assertEqual(act["data_emissione"], "2026-11-09")
        self.assertEqual(act["richiedente"], "Fastweb")
        self.assertEqual(act["operator_target"], "FiberCop")
        self.assertEqual(act["validita"], {"dal": "2026-11-16", "al": "2026-12-04", "orario": "08:00 - 18:00"})
        self.assertEqual(act["localizzazione"]["strade"], ["Via Roma", "Via del Valico a Pisa"])
        self.assertEqual([(ref["numero"], ref["data"]) for ref in act["riferimenti"]], [("28/2026", "2026-10-28")])

    def test_publication_footer_does_not_supply_worksite_dates(self):
        act = parse("""
Registro Generale n. 994 del 12/10/2026
DETERMINAZIONE DEL RESPONSABILE

Oggetto: Affidamento di servizi dati a WindTre

DETERMINA

Copia del presente atto è pubblicata all'Albo Pretorio dal 20/10/2026 al 04/11/2026.
""", "a" * 64, "COMUNE_COLLESALVETTI")
        self.assertIsNone(act["validita"]["dal"])
        self.assertIsNone(act["validita"]["al"])

    def test_published_pdf_paths_and_map_links(self):
        index = (ARCHIVE / "ordinanze.json").read_bytes()
        self.assertEqual(index, (ROOT / "public/data/ordinanze.json").read_bytes())
        acts = json.loads(index)
        self.assertEqual(len(acts), len({act["id"] for act in acts}))
        by_id = {act["id"]: act for act in acts}
        routes = json.loads((ROOT / "data/network_data.json").read_text())["features"]
        expected = {f["id"] for f in routes if (f["properties"].get("cantiere") or {}).get("id_ordinanza") ==
                    "PM-COLLE-ORD-118-2026"}
        self.assertEqual(len(expected), 4)
        self.assertEqual(set(by_id["PM-COLLE-ORD-118-2026"]["localizzazione"]["matched_feature_ids"]), expected)
        for act in acts:
            self.assertTrue((ROOT / unquote(act["file_pdf"]["url_path"])).is_file(), act["id"])
            self.assertFalse(set(act["localizzazione"]["matched_feature_ids"]) &
                             set(act["localizzazione"]["candidate_feature_ids"]), act["id"])
        tracker = (ROOT / "js/cantieri_tracker.js").read_text()
        fallback = tracker.split("const ORDINANZE_DATA_DEFAULT = ", 1)[1].split(";\n\nlet ORDINANZE_DATA", 1)[0]
        self.assertEqual(json.loads(fallback), json.loads((ROOT / "data/ordinanze.json").read_text()))


if __name__ == "__main__":
    unittest.main()
