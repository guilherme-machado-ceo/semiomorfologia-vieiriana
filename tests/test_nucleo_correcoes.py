"""
Testes de regressão para as correções do núcleo (revisão independente, nov/2026).

Cada teste falhava no commit 54f341b e documenta o comportamento esperado.
"""
import numpy as np
import pytest

from semiomorfologia.motor.hylomorphism import HylomorphismEngine
from semiomorfologia.motor.mapreduce_engine import MapReduceEngine
from semiomorfologia.motor.invariante import extrair_invariante

SEXAGESIMA = [
    ("A natureza insensível", "nas pedras"),
    ("a vegetativa", "nos espinhos"),
    ("a sensitiva", "nas aves"),
    ("a racional", "nos homens"),
]


# --- Circularidade G -> EXPAND -> CONTRACT -> G ---------------------------

@pytest.mark.parametrize("g,pares", [
    ("o perseguiu", [("insensivel", "pedras"), ("vegetativa", "espinhos"), ("racional", "homens")]),
    ("o perseguiu", SEXAGESIMA),
    ("G", [("a", "x"), ("b", "y")]),
    ("caiu a semente", [("uma parte", "no caminho"), ("outra", "entre espinhos"), ("outra ainda", "em boa terra")]),
])
def test_hylomorphism_recupera_G(g, pares):
    r = HylomorphismEngine().hylomorphism(g, pares)
    assert r["G_recuperado"] == g
    assert r["invariante"] is True


def test_mapreduce_recupera_G():
    r = MapReduceEngine().mapreduce("o perseguiu", SEXAGESIMA)
    assert r["G"] == "o perseguiu"
    assert r["invariante"] is True


def test_instancia_unica_nao_afirma_circularidade():
    # Com um só par, G não é identificável; o motor não pode declarar invariância.
    r = HylomorphismEngine().hylomorphism("o perseguiu", [("insensivel", "pedras")])
    assert r["invariante"] is False


def test_desempate_prefere_posicao_medial():
    # S compartilham "a natureza"; o invariante medial deve vencer o prefixo.
    inst = ["a natureza insensível o perseguiu nas pedras",
            "a natureza vegetativa o perseguiu nos espinhos"]
    assert extrair_invariante(inst) == "o perseguiu"


def test_sem_token_comum_devolve_vazio():
    assert extrair_invariante(["alfa beta", "gama delta"]) == ""


# --- Sintagma.extrair_generico usa a interseção calculada ------------------

def test_extrair_generico_usa_descritores_comuns():
    from semiomorfologia.core.ontologia import Morfema, Sintagma, DominioNatural, NivelOrganizacao
    m1 = Morfema("a", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR, descritores={"funcao": "x", "cor": "azul"})
    m2 = Morfema("b", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR, descritores={"funcao": "y"})
    g = Sintagma(id="s", morfemas=[m1, m2]).extrair_generico()
    assert g == "conjunto_mineral_generico:funcao"


# --- TAP-PAN etapa 4 deixa de ser tautológica ------------------------------

def test_etapa4_pode_rejeitar_PANVIEIRA():
    from semiomorfologia.similaridade.tap_pan import TAPPAN, ResultadoTAPPAN
    rng = np.random.RandomState(0)
    emb = rng.normal(size=(5, 20))  # sem estrutura de grupo, d grande, n pequeno
    r = ResultadoTAPPAN()
    TAPPAN()._etapa4_benchmark(["x"] * 5, emb, r)
    aic_nulo = r.etapa4_resultados_nulos["media_global"]["aic"]
    assert r.etapa4_aic_pan > aic_nulo  # o modelo nulo vence quando não há estrutura


def test_etapa4_favorece_PANVIEIRA_com_estrutura():
    from semiomorfologia.similaridade.tap_pan import TAPPAN, ResultadoTAPPAN
    rng = np.random.RandomState(0)
    centro = rng.normal(scale=5.0, size=20)
    emb = centro + rng.normal(scale=0.05, size=(30, 20))  # grupo coeso, longe da média escalar
    r = ResultadoTAPPAN()
    TAPPAN()._etapa4_benchmark(["x"] * 30, emb, r)
    assert r.etapa4_aic_pan < r.etapa4_resultados_nulos["media_global"]["aic"]


# --- Vetorização sem modelo é discriminativa e reprodutível ----------------

def test_fallback_distingue_textos_de_mesmo_tamanho():
    from semiomorfologia.similaridade.semantica import MotorSemantico
    m = MotorSemantico()
    m.modelo, m._nivel = None, 0  # força o fallback, mesmo com sentence-transformers instalado
    assert m.similaridade("o mar azul", "a terra seca") < 0.5
    assert m.similaridade("o mar azul", "o mar azul") == pytest.approx(1.0)


def test_fallback_reprodutivel_entre_chamadas():
    from semiomorfologia.similaridade.semantica import _saco_de_palavras
    assert _saco_de_palavras("Sermão da Sexagésima") == _saco_de_palavras("Sermão da Sexagésima")


# --- Forças de analogia determinísticas ------------------------------------

def test_forca_ponte_determinista():
    from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao
    from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico
    m1 = Morfema("a", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR, propriedades={"p": 1.0, "q": 2.0})
    m2 = Morfema("b", DominioNatural.VEGETAL, NivelOrganizacao.CELULAR, propriedades={"p": 3.0})
    motor = MotorSemiomorfologico()
    f = [motor._forca_ponte(m1, m2) for _ in range(5)]
    assert len(set(f)) == 1 and 0.55 <= f[0] <= 0.85
