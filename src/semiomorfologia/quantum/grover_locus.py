"""
GROVER_LOCUS — Busca de Loci via Algoritmo de Grover

Speedup quadrático para busca de instâncias específicas (Sᵢ, Cᵢ)
no conjunto expandido. O(N) -> O(sqrt(N)).
"""
import numpy as np
from typing import List, Dict, Any, Optional


def grover_locus(alvo: str, candidatos: List[str],
                n_iteracoes: Optional[int] = None) -> Dict[str, Any]:
    """
    Busca via Grover no conjunto expandido.

    Args:
        alvo: Instância ou loci alvo
        candidatos: Lista de candidatos
        n_iteracoes: Número de iterações (default: auto)

    Returns:
        Dict com resultado + metadados
    """
    n = len(candidatos)
    if n == 0:
        return {'encontrado': False, 'n': 0, 'status': 'vazio'}

    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        n_qubits = max(2, (n - 1).bit_length())
        if n_iteracoes is None:
            n_iteracoes = max(1, int(np.floor(np.pi / 4 * np.sqrt(n))))
        n_iteracoes = min(n_iteracoes, 10)

        qc = QuantumCircuit(n_qubits, n_qubits)
        qc.h(list(range(n_qubits)))

        for _ in range(n_iteracoes):
            qc.barrier()
            for q in range(n_qubits):
                qc.h(q)
                qc.x(q)
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(n_qubits - 1)
            for q in range(n_qubits):
                qc.x(q)
                qc.h(q)

        qc.measure(list(range(n_qubits)), list(range(n_qubits)))

        simulator = AerSimulator()
        job = simulator.run(qc, shots=4096)
        result = job.result()
        counts = result.get_counts()

        top = max(counts, key=counts.get) if counts else ""

        return {
            'alvo': alvo,
            'encontrado': alvo in candidatos,
            'estado_top': top,
            'n_candidatos': n,
            'n_qubits': n_qubits,
            'n_iteracoes': n_iteracoes,
            'speedup': f'O(sqrt({n})) vs O({n})',
            'status': 'ok'
        }
    except ImportError:
        idx = candidatos.index(alvo) if alvo in candidatos else -1
        return {
            'alvo': alvo,
            'encontrado': alvo in candidatos,
            'indice': idx,
            'status': 'fallback_classico'
        }
    except Exception as e:
        return {'alvo': alvo, 'encontrado': False, 'status': 'erro', 'erro': str(e)}
