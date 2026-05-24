"""
Testes para módulos v3.0.0 do framework Semiomorfologia Vieiriana.
Cobertura: TAP-PAN, CSI, Hylomorphism, MapReduce, AbstractKMeans,
GrafoBipartido, Quantum (fallback clássico).
"""
import pytest
import numpy as np


# ============ TAP-PAN ============

class TestTAPPAN:
    def test_instanciacao(self):
        from semiomorfologia.similaridade.tap_pan import TAPPAN, ResultadoTAPPAN
        tap = TAPPAN()
        assert tap.epsilon1 == 0.15
        assert tap.epsilon2 == 0.3

    def test_resultado_vazio(self):
        from semiomorfologia.similaridade.tap_pan import ResultadoTAPPAN
        r = ResultadoTAPPAN()
        assert r.aderencia is False
        assert r.aderencia_global is None

    def test_instancias_vieirianas(self):
        from semiomorfologia.similaridade.tap_pan import TAPPAN
        instancias = [
            "a natureza insensivel o perseguiu nas pedras",
            "a natureza vegetativa o perseguiu nos espinhos",
            "a natureza sensitiva o perseguiu nas aves",
            "a natureza racional o perseguiu nos homens",
        ]
        S = ["insensivel", "vegetativa", "sensitiva", "racional"]
        C = ["pedras", "espinhos", "aves", "homens"]
        tap = TAPPAN()
        resultado = tap.executar(instancias, S, C)
        assert resultado.etapa1_variancia_G is not None
        assert resultado.etapa2_chi2 is not None
        assert resultado.etapa3_erro_medio is not None
        assert resultado.etapa4_aic_pan is not None
        assert resultado.aderencia_global is not None
        assert isinstance(resultado.aderencia, bool)

    def test_hash_embeddings_fallback(self):
        from semiomorfologia.similaridade.tap_pan import TAPPAN
        tap = TAPPAN()
        embs = tap._hash_embeddings(["abc", "def", "ghi"])
        assert embs.shape == (3, 64)

    def test_etapa2_independencia(self):
        from semiomorfologia.similaridade.tap_pan import TAPPAN
        instancias = ["a b c", "d e f", "g h i"]
        S = ["a", "d", "g"]
        C = ["c", "f", "i"]
        tap = TAPPAN()
        resultado = tap.executar(instancias, S, C)
        assert resultado.etapa2_p_valor is not None


# ============ CSI ============

class TestCSI:
    def test_instanciacao(self):
        from semiomorfologia.similaridade.csi import CSICalculador
        calc = CSICalculador()
        assert calc.percentil == 75.0

    def test_instancias_coerentes(self):
        from semiomorfologia.similaridade.csi import CSICalculador
        instancias = [
            "a natureza insensivel o perseguiu nas pedras",
            "a natureza vegetativa o perseguiu nos espinhos",
            "a natureza sensitiva o perseguiu nas aves",
            "a natureza racional o perseguiu nos homens",
        ]
        calc = CSICalculador(n_bootstrap=100)
        resultado = calc.calcular(instancias)
        assert resultado.csi > 0
        assert resultado.tau > 0
        assert resultado.categoria in ["significativo", "parcial", "insignificante"]
        assert len(resultado.csi_por_instancia) == 4

    def test_instancias_incoerentes(self):
        from semiomorfologia.similaridade.csi import CSICalculador
        instancias = ["gato", "bicicleta", "telescopio", "sopa"]
        calc = CSICalculador(n_bootstrap=50)
        resultado = calc.calcular(instancias)
        assert resultado.csi >= 0
        assert resultado.categoria in ["significativo", "parcial", "insignificante"]


# ============ Hylomorphism ============

