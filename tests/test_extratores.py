"""
Testes unitários para os 4 extratores especializados.
"""
import pytest

from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao
from semiomorfologia.extratores import (
    ExtratorMineral, ExtratorVegetal, ExtratorAnimal, ExtratorHumano
)


class TestExtratorMineral:
    def setup_method(self):
        self.extrator = ExtratorMineral()
        self.corpus = [
            Morfema("grafeno", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                    descritores={"elemento_base": "carbono", "funcao": "condutividade"},
                    propriedades={"condutividade": 0.98, "flexibilidade": 0.95}),
            Morfema("diamante", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                    descritores={"elemento_base": "carbono", "funcao": "dureza"},
                    propriedades={"dureza": 1.0, "brilho": 0.99}),
            Morfema("grafite", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
                    descritores={"elemento_base": "carbono", "funcao": "lubrificacao"},
                    propriedades={"condutividade": 0.85, "flexibilidade": 0.30}),
        ]

    def test_homologica_carbono(self):
        resultados = self.extrator.processar(self.corpus)
        homologicas = resultados[TipoAnalogia.HOMOLOGICA]
        assert len(homologicas) > 0
        # grafeno-diamante-grafite compartilham elemento_base=carbono
        pares = [(a.fonte.id, a.alvo.id) for a in homologicas]
        assert any("grafeno" in p and "diamante" in p for p in pares)

    def test_dominio_correto(self):
        assert self.extrator.dominio == DominioNatural.MINERAL


class TestExtratorVegetal:
    def setup_method(self):
        self.extrator = ExtratorVegetal()
        self.corpus = [
            Morfema("cacto", DominioNatural.VEGETAL, NivelOrganizacao.ORGANICO,
                    descritores={"ambiente": "desertico", "processo": "CAM", "familia": "Cactaceae"}),
            Morfema("edelweiss", DominioNatural.VEGETAL, NivelOrganizacao.ORGANICO,
                    descritores={"ambiente": "alpino", "processo": "protecao_UV", "familia": "Asteraceae"}),
        ]

    def test_heuristica_estresse(self):
        resultados = self.extrator.processar(self.corpus)
        heuristicas = resultados[TipoAnalogia.HEURISTICA]
        assert len(heuristicas) >= 1


class TestExtratorAnimal:
    def setup_method(self):
        self.extrator = ExtratorAnimal()
        self.corpus = [
            Morfema("tardigrado", DominioNatural.ANIMAL, NivelOrganizacao.CELULAR,
                    descritores={"filum": "Tardigrada", "sistema": "tun", "adaptacao": "criptobiose"}),
            Morfema("polvo", DominioNatural.ANIMAL, NivelOrganizacao.ORGANICO,
                    descritores={"filum": "Mollusca", "sistema": "camuflagem", "adaptacao": "mimetismo"}),
        ]

    def test_dominio_correto(self):
        assert self.extrator.dominio == DominioNatural.ANIMAL


class TestExtratorHumano:
    def setup_method(self):
        self.extrator = ExtratorHumano()
        self.corpus = [
            Morfema("neuronio_espelho", DominioNatural.HUMANO, NivelOrganizacao.CELULAR,
                    descritores={"tipo": "biologico", "sistema_biologico": "nervoso", "estrutura_profunda": "replicacao"}),
            Morfema("sintaxe_recursiva", DominioNatural.HUMANO, NivelOrganizacao.ECOSSISTEMICO,
                    descritores={"tipo": "linguistico", "sistema_biologico": "linguagem", "estrutura_profunda": "replicacao"}),
        ]

    def test_heuristica_corpo_linguagem(self):
        resultados = self.extrator.processar(self.corpus)
        heuristicas = resultados[TipoAnalogia.HEURISTICA]
        assert len(heuristicas) == 1
        assert heuristicas[0].mapeamento.get("estrutura_profunda") == "corpo↔linguagem"
