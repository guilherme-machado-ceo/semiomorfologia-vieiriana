"""
Motor MapReduce PANVIEIRA

Implementa as operações EXPAND e CONTRACT usando o paradigma MapReduce:
    EXPAND ≈ Map: G x {(Sᵢ,Cᵢ)} -> {Sᵢ⊗G⊗Cᵢ}
    CONTRACT ≈ Reduce: {eᵢ} -> G

Permite processamento paralelo de grandes volumes de dados semióticos
(Big Data Semiótico) usando concurrent.futures.
"""
from typing import List, Dict, Callable, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import numpy as np


class MapReduceEngine:
    """
    Motor MapReduce para o padrão PANVIEIRA.

    EXPAND é análogo à fase Map (transformar entrada em pares),
    CONTRACT é análogo à fase Reduce (agregar ao genérico).
    """

    def __init__(self, compor: Optional[Callable] = None,
                 n_workers: int = 4):
        self.compor = compor or self._compor_padrao
        self.n_workers = n_workers

    def _compor_padrao(self, s: str, g: str, c: str) -> str:
        return f"{s} {g} {c}"

    def map_expand(self, g: str, pares: List[Tuple[str, str]],
                   n_workers: Optional[int] = None) -> List[str]:
        """
        Fase MAP (EXPAND paralelo).

        Gera instâncias em paralelo: cada (Sᵢ, Cᵢ) é processado
        independentemente para produzir Sᵢ ⊗ G ⊗ Cᵢ.

        Args:
            g: Termo genérico (invariante)
            pares: Lista de (diferenciador, locus)
            n_workers: Número de threads (default: self.n_workers)

        Returns:
            Lista de instâncias expandidas
        """
        workers = n_workers or self.n_workers
        func = partial(lambda g, par: self.compor(par[0], g, par[1]), g)

        if workers <= 1 or len(pares) <= 1:
            return [self.compor(s, g, c) for s, c in pares]

        instancias = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futuros = {executor.submit(self.compor, s, g, c): (s, c)
                       for s, c in pares}
            for futuro in as_completed(futuros):
                try:
                    instancias.append(futuro.result())
                except Exception as e:
                    s, c = futuros[futuro]
                    instancias.append(f"ERRO: {s} + {g} + {c} -> {e}")

        return instancias

    def reduce_contract(self, instancias: List[str],
                        reduzir: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Fase REDUCE (CONTRACT).

        Agrega instâncias ao genérico G, preservando metadados
        dos diferenciadores (Proposição 1).

        Returns:
            Dict com 'G' (genérico), 'n' (total), 'metadados'
        """
        if not instancias:
            return {'G': '', 'n': 0, 'metadados': []}

        if reduzir:
            g = reduzir(instancias)
        else:
            # Redução semântica via centróide de embeddings
            g = self._reducao_semantica(instancias)

        return {
            'G': g,
            'n': len(instancias),
            'metadados': instancias  # metadados dos Sᵢ, Cᵢ
        }

    def _reducao_semantica(self, instancias: List[str]) -> str:
        """Redução semântica: instância mais próxima do centróide."""
        try:
            from semiomorfologia.similaridade.semantica import MotorSemantico
            motor = MotorSemantico()
            embeddings = [motor.vetorizar(inst) for inst in instancias]
            validos = [(inst, emb) for inst, emb in zip(instancias, embeddings) if emb is not None]

            if len(validos) >= 2:
                mats = [np.array(e) for _, e in validos]
                cent = np.mean(mats, axis=0)
                melhor_sim = -1
                melhor_inst = validos[0][0]
                for inst, mat in validos:
                    norm = np.linalg.norm(mat)
                    norm_c = np.linalg.norm(cent)
                    if norm > 0 and norm_c > 0:
                        sim = np.dot(mat, cent) / (norm * norm_c)
                        if sim > melhor_sim:
                            melhor_sim = sim
                            melhor_inst = inst
                return melhor_inst
        except Exception:
            pass

        # Fallback: instância mais frequente
        from collections import Counter
        return Counter(instancias).most_common(1)[0][0]

    def mapreduce(self, g: str, pares: List[Tuple[str, str]],
                  n_workers: Optional[int] = None) -> Dict[str, Any]:
        """
        Pipeline MapReduce completa: EXPAND -> CONTRACT

        Equivalente ao hylomorfismo, mas com paralelização explícita.
        """
        expandido = self.map_expand(g, pares, n_workers)
        resultado = self.reduce_contract(expandido)
        resultado['G_original'] = g
        resultado['invariante'] = (resultado['G'] == g)
        return resultado
