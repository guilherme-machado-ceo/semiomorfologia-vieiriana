import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from semiomorfologia.visualizacao.grafo import VisualizadorAnalogias


class TestVisualizador(unittest.TestCase):
    def setUp(self):
        self.viz = VisualizadorAnalogias()
        self.dados = [
            {"fonte_id": "aerogel", "alvo_id": "edelweiss",
             "dominio_fonte": "mineral", "dominio_alvo": "vegetal",
             "forca": 0.85, "tipo": "heuristica"},
            {"fonte_id": "grafeno", "alvo_id": "neuronio",
             "dominio_fonte": "mineral", "dominio_alvo": "humano",
             "forca": 0.72, "tipo": "funcional"},
        ]

    def test_criar_grafo(self):
        G = self.viz.criar_grafo(self.dados)
        self.assertEqual(G.number_of_nodes(), 4)
        self.assertEqual(G.number_of_edges(), 2)

    def test_estatisticas(self):
        s = self.viz.estatisticas(self.dados)
        self.assertEqual(s["nos"], 4)
        self.assertEqual(s["arestas"], 2)

    def test_gerar_html(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
            output = f.name
        try:
            self.assertTrue(self.viz.gerar_html(self.dados, output))
            with open(output, encoding="utf-8") as f:
                self.assertIn("aerogel", f.read())
        finally:
            if os.path.exists(output):
                os.unlink(output)

    def test_gerar_html_vazio(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
            output = f.name
        try:
            self.assertTrue(self.viz.gerar_html([], output))
        finally:
            if os.path.exists(output):
                os.unlink(output)

if __name__ == "__main__":
    unittest.main()
