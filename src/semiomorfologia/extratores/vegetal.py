"""
ExtratorVegetal: Algoritmo na natureza vegetal.
Prescruta analogias (heurística, funcional, homológica) em plantas.
"""
from typing import List, Dict

from semiomorfologia.core.ontologia import Morfema, Analogia, TipoAnalogia, DominioNatural
from semiomorfologia.extratores.base import ExtratorAnalogias


class ExtratorVegetal(ExtratorAnalogias):
    """
    Extrator especializado para o domínio vegetal.

    Aplicações típicas:
        - Agronegócio resiliente
        - Farmacologia natural
        - Bioarquitetura
        - Cosmética bioativa
    """

    def __init__(self) -> None:
        super().__init__(DominioNatural.VEGETAL)

    def extrair_heuristica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Heurística vegetal: estratégias de sobrevivência em estresse extremo."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._estresse_extremo(m1) and self._estresse_extremo(m2):
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HEURISTICA,
                            forca=0.85,
                            mapeamento={"mecanismo_resistencia": "transferivel"},
                            aplicacao_industrial=(
                                f"Cultivo resiliente: cruzamento de "
                                f"estratégias {m1.id}×{m2.id}"
                            ),
                        )
                    )
        return analogias

    def extrair_funcional(self, corpus: List[Morfema]) -> List[Analogia]:
        """Funcional vegetal: mesmo processo fisiológico em espécies distintas."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._funcao_fisiologica_equivalente(m1, m2):
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.FUNCIONAL,
                            forca=0.9,
                            mapeamento={
                                "processo_fisiologico": str(m1.descritores.get("processo", ""))
                            },
                            aplicacao_industrial=(
                                f"Bioengenharia: replicação de "
                                f"{m1.descritores.get('processo', 'processo')} em {m2.id}"
                            ),
                        )
                    )
        return analogias

    def extrair_homologica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Homológica vegetal: mesma família botânica, espécies diferentes."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._homologia_evolutiva(m1, m2):
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HOMOLOGICA,
                            forca=0.75,
                            mapeamento={
                                "ancestral_comum": str(m1.descritores.get("familia", ""))
                            },
                            aplicacao_industrial=(
                                f"Fitoprospecção na família "
                                f"{m1.descritores.get('familia', '')}: novos compostos"
                            ),
                        )
                    )
        return analogias

    def _estresse_extremo(self, m: Morfema) -> bool:
        return m.descritores.get("ambiente") in [
            "desertico", "alpino", "salino", "radiacao_uv"
        ]

    def _funcao_fisiologica_equivalente(self, m1: Morfema, m2: Morfema) -> bool:
        return m1.descritores.get("processo") == m2.descritores.get("processo")

    def _homologia_evolutiva(self, m1: Morfema, m2: Morfema) -> bool:
        return (
            m1.descritores.get("familia") == m2.descritores.get("familia")
            and m1.id != m2.id
        )
