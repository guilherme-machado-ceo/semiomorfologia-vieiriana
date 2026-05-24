"""
ABSTRACT via K-Means

Identifica automaticamente o invariante G de um conjunto de instâncias
usando clustering (K-Means). O centróide do cluster dominante é o
candidato a G — a abstração máxima do padrão PANVIEIRA.
"""
import numpy as np
from typing import List, Dict, Optional, Tuple


class AbstractKMeans:
    """
    ABSTRACT via clustering de embeddings.

    Usa K-Means para identificar o termo genérico G como o centróide
    do cluster mais representativo de um conjunto de instâncias semióticas.
    """

    def __init__(self, k: int = 1, max_iter: int = 100, n_init: int = 10):
        self.k = k
        self.max_iter = max_iter
        self.n_init = n_init

    def abstract(self, instancias: List[str],
                 embeddings: Optional[np.ndarray] = None) -> Dict[str, any]:
        """
        Extrai G via clustering.

        Args:
            instancias: Lista de instâncias eᵢ
            embeddings: Matriz (n, d) — se None, usa TF-IDF

        Returns:
            Dict com 'G' (instância mais próxima do centróide),
            'cluster_labels', 'n_clusters', 'csi_estimada'
        """
        if embeddings is None:
            embeddings = self._tfidf_embeddings(instancias)
        embeddings = np.array(embeddings)
        n = len(instancias)

        if n <= 1:
            return {
                'G': instancias[0] if instancias else '',
                'cluster_labels': [0] * n,
                'n_clusters': 1,
                'csi_estimada': 1.0
            }

        k = min(self.k, n)

        # K-Means
        try:
            from sklearn.cluster import KMeans
            km = KMeans(n_clusters=k, max_iter=self.max_iter,
                       n_init=self.n_init, random_state=42)
            labels = km.fit_predict(embeddings)

            # Cluster dominante (maior)
            from collections import Counter
            contagem = Counter(labels)
            cluster_dominante = contagem.most_common(1)[0][0]

            # G = instância mais próxima do centróide do cluster dominante
            centroido_dominante = km.cluster_centers_[cluster_dominante]
            idx_dominante = [i for i, l in enumerate(labels) if l == cluster_dominante]

            melhor_idx = idx_dominante[0]
            melhor_sim = -1
            for i in idx_dominante:
                sim = np.dot(embeddings[i], centroido_dominante) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(centroido_dominante) + 1e-10)
                if sim > melhor_sim:
                    melhor_sim = sim
                    melhor_idx = i

            # CSI estimada = similaridade intra-cluster dominante
            csi = float(np.mean([
                np.dot(embeddings[i], centroido_dominante) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(centroido_dominante) + 1e-10)
                for i in idx_dominante
            ]))

            return {
                'G': instancias[melhor_idx],
                'cluster_labels': labels.tolist(),
                'n_clusters': k,
                'csi_estimada': csi,
                'cluster_dominante': int(cluster_dominante),
                'n_no_dominante': len(idx_dominante)
            }
        except ImportError:
            # Fallback sem sklearn: G = instância mais central
            centroidoide = np.mean(embeddings, axis=0)
            melhor_idx = 0
            melhor_sim = -1
            for i in range(n):
                sim = np.dot(embeddings[i], centroidoide) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(centroidoide) + 1e-10)
                if sim > melhor_sim:
                    melhor_sim = sim
                    melhor_idx = i
            return {
                'G': instancias[melhor_idx],
                'cluster_labels': [0] * n,
                'n_clusters': 1,
                'csi_estimada': float(melhor_sim)
            }

    def _tfidf_embeddings(self, textos: List[str]) -> np.ndarray:
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
        dim = 64
        mat = np.zeros((len(textos), dim))
        for i, t in enumerate(textos):
            for j, ch in enumerate(t[:dim*4]):
                mat[i, j % dim] += ord(ch) * (0.1 ** (j // dim))
            norm = np.linalg.norm(mat[i])
            if norm > 0:
                mat[i] /= norm
        return mat
