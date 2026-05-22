"""
Testes de integração para o MotorSemiomorfologico.
"""
import pytest

from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao
from semiomorfologia.motor import MotorSemiomorfologico


class TestMotorIntegracao:
    def setup_method(self):
        self.motor = MotorSemiomorfologico()

    def test_composicao_sintagma(self):
        m1 = Morfema("a", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR)
        m2 = Morfema("b", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR)
        s = self.motor.compor_sintagma([m1, m2])
        assert s.conteudo_generico is not None
        assert len(self.motor.sintagmas) == 1

    def test_extracao_completa_mineral(self):
        corpus = [
            Morfema("grafeno", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                    descritores={"elemento_base": "carbono"},
                    propriedades={"condutividade": 0.98}),
            Morfema("grafite", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                    descritores={"elemento_base": "carbono"},
                    propriedades={"condutividade": 0.85}),
        ]
        resultados = self.motor.extrair_analogias_dominio(corpus, DominioNatural.MINERAL)
        assert TipoAnalogia.HOMOLOGICA in resultados
        assert len(resultados[TipoAnalogia.HOMOLOGICA]) >= 1

    def test_pontes_cruzadas(self):
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
        pontes = self.motor.extrair_analogias_cruzadas(corpus_multi)
        assert len(pontes) >= 1
        assert pontes[0].fonte.dominio != pontes[0].alvo.dominio

    def test_gerar_conhecimento(self):
        m1 = Morfema("a", DominioNatural.ANIMAL, NivelOrganizacao.CELULAR)
        m2 = Morfema("b", DominioNatural.ANIMAL, NivelOrganizacao.CELULAR)
        from semiomorfologia.core.ontologia import Analogia, TipoAnalogia
        analogia = Analogia(
            fonte=m1, alvo=m2, tipo=TipoAnalogia.FUNCIONAL,
            forca=0.85, aplicacao_industrial="teste"
        )
        conhecimentos = self.motor.gerar_conhecimento_aplicado([analogia])
        assert len(conhecimentos) == 1
        assert conhecimentos[0]["TRL_inicial"] >= 1
