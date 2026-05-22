"""
Classe base para extratores de analogias.
Define o contrato que todo extrator especializado deve implementar.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Callable

from semiomorfologia.core.ontologia import Morfema, Analogia, TipoAnalogia, DominioNatural


class ExtratorAnalogias(ABC):
    """
    Classe base abstrata para extratores especializados por domínio.

    Cada domínio natural (mineral, vegetal, animal, humano) implementa
    seus próprios critérios para as 3 tipologias de analogia.
    """

    def __init__(self, dominio: DominioNatural) -> None:
        self.dominio = dominio
        self.heuristicas: List[Callable[[Morfema, Morfema], bool]] = []
        self.funcionais: List[Callable[[Morfema, Morfema], bool]] = []
        self.homologicas: List[Callable[[Morfema, Morfema], bool]] = []

    @abstractmethod
    def extrair_heuristica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Extrai analogias heurísticas: descobertas não-óbvias, emergências."""
        ...

    @abstractmethod
    def extrair_funcional(self, corpus: List[Morfema]) -> List[Analogia]:
        """Extrai analogias funcionais: mesma função, estrutura diferente."""
        ...

    @abstractmethod
    def extrair_homologica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Extrai analogias homológicas: mesma origem/evolução."""
        ...

    def processar(self, corpus: List[Morfema]) -> Dict[TipoAnalogia, List[Analogia]]:
        """
        Executa os 3 algoritmos de extração para o domínio.

        Returns:
            Dicionário mapeando TipoAnalogia -> lista de Analogias extraídas.
        """
        return {
            TipoAnalogia.HEURISTICA: self.extrair_heuristica(corpus),
            TipoAnalogia.FUNCIONAL: self.extrair_funcional(corpus),
            TipoAnalogia.HOMOLOGICA: self.extrair_homologica(corpus),
        }
