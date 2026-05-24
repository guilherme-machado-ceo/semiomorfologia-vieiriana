"""
Teste de Aderência ao Padrão PANVIEIRA (TAP-PAN)

Procedimento estatístico em 4 etapas para verificar se um sistema semiótico
realmente adere ao padrão PANVIEIRA — e não apenas a uma aproximação superficial.

Referência: Proposição 6 do paper PANVIEIRA (Machado, 2026)
"""
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from scipy import stats
from collections import Counter


class ResultadoTAPPAN:
    """Resultado completo do TAP-PAN com todas as 4 etapas."""
    def __init__(self):
        self.etapa1_invariancia: Optional[float] = None  # p-valor ou estatística
        self.etapa1_variancia_G: Optional[float] = None
        self.etapa2_chi2: Optional[float] = None
        self.etapa2_p_valor: Optional[float] = None
        self.etapa2_info_mutua: Optional[float] = None
        self.etapa3_erros: List[float] = []
        self.etapa3_erro_medio: Optional[float] = None
        self.etapa4_aic_pan: Optional[float] = None
        self.etapa4_bic_pan: Optional[float] = None
        self.etapa4_resultados_nulos: Dict[str, Dict[str, float]] = {}
        self.aderencia_global: Optional[float] = None  # score 0-1
        self.aderencia: bool = False


