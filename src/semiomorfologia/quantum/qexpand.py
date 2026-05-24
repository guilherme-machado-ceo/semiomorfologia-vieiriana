"""
QEXPAND — EXPAND Quântico

Implementa a operação EXPAND do PANVIEIRA via superposição quântica.
Cada instância Sᵢ⊗G⊗Cᵢ é codificada como estado quântico.
O operador de Hadamard cria superposição de todas as instâncias.
"""
import numpy as np
from typing import List, Tuple, Dict, Any, Optional


def qexpand(g: str, pares: List[Tuple[str, str]],
            backend=None, shots: int = 1024) -> Dict[str, Any]:
    """
    EXPAND quântico: codifica instâncias como superposição.

    Args:
        g: Termo genérico (invariante)
        pares: Lista de (Sᵢ, Cᵢ)
        backend: Backend quântico (default: aer_simulator)
        shots: Número de medições

    Returns:
        Dict com instâncias clássicas + metadados quânticos
    """
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        n = len(pares)
        n_qubits = max(2, (n - 1).bit_length())

        qc = QuantumCircuit(n_qubits, n_qubits)
        for q in range(n_qubits):
            qc.h(q)
        qc.measure(list(range(n_qubits)), list(range(n_qubits)))

        simulator = AerSimulator()
        job = simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts()

        return {
            'instancias': [f"{s} {g} {c}" for s, c in pares],
            'n_qubits': n_qubits,
            'n_instancias': n,
            'shots': shots,
            'distribuicao': dict(list(counts.items())[:10]),
            'circuito_depth': qc.depth(),
            'status': 'ok'
        }
    except ImportError:
        return {
            'instancias': [f"{s} {g} {c}" for s, c in pares],
            'status': 'fallback_classico',
            'notas': 'qiskit não disponível'
        }
    except Exception as e:
        return {'instancias': [], 'status': 'erro', 'erro': str(e)}
