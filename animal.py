"""
ExtratorAnimal: Algoritmo na natureza animal.
Prescruta analogias (heurística, funcional, homológica) nos bichos.
"""
from typing import List, Dict

from semiomorfologia.core.ontologia import Morfema, Analogia, TipoAnalogia, DominioNatural
from semiomorfologia.extratores.base import ExtratorAnalogias
from semiomorfologia.similaridade.metricas import cosseno, sobreposicao_descritores, jaccard


class ExtratorAnimal(ExtratorAnalogias):
    """
    Extrator especializado para o domínio animal.

    Aplicações típicas:
        - Robótica biomimética
        - Aeroespacial e hidrodinâmica
        - Materiais bioinspirados
        - Medicina veterinária traduzida
    """

    def __init__(self) -> None:
        super().__init__(DominioNatural.ANIMAL)

    def extrair_heuristica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Heurística animal: convergência evolutiva não-óbvia entre filos distintos."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._convergencia_nao_obvia(m1, m2):
                    v1, v2 = m1.vetor_propriedades().tolist(), m2.vetor_propriedades().tolist()
                    if len(v1) > 0 and len(v2) > 0 and len(v1) == len(v2):
                        forca = cosseno(v1, v2)
                    else:
                        forca = 0.5
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HEURISTICA,
                            forca=forca,
                            mapeamento={
                                "solucao_convergente": str(m1.descritores.get("adaptacao", ""))
                            },
                            aplicacao_industrial=(
                                f"Inovação biomimética: "
                                f"{m1.descritores.get('adaptacao', '')} em sistemas artificiais"
                            ),
                        )
                    )
        return analogias

    def extrair_funcional(self, corpus: List[Morfema]) -> List[Analogia]:
        """Funcional animal: mesmo sistema biológico em espécies distintas."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._sistema_biologico_equivalente(m1, m2):
                    forca = sobreposicao_descritores(
                        {"descritores": list(m1.descritores.values())},
                        {"descritores": list(m2.descritores.values())},
                    )
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.FUNCIONAL,
                            forca=forca,
                            mapeamento={"sistema": str(m1.descritores.get("sistema", ""))},
                            aplicacao_industrial=(
                                f"Engenharia reversa de "
                                f"{m1.descritores.get('sistema', 'sistema')}: {m1.id}→{m2.id}"
                            ),
                        )
                    )
        return analogias

    def extrair_homologica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Homológica animal: mesmo órgão/homologia filogenética."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._homologia_filogenetica(m1, m2):
                    forca = jaccard(set(m1.descritores.keys()), set(m2.descritores.keys()))
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HOMOLOGICA,
                            forca=forca,
                            mapeamento={"orgao_homologo": str(m1.descritores.get("orgao", ""))},
                            aplicacao_industrial=(
                                f"Modelo animal para patologia humana: "
                                f"estudo de {m1.descritores.get('orgao', 'orgão')}"
                            ),
                        )
                    )
        return analogias

    def _convergencia_nao_obvia(self, m1: Morfema, m2: Morfema) -> bool:
        return (
            m1.descritores.get("adaptacao") == m2.descritores.get("adaptacao")
            and m1.descritores.get("filum") != m2.descritores.get("filum")
        )

    def _sistema_biologico_equivalente(self, m1: Morfema, m2: Morfema) -> bool:
        return m1.descritores.get("sistema") == m2.descritores.get("sistema")

    def _homologia_filogenetica(self, m1: Morfema, m2: Morfema) -> bool:
        return (
            m1.descritores.get("orgao") == m2.descritores.get("orgao")
            and m1.descritores.get("filum") == m2.descritores.get("filum")
        )
