import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from unittest.mock import patch, MagicMock
from semiomorfologia.conhecimento.wikidata import WikidataClient
from semiomorfologia.conhecimento.pubchem import PubChemClient
from semiomorfologia.conhecimento.gbif import GBIFClient
from semiomorfologia.conhecimento.enriquecedor import EnriquecedorMorfemas


class TestWikidata(unittest.TestCase):
    @patch("semiomorfologia.conhecimento.wikidata.requests.get")
    def test_buscar_propriedades(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"results": {"bindings": []}}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp
        c = WikidataClient()
        r = c.buscar_propriedades("grafeno")
        self.assertEqual(r["fonte"], "Wikidata")


class TestPubChem(unittest.TestCase):
    @patch("semiomorfologia.conhecimento.pubchem.requests.get")
    def test_buscar_composto_nao_encontrado(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.raise_for_status.side_effect = Exception("404")
        mock_get.return_value = mock_resp
        c = PubChemClient()
        self.assertIsNone(c.buscar_composto("inexistente_xyz"))


class TestGBIF(unittest.TestCase):
    @patch("semiomorfologia.conhecimento.gbif.requests.get")
    def test_buscar_especie(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "matchType": "EXACT", "scientificName": "Panthera leo",
            "kingdom": "Animalia", "family": "Felidae"
        }
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp
        c = GBIFClient()
        r = c.buscar_especie("Panthera leo")
        self.assertIsNotNone(r)
        self.assertEqual(r["familia"], "Felidae")

    @patch("semiomorfologia.conhecimento.gbif.requests.get")
    def test_buscar_especie_nao_encontrado(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"matchType": "NONE"}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp
        c = GBIFClient()
        self.assertIsNone(c.buscar_especie("naoexiste"))


class TestEnriquecedor(unittest.TestCase):
    @patch("semiomorfologia.conhecimento.enriquecedor.GBIFClient")
    @patch("semiomorfologia.conhecimento.enriquecedor.PubChemClient")
    @patch("semiomorfologia.conhecimento.enriquecedor.WikidataClient")
    def test_enriquecer_mineral(self, MockWiki, MockPubChem, MockGBIF):
        MockWiki.return_value.buscar_propriedades.return_value = {
            "fonte": "Wikidata", "propriedades": {"x": "y"}
        }
        enc = EnriquecedorMorfemas()
        r = enc.enriquecer({"nome": "grafeno", "dominio": "mineral"})
        self.assertIn("wikidata", r["enriquecimento"])

if __name__ == "__main__":
    unittest.main()