class TAPPAN:
    """
    Teste de Aderência ao Padrão PANVIEIRA (TAP-PAN).

    Etapas:
        1. Invariância de G — variância angular das instâncias no espaço semântico
        2. Independência entre {Sᵢ} e {Cᵢ} — qui-quadrado + informação mútua
        3. Validação cruzada por exclusão — leave-one-out e reconstrução
        4. Benchmark contra modelos nulos — AIC/BIC
    """

    def __init__(self, epsilon1: float = 0.15, epsilon2: float = 0.3,
                 alpha: float = 0.05):
        self.epsilon1 = epsilon1  # limiar variância G
        self.epsilon2 = epsilon2  # limiar erro predição
        self.alpha = alpha  # nível de significância

    def executar(self, instancias: List[str], S_labels: List[str],
                 C_labels: List[str], embeddings: Optional[np.ndarray] = None,
                 n_bootstrap: int = 1000) -> ResultadoTAPPAN:
        """
        Executa as 4 etapas do TAP-PAN.

        Args:
            instancias: Lista de instâncias completas eᵢ = Sᵢ ⊗ G ⊗ Cᵢ
            S_labels: Diferenciadores correspondentes
            C_labels: Loci correspondentes
            embeddings: Matriz (n, d) de embeddings — se None, usa TF-IDF
            n_bootstrap: Número de iterações bootstrap

        Returns:
            ResultadoTAPPAN com todas as métricas
        """
        resultado = ResultadoTAPPAN()
        n = len(instancias)
        assert n == len(S_labels) == len(C_labels), "Tamanhos inconsistentes"

        # Obter embeddings se não fornecidos
        if embeddings is None:
            embeddings = self._tfidf_embeddings(instancias)
        embeddings = np.array(embeddings)

        # Etapa 1: Invariância de G
        self._etapa1_invariancia(embeddings, resultado)

        # Etapa 2: Independência Sᵢ x Cᵢ
        self._etapa2_independencia(S_labels, C_labels, resultado)

        # Etapa 3: Validação cruzada
        self._etapa3_validacao_cruzada(instancias, S_labels, C_labels, embeddings, resultado)

        # Etapa 4: Benchmark contra nulos
        self._etapa4_benchmark(instancias, embeddings, resultado)

        # Score global
        resultado.aderencia = self._calcular_aderencia(resultado)
        resultado.aderencia_global = self._score_global(resultado)

        return resultado

    def _tfidf_embeddings(self, textos: List[str]) -> np.ndarray:
        """Gera embeddings via TF-IDF como fallback."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.decomposition import TruncatedSVD
            # token_pattern r'(?u)\b\w+\b' aceita tokens de 1 char
            vec = TfidfVectorizer(max_features=100, token_pattern=r'(?u)\b\w+\b')
            X = vec.fit_transform(textos)
            if X.shape[1] == 0:
                return self._hash_embeddings(textos)
            if X.shape[1] > 50:
                svd = TruncatedSVD(n_components=50, random_state=42)
                X = svd.fit_transform(X)
            return X.toarray() if hasattr(X, 'toarray') else X
        except (ImportError, ValueError):
            return self._hash_embeddings(textos)

    def _hash_embeddings(self, textos: List[str]) -> np.ndarray:
        """Fallback mínimo usando hash fingerprints."""
        dim = 64
        mat = np.zeros((len(textos), dim))
        for i, t in enumerate(textos):
            for j, ch in enumerate(t[:dim*4]):
                mat[i, j % dim] += ord(ch) * (0.1 ** (j // dim))
            norm = np.linalg.norm(mat[i])
            if norm > 0:
                mat[i] /= norm
        return mat

    def _etapa1_invariancia(self, embeddings: np.ndarray, resultado: ResultadoTAPPAN):
        """
        Etapa 1 — Invariância de G.
        Mede a variância angular entre os embeddings das instâncias.
        Baixa variância = G invariante.
        """
        centroides = np.mean(embeddings, axis=0)
        centroides_norm = centroides / (np.linalg.norm(centroides) + 1e-10)

        cossenos = []
        for emb in embeddings:
            norm = np.linalg.norm(emb)
            if norm > 0:
                cos_sim = np.dot(emb / norm, centroides_norm)
                cossenos.append(cos_sim)

        cossenos = np.array(cossenos)
        resultado.etapa1_variancia_G = float(np.var(1 - cossenos))

        # Bootstrap para p-valor
        n = len(embeddings)
        bootstrap_vars = []
        for _ in range(1000):
            idx = np.random.choice(n, n, replace=True)
            sample = embeddings[idx]
            cent = np.mean(sample, axis=0)
            cent_norm = cent / (np.linalg.norm(cent) + 1e-10)
            cos_sample = []
            for emb in sample:
                norm = np.linalg.norm(emb)
                if norm > 0:
                    cos_sample.append(np.dot(emb/norm, cent_norm))
            bootstrap_vars.append(np.var(1 - np.array(cos_sample)))

        p_valor = float(np.mean(np.array(bootstrap_vars) <= resultado.etapa1_variancia_G))
        resultado.etapa1_invariancia = p_valor

    def _etapa2_independencia(self, S_labels: List[str], C_labels: List[str],
                              resultado: ResultadoTAPPAN):
        """
        Etapa 2 — Independência entre {Sᵢ} e {Cᵢ}.
        Teste qui-quadrado + informação mútua.
        """
        # Contingência
        tab = Counter(zip(S_labels, C_labels))
        todos_S = sorted(set(S_labels))
        todos_C = sorted(set(C_labels))

        matriz = np.zeros((len(todos_S), len(todos_C)))
        for (s, c), count in tab.items():
            i, j = todos_S.index(s), todos_C.index(c)
            matriz[i, j] = count

        # Qui-quadrado
        if matriz.shape[0] >= 2 and matriz.shape[1] >= 2:
            chi2, p, dof, expected = stats.chi2_contingency(matriz + 0.5)
            resultado.etapa2_chi2 = float(chi2)
            resultado.etapa2_p_valor = float(p)
        else:
            resultado.etapa2_chi2 = 0.0
            resultado.etapa2_p_valor = 1.0

        # Informação mútua (normalizada)
        total = matriz.sum()
        if total > 0:
            mi = 0.0
            for i in range(len(todos_S)):
                for j in range(len(todos_C)):
                    pxy = matriz[i, j] / total
                    px = matriz[i, :].sum() / total
                    py = matriz[:, j].sum() / total
                    if pxy > 0:
                        mi += pxy * np.log2(pxy / (px * py + 1e-10) + 1e-10)
            # Normalizar por H(S) + H(C)
            h_s = -sum((matriz[i,:].sum()/total) * np.log2(matriz[i,:].sum()/total + 1e-10)
                       for i in range(len(todos_S)) if matriz[i,:].sum() > 0)
            h_c = -sum((matriz[:,j].sum()/total) * np.log2(matriz[:,j].sum()/total + 1e-10)
                       for j in range(len(todos_C)) if matriz[:,j].sum() > 0)
            denom = h_s + h_c if (h_s + h_c) > 0 else 1
            resultado.etapa2_info_mutua = float(mi / denom)
        else:
            resultado.etapa2_info_mutua = 0.0

    def _etapa3_validacao_cruzada(self, instancias: List[str], S_labels: List[str],
                                   C_labels: List[str], embeddings: np.ndarray,
                                   resultado: ResultadoTAPPAN):
        """
        Etapa 3 — Validação cruzada por exclusão (leave-one-out).
        Remove cada instância, re-estima G (centróide), prevê a removida.
        """
        n = len(instancias)
        erros = []

        for k in range(n):
            # Remover instância k
            idx_resto = [i for i in range(n) if i != k]
            emb_resto = embeddings[idx_resto]
            emb_removida = embeddings[k]

            # G estimado = centróide das restantes
            G_est = np.mean(emb_resto, axis=0)

            # Erro = 1 - cosseno(emb_removida, G_est)
            norm_rem = np.linalg.norm(emb_removida)
            norm_est = np.linalg.norm(G_est)
            if norm_rem > 0 and norm_est > 0:
                cosseno = np.dot(emb_removida, G_est) / (norm_rem * norm_est)
                erro = 1 - cosseno
            else:
                erro = 1.0
            erros.append(erro)

        resultado.etapa3_erros = [float(e) for e in erros]
        resultado.etapa3_erro_medio = float(np.mean(erros))

    def _etapa4_benchmark(self, instancias: List[str], embeddings: np.ndarray,
                           resultado: ResultadoTAPPAN):
        """
        Etapa 4 — Benchmark contra modelos nulos via AIC/BIC.
        Compara o PANVIEIRA contra: variância total e média aleatória.
        """
        n, d = embeddings.shape

        # Modelo PANVIEIRA: variância dentro do cluster (intra-classe)
        centroides = np.mean(embeddings, axis=0)
        residuos_pan = np.sum((embeddings - centroides) ** 2)
        k_pan = d + 1  # parâmetros: centróide (d) + variância (1)

        resultado.etapa4_aic_pan = float(2 * k_pan + n * np.log(residuos_pan / n + 1e-10))
        resultado.etapa4_bic_pan = float(k_pan * np.log(n) + n * np.log(residuos_pan / n + 1e-10))

        # Modelo nulo 1: média global (constante)
        media_global = np.mean(embeddings)
        residuos_null1 = np.sum((embeddings - media_global) ** 2)
        k_null1 = d + 1
        aic_null1 = float(2 * k_null1 + n * np.log(residuos_null1 / n + 1e-10))
        bic_null1 = float(k_null1 * np.log(n) + n * np.log(residuos_null1 / n + 1e-10))

        resultado.etapa4_resultados_nulos["media_global"] = {
            "aic": aic_null1, "bic": bic_null1
        }

    def _calcular_aderencia(self, resultado: ResultadoTAPPAN) -> bool:
        """
        Determina aderência com base nos critérios.
        """
        # Etapa 1: variância de G deve ser baixa
        e1_ok = resultado.etapa1_variancia_G is not None and resultado.etapa1_variancia_G < self.epsilon1

        # Etapa 2: p-valor do qui-quadrado deve ser não-significativo (independência)
        e2_ok = resultado.etapa2_p_valor is not None and resultado.etapa2_p_valor > self.alpha

        # Etapa 3: erro médio de reconstrução deve ser baixo
        e3_ok = resultado.etapa3_erro_medio is not None and resultado.etapa3_erro_medio < self.epsilon2

        # Etapa 4: AIC do PANVIEIRA deve ser menor que o nulo
        e4_ok = True
        if resultado.etapa4_aic_pan is not None and resultado.etapa4_resultados_nulos:
            for nome, res in resultado.etapa4_resultados_nulos.items():
                if resultado.etapa4_aic_pan < res.get("aic", float('inf')):
                    e4_ok = True
                else:
                    e4_ok = False

        return e1_ok and e2_ok and e3_ok and e4_ok

    def _score_global(self, resultado: ResultadoTAPPAN) -> float:
        """Score de aderência global (0 a 1)."""
        scores = []

        if resultado.etapa1_variancia_G is not None:
            scores.append(max(0, 1 - resultado.etapa1_variancia_G / self.epsilon1))

        if resultado.etapa2_p_valor is not None:
            scores.append(min(1, resultado.etapa2_p_valor / (2 * self.alpha)))

        if resultado.etapa3_erro_medio is not None:
            scores.append(max(0, 1 - resultado.etapa3_erro_medio / self.epsilon2))

        return float(np.mean(scores)) if scores else 0.0
