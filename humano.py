"""
ExtratorHumano: Algoritmo na natureza humana.
Prescruta analogias (heurística, funcional, homológica) na humanidade 
(fisiologia/biologia) e nas línguas naturais (morfologia).
"""
from typing import List, Dict

from semiomorfologia.core.ontologia import Morfema, Analogia, TipoAnalogia, DominioNatural
from semiomorfologia.extratores.base import ExtratorAnalogias
from semiomorfologia.similaridade.metricas import cosseno, sobreposicao_descritores, jaccard


class ExtratorHumano(ExtratorAnalogias):
    """
    Extrator especializado para o domínio humano.

    Aplicações típicas:
        - Medicina de precisão
        - NLP biomimético e IA explicável
        - Interface cérebro-computador
        - Farmacogenômica
        - Linguística computacional
    """

    def __init__(self) -> None:
        super().__init__(DominioNatural.HUMANO)

    def extrair_heuristica(self, corpus: List[Morfema]) -> List[Analogia]:
        """
        Heurística humana: isomorfismos corpo-linguagem (semiomorfologia pura).

        Detecta correspondências estruturais entre sistemas biológicos e
        unidades linguísticas, e.g., neurônio espelho ↔ sintaxe recursiva.
        """
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._isomorfismo_corpo_linguagem(m1, m2):
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
                            mapeamento={"estrutura_profunda": "corpo↔linguagem"},
                            aplicacao_industrial=(
                                f"NLP biomimético: modelo de linguagem baseado em "
                                f"{m1.descritores.get('sistema_biologico', 'fisiologia')}"
                            ),
                        )
                    )
        return analogias

    def extrair_funcional(self, corpus: List[Morfema]) -> List[Analogia]:
        """Funcional humana: mesma função cognitiva em substratos distintos."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._funcao_cognitiva_equivalente(m1, m2):
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
                            mapeamento={
                                "funcao_cognitiva": str(m1.descritores.get("funcao_cognitiva", ""))
                            },
                            aplicacao_industrial=(
                                f"IA explicável: arquitetura inspirada em "
                                f"{m1.descritores.get('funcao_cognitiva', 'função')} humana"
                            ),
                        )
                    )
        return analogias

    def extrair_homologica(self, corpus: List[Morfema]) -> List[Analogia]:
        """Homológica humana: mesma via desenvolvimental em tecidos distintos."""
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._homologia_desenvolvimental(m1, m2):
                    forca = jaccard(set(m1.descritores.keys()), set(m2.descritores.keys()))
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HOMOLOGICA,
                            forca=forca,
                            mapeamento={
                                "via_desenvolvimental": str(m1.descritores.get("via", ""))
                            },
                            aplicacao_industrial=(
                                f"Medicina regenerativa: ativação de via "
                                f"{m1.descritores.get('via', 'via')} em "
                                f"{m2.descritores.get('tecido_alvo', 'tecido')}"
                            ),
                        )
                    )
        return analogias

    def _isomorfismo_corpo_linguagem(self, m1: Morfema, m2: Morfema) -> bool:
        return (
            m1.descritores.get("tipo") == "biologico"
            and m2.descritores.get("tipo") == "linguistico"
            and m1.descritores.get("estrutura_profunda")
            == m2.descritores.get("estrutura_profunda")
        )

    def _funcao_cognitiva_equivalente(self, m1: Morfema, m2: Morfema) -> bool:
        return m1.descritores.get("funcao_cognitiva") == m2.descritores.get("funcao_cognitiva")

    def _homologia_desenvolvimental(self, m1: Morfema, m2: Morfema) -> bool:
        return (
            m1.descritores.get("via") == m2.descritores.get("via")
            and m1.descritores.get("tipo") == "biologico"
            and m2.descritores.get("tipo") == "biologico"
        )
