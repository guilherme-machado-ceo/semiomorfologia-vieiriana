import numpy as np
from typing import List, Optional
from .metricas import cosseno

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
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            vocab = [" ".join(texto.lower().split())]
            if len(vocab[0].strip()) < 2:
                return None
            tfidf = TfidfVectorizer().fit_transform(vocab)
            return tfidf.toarray()[0].tolist()
        except Exception:
            pass
        tokens = texto.lower().split()
        return [float(hash(t) % 1000) / 1000.0 for t in tokens] if tokens else None

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
