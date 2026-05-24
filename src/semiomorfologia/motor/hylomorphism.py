"""
Hylomorfismo PANVIEIRA

Implementação das operações ABSTRACT e EXPAND como catamorfismo (fold)
e anamorfismo (unfold), respectivamente. PANVIEIRA como hylomorfismo:
  unfold(G) -> [S1⊗G⊗C1, ..., Sn⊗G⊗Cn] -> fold(instances) -> G

O hylomorfismo é a composição de um anamorfismo (geração/expansão)
com um catamorfismo (redução/extração), capturando a circularidade
iterativa do padrão vieiriano: G -> EXPAND -> CONTRACT -> G.
"""
from typing import List, Dict, Callable, Any, Optional, Tuple
from functools import reduce
import numpy as np


class HylomorphismEngine:
    """
    Motor de hylomorfismo para o padrão PANVIEIRA.

    Mapeia as 4 operações para o paradigma funcional:
        - EXPAND como anamorfismo (unfold): G -> [e1, ..., en]
        - CONTRACT como catamorfismo (fold): [e1, ..., en] -> G
        - ABSTRACT como catamorfismo sobre instâncias arbitrárias
        - CIRCLE como hylomorfismo: fold ∘ unfold
    """

    def __init__(self, compor: Optional[Callable] = None,
                 reduzir: Optional[Callable] = None):
        self.compor = compor or self._compor_padrao
        self.reduzir = reduzir or self._reduzir_padrao
        self._historico = []

    def _compor_padrao(self, s: str, g: str, c: str) -> str:
        """Operador de composição padrão: justaposição em língua natural."""
        return f"{s} {g} {c}"

    def _reduzir_padrao(self, instancias: List[str]) -> str:
        """Redução padrão: retorna a instância mais comum como proxy de G."""
        if not instancias:
            return ""
        from collections import Counter
        return Counter(instancias).most_common(1)[0][0]

    def unfold(self, g: str, pares: List[Tuple[str, str]]) -> List[str]:
        """
        Anamorfismo (EXPAND): G -> [S1⊗G⊗C1, ..., Sn⊗G⊗Cn]

        Gera instâncias por composição do invariante G com cada par (Sᵢ, Cᵢ).
        Equivalente a map(lambda (s,c): compor(s, g, c), pares).
        """
        return [self.compor(s, g, c) for s, c in pares]

    def fold(self, instancias: List[str]) -> str:
        """
        Catamorfismo (CONTRACT): [e1, ..., en] -> G

        Reduz a série expandida ao genérico G.
        Equivalente a reduce(abstract, instancias).
        """
        return self.reduzir(instancias)

    def abstract(self, instancias: List[str]) -> str:
        """
        ABSTRACT como catamorfismo: extrai G de instâncias arbitrárias.
        Versão semântica:usa similaridade para encontrar o termo mais central.
        """
        if not instancias:
            return ""
        if len(instancias) == 1:
            return instancias[0]

        # Tentar via embeddings para ABSTRACT semântico
        try:
            from semiomorfologia.similaridade.semantica import MotorSemantico
            motor = MotorSemantico()
            embeddings = [motor.vetorizar(inst) for inst in instancias]
            embeddings_validos = [(inst, emb) for inst, emb in zip(instancias, embeddings) if emb is not None]

            if len(embeddings_validos) >= 2:
                mats = [np.array(emb) for _, emb in embeddings_validos]
                centroidoide = np.mean(mats, axis=0)
                # G = instância mais próxima do centróide
                melhor_idx = 0
                melhor_sim = -1
                for i, mat in enumerate(mats):
                    norm = np.linalg.norm(mat)
                    norm_c = np.linalg.norm(centroidoide)
                    if norm > 0 and norm_c > 0:
                        sim = np.dot(mat, centroidoide) / (norm * norm_c)
                        if sim > melhor_sim:
                            melhor_sim = sim
                            melhor_idx = i
                return embeddings_validos[melhor_idx][0]
        except Exception:
            pass

        # Fallback: instância mais frequente
        return self.fold(instancias)

    def hylomorphism(self, g: str, pares: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Hylomorfismo completo: fold ∘ unfold

        Executa a circularidade: G -> EXPAND -> SERIALIZE -> CONTRACT -> G.
        Verifica a invariância de G (Proposição 1).

        Returns:
            Dict com 'G_original', 'instancias', 'G_recuperado', 'invariante'
        """
        instancias = self.unfold(g, pares)
        g_recuperado = self.fold(instancias)
        invariante = (g == g_recuperado)

        resultado = {
            'G_original': g,
            'instancias': instancias,
            'G_recuperado': g_recuperado,
            'invariante': invariante,
            'n_instancias': len(instancias)
        }

        self._historico.append(resultado)
        return resultado

    def circle(self, g: str, pares: List[Tuple[str, str]], n_iter: int = 1) -> List[Dict]:
        """
        CIRCULARIDADE: executa o hylomorfismo n vezes.
        Cada ciclo usa o G_recuperado como entrada do próximo.

        Propriedade esperada: G se mantém invariante a cada iteração.
        """
        resultados = []
        g_atual = g
        for _ in range(n_iter):
            res = self.hylomorphism(g_atual, pares)
            resultados.append(res)
            g_atual = res['G_recuperado']
        return resultados

    def obter_historico(self) -> List[Dict]:
        """Retorna o histórico de execuções do hylomorfismo."""
        return self._historico
