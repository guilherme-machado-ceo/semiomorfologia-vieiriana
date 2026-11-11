import hashlib
import re
import numpy as np
from typing import List, Optional
from .metricas import cosseno

DIM_HASH = 512


def _saco_de_palavras(texto: str, dim: int = DIM_HASH) -> Optional[List[float]]:
    """Vetor de contagem de tokens por hashing estável (md5), normalizado."""
    tokens = re.findall(r"\w+", texto.lower())
    if not tokens:
        return None
    v = np.zeros(dim)
    for t in tokens:
        v[int(hashlib.md5(t.encode("utf-8")).hexdigest(), 16) % dim] += 1.0
    n = np.linalg.norm(v)
    return (v / n).tolist() if n > 0 else None

class MotorSemantico:
    def __init__(self, modelo: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.modelo_nome = modelo
        self.modelo = None
        self._vetores_cache = {}
        self._nivel = 0
        self._tentar_carregar()

    def _tentar_carregar(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.modelo = SentenceTransformer(self.modelo_nome)
            self._nivel = 3
        except Exception:
            self._nivel = 0

    def vetorizar(self, texto: str) -> Optional[List[float]]:
        if texto in self._vetores_cache:
            return self._vetores_cache[texto]
        vetor = self._vetorizar_sem_cache(texto)
        if vetor is not None:
            self._vetores_cache[texto] = vetor
        return vetor

    def _vetorizar_sem_cache(self, texto: str) -> Optional[List[float]]:
        if self._nivel == 3 and self.modelo:
            try:
                v = self.modelo.encode([texto])[0]
                return v.tolist()
            except Exception:
                pass
        # Fallback sem modelo: saco de palavras com hashing em dimensão fixa.
        # Antes: TF-IDF ajustado num único documento (todos os vetores ficavam
        # uniformes, e textos de mesmo tamanho davam cosseno 1,0) e hash() do
        # Python (aleatorizado a cada processo, logo não reprodutível).
        return _saco_de_palavras(texto)

    def similaridade(self, t1: str, t2: str) -> float:
        v1, v2 = self.vetorizar(t1), self.vetorizar(t2)
        if v1 is None or v2 is None:
            from difflib import SequenceMatcher
            return SequenceMatcher(None, t1.lower(), t2.lower()).ratio()
        max_len = max(len(v1), len(v2))
        if len(v1) > len(v2):
            v1 = v1[:len(v2)]
        elif len(v2) > len(v1):
            v2 = v2[:len(v1)]
        return cosseno(v1, v2)

    @property
    def nivel(self):
        return self._nivel
