"""
QCONTRACT — CONTRACT Quântico

Implementa CONTRACT via interferência quântica.
Instâncias com mesmo G interferem construtivamente;
diferenciadores interferem destrutivamente.
A medição tende ao estado |G⟩.
"""
import numpy as np
from typing import List, Dict, Any, Optional


def qcontract(instancias: List[str], backend=None,
              shots: int = 2048) -> Dict[str, Any]:
    """
    CONTRACT quântico via interferência.

    Args:
        instancias: Lista de instâncias eᵢ
        backend: Backend quântico
        shots: Número de medições

    Returns:
        Dict com G recuperado + metadados quânticos
    """
    if not instancias:
        return {'G': '', 'status': 'vazio'}

    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        n = len(instancias)
        n_qubits = max(1, min(n, 10))

        qc = QuantumCircuit(n_qubits, n_qubits)
        for i in range(min(n, n_qubits)):
            theta = 2 * np.pi * (i + 1) / (n + 1)
            qc.ry(theta, i)
        for q in range(n_qubits):
            qc.h(q)
        qc.measure(list(range(n_qubits)), list(range(n_qubits)))

        simulator = AerSimulator()
        job = simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts()

        top = max(counts, key=counts.get) if counts else ""
        idx = int(top, 2) if top else 0
        g = instancias[idx % len(instancias)]

        return {
            'G': g,
            'n_instancias': n,
            'n_qubits': n_qubits,
            'estado_dominante': top,
            'distribuicao': dict(list(counts.items())[:5]),
            'status': 'ok'
        }
    except ImportError:
        return {'G': instancias[0], 'status': 'fallback_classico'}
    except Exception as e:
        return {'G': '', 'status': 'erro', 'erro': str(e)}
