"""
Testes unitários para o módulo core/ontologia.
"""
import pytest
import numpy as np

from semiomorfologia.core.ontologia import (
    TipoAnalogia, DominioNatural, NivelOrganizacao, Morfema, Sintagma, Analogia
)


class TestMorfema:
    def test_criacao_basica(self):
        m = Morfema(
            id="grafeno",
            dominio=DominioNatural.MINERAL,
            nivel=NivelOrganizacao.MOLECULAR,
            descritores={"elemento": "carbono"},
            propriedades={"condutividade": 0.98}
        )
        assert m.id == "grafeno"
        assert m.dominio == DominioNatural.MINERAL

    def test_vetor_propriedades(self):
        m = Morfema(
            id="teste", dominio=DominioNatural.VEGETAL,
            nivel=NivelOrganizacao.CELULAR,
            propriedades={"a": 1.0, "b": 2.0}
        )
        vetor = m.vetor_propriedades()
        assert np.array_equal(vetor, np.array([1.0, 2.0]))

    def test_vetor_vazio(self):
        m = Morfema(
            id="vazio", dominio=DominioNatural.ANIMAL,
            nivel=NivelOrganizacao.ATOMICO
        )
        assert len(m.vetor_propriedades()) == 0


class TestSintagma:
    def test_extrair_generico(self):
        m1 = Morfema("a", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR)
        m2 = Morfema("b", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR)
        s = Sintagma(id="s1", morfemas=[m1, m2])
        generico = s.extrair_generico()
        assert "mineral" in generico
        assert "generico" in generico

    def test_sintagma_vazio(self):
        s = Sintagma(id="vazio")
        assert s.extrair_generico() == "vazio"


class TestAnalogia:
    def test_serializacao(self):
        m1 = Morfema("a", DominioNatural.HUMANO, NivelOrganizacao.CELULAR)
        m2 = Morfema("b", DominioNatural.HUMANO, NivelOrganizacao.CELULAR)
        a = Analogia(
            fonte=m1, alvo=m2, tipo=TipoAnalogia.HEURISTICA,
            forca=0.85, mapeamento={"x": "y"}, aplicacao_industrial="teste"
        )
        serial = a.serializar()
        assert serial["fonte_id"] == "a"
        assert serial["tipo"] == "heuristica"
        assert serial["forca"] == 0.85
