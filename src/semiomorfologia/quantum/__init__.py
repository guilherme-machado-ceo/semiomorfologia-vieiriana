"""
Módulo Quântico Experimental — H-PANVIEIRA

Implementação híbrida (clássico + quântico) do Algoritmo PANVIEIRA.
Requer qiskit para execução. Funciona em modo simulação sem hardware quântico.
"""
from .hpanvieira import HPANVIEIRA

__all__ = ['HPANVIEIRA']
