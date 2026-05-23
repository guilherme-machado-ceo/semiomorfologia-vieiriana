import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from semiomorfologia.similaridade.semantica import MotorSemantico
from semiomorfologia.similaridade.anti_unificacao import AntiUnificador
from semiomorfologia.avaliacao.fame import AvaliadorFAME
from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico


class TestMotorSemantico(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(MotorSemantico())

    def test_similaridade(self):
        ms = MotorSemantico()
        self.assertGreater(ms.similaridade("gato", "gato"), 0.5)

    def test_similaridade_diferente(self):
        ms = MotorSemantico()
        self.assertGreaterEqual(ms.similaridade("gato", "gato"), ms.similaridade("gato", "pedra"))

    def test_vetorizar(self):
        self.assertIsNotNone(MotorSemantico().vetorizar("teste"))


class TestAntiUnificador(unittest.TestCase):
    def test_anti_unificar(self):
        au = AntiUnificador()
        m1, m2 = {"nome": "a", "propriedades": {"p": 1}, "descritores": ["x"]}, {"nome": "b", "propriedades": {"p": 1}, "descritores": ["x"]}
        r = au.anti_unificar(m1, m2)
        self.assertIn("geral", r)
        self.assertGreater(r["grau_similaridade"], 0)

    def test_contrato(self):
        au = AntiUnificador()
        m1, m2 = {"nome": "a", "propriedades": {"p": 1}, "descritores": ["x"]}, {"nome": "b", "propriedades": {"p": 2}, "descritores": ["y"]}
        self.assertIn("tipo_contrato", au.contrato(m1, m2))

    def test_classificar(self):
        au = AntiUnificador()
        m = {"nome": "a", "descritores": ["comum"]}
        au.registrar(m)
        self.assertEqual(au.classificar(m), "especifico")


class TestAvaliadorFAME(unittest.TestCase):
    def test_avaliar(self):
        r = AvaliadorFAME().avaliar(0.8)
        self.assertIn("fame", r)
        self.assertGreater(r["fame"], 0)

    def test_avaliar_conjunto(self):
        r = AvaliadorFAME().avaliar_conjunto([0.5, 0.7, 0.9])
        self.assertIn("media", r["fame"])

    def test_avaliar_contrato(self):
        r = AvaliadorFAME().avaliar_contrato({"grau_similaridade": 0.7})
        self.assertGreater(r["fame"], 0)


class TestMotorSemiomorfologico(unittest.TestCase):
    def test_contrato_fame(self):
        au = AntiUnificador()
        av = AvaliadorFAME()
        m1 = {"nome": "a", "propriedades": {"p": 1}, "descritores": ["x"], "dominios": ["d1"]}
        m2 = {"nome": "b", "propriedades": {"p": 1}, "descritores": ["x"], "dominios": ["d1"]}
        contrato = au.contrato(m1, m2)
        avaliacao = av.avaliar_contrato(contrato)
        self.assertIn("fame", avaliacao)
        self.assertGreater(avaliacao["fame"], 0)

    def test_ponte_cruzada(self):
        from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao
        motor = MotorSemiomorfologico()
        corpus_multi = {
            DominioNatural.MINERAL: [
                Morfema("aerogel", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                        propriedades={"isolamento": 0.98})
            ],
            DominioNatural.VEGETAL: [
                Morfema("edelweiss", DominioNatural.VEGETAL, NivelOrganizacao.ORGANICO,
                        propriedades={"isolamento": 0.92})
            ],
        }
        pontes = motor.extrair_analogias_cruzadas(corpus_multi)
        self.assertGreaterEqual(len(pontes), 1)

    def test_rankear_pontes(self):
        from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao
        motor = MotorSemiomorfologico()
        corpus_multi = {
            DominioNatural.MINERAL: [
                Morfema(f"a{i}", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                        propriedades={"isolamento": 0.5 + i * 0.1}) for i in range(5)
            ],
            DominioNatural.VEGETAL: [
                Morfema(f"b{i}", DominioNatural.VEGETAL, NivelOrganizacao.ORGANICO,
                        propriedades={"isolamento": 0.5 + i * 0.1}) for i in range(5)
            ],
        }
        pontes = motor.extrair_analogias_cruzadas(corpus_multi)
        self.assertGreaterEqual(len(pontes), 1)
        top = sorted(pontes, key=lambda x: x.forca, reverse=True)[:3]
        self.assertEqual(len(top), 3)


if __name__ == "__main__":
    unittest.main()