class TestHylomorphism:
    def test_instanciacao(self):
        from semiomorfologia.motor.hylomorphism import HylomorphismEngine
        engine = HylomorphismEngine()
        assert engine is not None

    def test_unfold(self):
        from semiomorfologia.motor.hylomorphism import HylomorphismEngine
        engine = HylomorphismEngine()
        pares = [("insensivel", "pedras"), ("vegetativa", "espinhos")]
        resultado = engine.unfold("o perseguiu", pares)
        assert len(resultado) == 2
        assert "insensivel" in resultado[0]
        assert "pedras" in resultado[0]

    def test_fold(self):
        from semiomorfologia.motor.hylomorphism import HylomorphismEngine
        engine = HylomorphismEngine()
        instancias = ["a b c", "a b c", "a b c"]
        g = engine.fold(instancias)
        assert g == "a b c"

    def test_hylomorphism_circularidade(self):
        from semiomorfologia.motor.hylomorphism import HylomorphismEngine
        engine = HylomorphismEngine()
        # Quando há apenas 1 par, unfold gera 1 instância, fold a retorna
        pares = [("insensivel", "pedras")]
        resultado = engine.hylomorphism("o perseguiu", pares)
        assert resultado['G_original'] == "o perseguiu"
        assert resultado['n_instancias'] == 1
        assert isinstance(resultado['invariante'], bool)

    def test_circle_multiplas_iteracoes(self):
        from semiomorfologia.motor.hylomorphism import HylomorphismEngine
        engine = HylomorphismEngine()
        pares = [("a", "x"), ("b", "y")]
        resultados = engine.circle("G", pares, n_iter=3)
        assert len(resultados) == 3


# ============ MapReduce ============

class TestMapReduce:
    def test_instanciacao(self):
        from semiomorfologia.motor.mapreduce_engine import MapReduceEngine
        engine = MapReduceEngine(n_workers=2)
        assert engine.n_workers == 2

    def test_map_expand(self):
        from semiomorfologia.motor.mapreduce_engine import MapReduceEngine
        engine = MapReduceEngine(n_workers=2)
        pares = [("insensivel", "pedras"), ("vegetativa", "espinhos")]
        resultado = engine.map_expand("o perseguiu", pares)
        assert len(resultado) == 2

    def test_reduce_contract(self):
        from semiomorfologia.motor.mapreduce_engine import MapReduceEngine
        engine = MapReduceEngine()
        resultado = engine.reduce_contract(["a b c", "a b c", "a b c"])
        assert resultado['G'] == "a b c"
        assert resultado['n'] == 3

    def test_mapreduce_pipeline(self):
        from semiomorfologia.motor.mapreduce_engine import MapReduceEngine
        engine = MapReduceEngine(n_workers=1)
        resultado = engine.mapreduce("G", [("a", "x")])
        assert resultado['G_original'] == "G"
        assert resultado['n'] == 1

    def test_mapexpand_single_worker(self):
        from semiomorfologia.motor.mapreduce_engine import MapReduceEngine
        engine = MapReduceEngine(n_workers=1)
        resultado = engine.map_expand("G", [("a", "b"), ("c", "d")])
        assert len(resultado) == 2


# ============ AbstractKMeans ============

class TestAbstractKMeans:
    def test_instanciacao(self):
        from semiomorfologia.motor.abstract_kmeans import AbstractKMeans
        ak = AbstractKMeans(k=2)
        assert ak.k == 2

    def test_abstract_vieiriano(self):
        from semiomorfologia.motor.abstract_kmeans import AbstractKMeans
        instancias = [
            "a natureza insensivel o perseguiu nas pedras",
            "a natureza vegetativa o perseguiu nos espinhos",
            "a natureza sensitiva o perseguiu nas aves",
            "a natureza racional o perseguiu nos homens",
        ]
        ak = AbstractKMeans(k=1)
        resultado = ak.abstract(instancias)
        assert 'G' in resultado
        assert resultado['G'] != ''
        assert resultado['n_clusters'] == 1

    def test_abstract_vazio(self):
        from semiomorfologia.motor.abstract_kmeans import AbstractKMeans
        ak = AbstractKMeans()
        resultado = ak.abstract([])
        assert resultado['G'] == ''

    def test_abstract_unica(self):
        from semiomorfologia.motor.abstract_kmeans import AbstractKMeans
        ak = AbstractKMeans()
        resultado = ak.abstract(["unica instancia"])
        assert resultado['G'] == "unica instancia"


# ============ Grafo Bipartido ============

