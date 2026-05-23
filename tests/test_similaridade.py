"""Testes das metricas de similaridade."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from semiomorfologia.similaridade.metricas import (
    cosseno, jaccard, euclidiana, manhattan, pearson, spearman,
    sobreposicao_descritores, distancia_combinada)

class TestMetricasSimilaridade(unittest.TestCase):
    def test_cosseno_vetores_iguais(self):
        self.assertAlmostEqual(cosseno([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0, places=4)
    def test_cosseno_ortogonais(self):
        self.assertAlmostEqual(cosseno([1, 0], [0, 1]), 0.0, places=4)
    def test_cosseno_vazios(self):
        self.assertEqual(cosseno([], []), 0.0)
    def test_jaccard_identico(self):
        self.assertAlmostEqual(jaccard({1, 2, 3}, {1, 2, 3}), 1.0)
    def test_jaccard_disjunto(self):
        self.assertAlmostEqual(jaccard({1, 2}, {3, 4}), 0.0)
    def test_jaccard_vazio(self):
        self.assertAlmostEqual(jaccard(set(), set()), 1.0)
    def test_euclidiana_iguais(self):
        self.assertAlmostEqual(euclidiana([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0, places=4)
    def test_manhattan_iguais(self):
        self.assertAlmostEqual(manhattan([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0, places=4)
    def test_pearson_correlacao(self):
        self.assertAlmostEqual(pearson([1, 2, 3], [1, 2, 3]), 1.0, places=4)
    def test_pearson_vazio(self):
        self.assertEqual(pearson([], []), 0.0)
    def test_spearman_correlacao(self):
        self.assertAlmostEqual(spearman([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]), 1.0, places=4)
    def test_sobreposicao_descritores(self):
        m1, m2 = {"descritores": ["duro", "brilhante"]}, {"descritores": ["duro", "pesado"]}
        self.assertGreater(sobreposicao_descritores(m1, m2), 0)
    def test_sobreposicao_vazios(self):
        self.assertGreaterEqual(sobreposicao_descritores({"descritores": []}, {"descritores": []}), 0.1)
    def test_distancia_combinada(self):
        m1 = {"descritores": ["a"], "propriedades": {"p": 1}, "dominios": ["d1"], "relacoes": ["r1"]}
        m2 = {"descritores": ["a"], "propriedades": {"p": 1}, "dominios": ["d1"], "relacoes": ["r1"]}
        r = distancia_combinada(m1, m2)
        self.assertGreaterEqual(r, 0.0)
        self.assertLessEqual(r, 1.0)

if __name__ == "__main__":
    unittest.main()
