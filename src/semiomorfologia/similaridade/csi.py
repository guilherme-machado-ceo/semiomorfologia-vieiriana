"""
Coerência Semântica Interna (CSI)

Métrica que distingue padrões semióticos genuínos de coincidências formais.
CSI(G, {Sᵢ}, {Cᵢ}) = (1/n) Σ sim(φ(eᵢ), ē_φ)

Referência: Proposição 7 do paper PANVIEIRA (Machado, 2026)
"""
import numpy as np
from typing import List, Optional, Tuple


class ResultadoCSI:
    """Resultado da análise de CSI."""
    def __init__(self, csi: float, tau: float, significativo: bool,
                 csi_por_instancia: List[float], categoria: str):
        self.csi = csi
        self.tau = tau
        self.significativo = significativo
        self.csi_por_instancia = csi_por_instancia
        self.categoria = categoria  # "significativo", "parcial", "insignificante"


class CSICalculador:
    """
    Calcula a Coerência Semântica Interna (CSI) de um padrão PANVIEIRA.

    A CSI mede o grau em que todas as instâncias de um padrão orbitam
    em torno do mesmo sentido profundo, distinguindo padrões semióticos
    genuínos (Vieira, ladainhas, fugas) de coincidências formais vazias
    (listas de compras, artefatos estilísticos).

    O limiar τ é determinado empiricamente via distribuição nula:
    τ = p₇₅({CSI₁, ..., CSI_B}) sob H₀: "instâncias geradas aleatoriamente"
    """

    def __init__(self, percentil: float = 75.0, n_bootstrap: int = 1000,
                 sementes: int = 42):
        self.percentil = percentil
        self.n_bootstrap = n_bootstrap
        self.sementes = sementes

    def calcular(self, instancias: List[str],
                 embeddings: Optional[np.ndarray] = None) -> ResultadoCSI:
        """
        Calcula CSI para um conjunto de instâncias.

        Args:
            instancias: Lista de instâncias eᵢ = Sᵢ ⊗ G ⊗ Cᵢ
            embeddings: Matriz (n, d) — se None, usa TF-IDF

        Returns:
            ResultadoCSI com valor, limiar τ e classificação
        """
        # Obter embeddings
        if embeddings is None:
            embeddings = self._tfidf_embeddings(instancias)
        embeddings = np.array(embeddings)

        # Calcular CSI
        csi, csi_por_instancia = self._calcular_csi(embeddings)

        # Estimar τ via bootstrap (distribuição nula)
        tau = self._estimar_tau(instancias, len(instancias))

        # Classificar
        if csi >= tau:
            significativo = True
            categoria = "significativo"
        elif csi >= tau * 0.75:
            significativo = False
            categoria = "parcial"
        else:
            significativo = False
            categoria = "insignificante"

        return ResultadoCSI(
            csi=float(csi),
            tau=float(tau),
            significativo=significativo,
            csi_por_instancia=[float(c) for c in csi_por_instancia],
            categoria=categoria
        )

    def _calcular_csi(self, embeddings: np.ndarray) -> Tuple[float, List[float]]:
        """
        CSI = (1/n) Σ sim(φ(eᵢ), ē_φ)
        onde sim é similaridade cosseno e ē_φ é o centróide semântico.
        """
        n = embeddings.shape[0]
        centroidoide = np.mean(embeddings, axis=0)
        norm_c = np.linalg.norm(centroidoide)

        csi_por_instancia = []
        for i in range(n):
            emb = embeddings[i]
            norm_e = np.linalg.norm(emb)
            if norm_e > 0 and norm_c > 0:
                cosseno = np.dot(emb, centroidoide) / (norm_e * norm_c)
            else:
                cosseno = 0.0
            csi_por_instancia.append(cosseno)

        csi = float(np.mean(csi_por_instancia))
        return csi, csi_por_instancia

    def _estimar_tau(self, instancias: List[str], n: int) -> float:
        """
        Estima τ = p₇₅ da distribuição nula via bootstrap.

        Sob H₀: instâncias geradas aleatoriamente do vocabulário e tamanho
        do corpus observado.
        """
        rng = np.random.RandomState(self.sementes)

        # Construir vocabulário do corpus
        palavras = []
        for inst in instancias:
            palavras.extend(inst.split())
        palavras = list(set(palavras))

        if not palavras or n < 2:
            return 0.5

        csi_nulos = []
        for _ in range(self.n_bootstrap):
            # Gerar lista aleatória do mesmo tamanho e vocabulário
            lista_aleatoria = []
            for _ in range(n):
                tam = rng.randint(2, max(3, max(len(inst) for inst in instancias)) + 1)
                lista_aleatoria.append(' '.join(rng.choice(palavras, tam)))

            # Calcular CSI dessa lista
            emb = self._tfidf_embeddings(lista_aleatoria)
            csi_null, _ = self._calcular_csi(emb)
            csi_nulos.append(csi_null)

        tau = float(np.percentile(csi_nulos, self.percentil))
        return tau

    def _tfidf_embeddings(self, textos: List[str]) -> np.ndarray:
        """Gera embeddings via TF-IDF como fallback."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.decomposition import TruncatedSVD
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