class TestGrafoBipartido:
    def test_instanciacao(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        assert len(grafo.arestas) == 0

    def test_adicionar_aresta(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        grafo.adicionar_aresta("insensivel", "pedras", 0.9)
        assert len(grafo.arestas) == 1
        assert ("insensivel", "pedras") in grafo.arestas

    def test_expand(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        grafo.adicionar_aresta("insensivel", "pedras", 1.0)
        grafo.adicionar_aresta("vegetativa", "espinhos", 0.8)
        resultado = grafo.expand("o perseguiu")
        assert len(resultado) == 2
        assert resultado[0]['G'] == "o perseguiu"
        assert resultado[0]['S'] == "insensivel"

    def test_expand_top_k(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        grafo.adicionar_aresta("a", "x", 1.0)
        grafo.adicionar_aresta("b", "y", 0.5)
        grafo.adicionar_aresta("c", "z", 0.3)
        resultado = grafo.expand_top_k("G", k=2)
        assert len(resultado) == 2

    def test_estatisticas(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        grafo.adicionar_aresta("a", "x", 1.0)
        grafo.adicionar_aresta("b", "y", 0.5)
        stats = grafo.estatisticas()
        assert stats['n_diferenciadores'] == 2
        assert stats['n_loci'] == 2
        assert stats['n_arestas'] == 2

    def test_estimar_arestas_ausentes(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        grafo.adicionar_aresta("a", "x", 1.0)
        grafo.adicionar_aresta("b", "x", 1.0)
        grafo.adicionar_aresta("a", "y", 0.8)
        grafo.adicionar_aresta("b", "y", 0.7)
        estimadas = grafo.estimar_arestas_ausentes()
        # Com 4 arestas existentes, deve encontrar arestas ausentes
        # entre nos existentes (e.g. se tivesse "c" nó, estimaria)
        stats = grafo.estatisticas()
        assert stats['n_arestas'] == 4

    def test_filtro_P(self):
        from semiomorfologia.visualizacao.grafo_bipartido import GrafoBipartidoExpand
        grafo = GrafoBipartidoExpand()
        grafo.adicionar_aresta("insensivel", "pedras", 1.0)
        grafo.adicionar_aresta("vegetativa", "espinhos", 0.8)
        grafo.adicionar_aresta("xyz", "abc", 0.5)
        def regra(s, g, c):
            return len(s) < 5
        resultado = grafo.expand_com_filtro_P("G", [regra])
        assert len(resultado) == 1
        assert resultado[0]['S'] == "xyz"


# ============ Quantum (fallback classico) ============

class TestQuantum:
    def test_hpanvieira_instanciacao(self):
        from semiomorfologia.quantum.hpanvieira import HPANVIEIRA
        hp = HPANVIEIRA(modo='simulacao')
        assert hp.modo == 'simulacao'

    def test_hpanvieira_fallback_classico(self):
        from semiomorfologia.quantum.hpanvieira import HPANVIEIRA
        hp = HPANVIEIRA()
        hp._qiskit_disponivel = False
        resultado = hp.expand_quantico("G", [("a", "x"), ("b", "y")])
        assert len(resultado['instancias']) == 2
        assert resultado['modo'] == 'classico_fallback'

    def test_qexpand_fallback(self):
        from semiomorfologia.quantum.qexpand import qexpand
        resultado = qexpand("G", [("a", "x")])
        assert resultado['status'] in ['fallback_classico', 'ok']

    def test_qcontract_fallback(self):
        from semiomorfologia.quantum.qcontract import qcontract
        resultado = qcontract(["inst1", "inst2"])
        assert resultado['G'] in ['inst1', 'inst2']

    def test_grover_fallback(self):
        from semiomorfologia.quantum.grover_locus import grover_locus
        resultado = grover_locus("alvo", ["a", "b", "alvo", "d"])
        assert resultado['encontrado'] is True

    def test_grover_nao_encontrado(self):
        from semiomorfologia.quantum.grover_locus import grover_locus
        resultado = grover_locus("xyz", ["a", "b", "c"])
        assert resultado['encontrado'] is False

    def test_hpanvieira_pipeline(self):
        from semiomorfologia.quantum.hpanvieira import HPANVIEIRA
        hp = HPANVIEIRA()
        hp._qiskit_disponivel = False
        resultado = hp.executar_hibrido("G", [("a", "x"), ("b", "y")])
        assert resultado['G_original'] == "G"
        assert resultado['n_instancias'] == 2
