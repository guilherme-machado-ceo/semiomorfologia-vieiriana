"""
ExtratorMineral: Algoritmo na natureza mineral.
Prescruta analogias (heurística, funcional, homológica) em pedras, minérios e terras raras.
"""
from typing import List, Dict
import numpy as np

from semiomorfologia.core.ontologia import Morfema, Analogia, TipoAnalogia, DominioNatural
from semiomorfologia.extratores.base import ExtratorAnalogias
from semiomorfologia.similaridade.metricas import cosseno, sobreposicao_descritores, distancia_combinada, euclidiana


class ExtratorMineral(ExtratorAnalogias):
    """
    Extrator especializado para o domínio mineral.

    Aplicações típicas:
        - Materiais avançados e compósitos
        - Engenharia de superfícies
        - Eletrônica e fotônica
        - Mineração sustentável
    """

    def __init__(self) -> None:
        super().__init__(DominioNatural.MINERAL)

    def extrair_heuristica(self, corpus: List[Morfema]) -> List[Analogia]:
        """
        Heurística mineral: emergência não-linear de propriedades.

        Detecta pares onde propriedades comuns se comportam de forma
        não-correlacionada, sugerindo fenômenos emergentes transferíveis.
        """
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._emergencia_nao_linear(m1, m2):
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HEURISTICA,
                            forca=self._calcular_forca_emergencia(m1, m2),
                            mapeamento=self._mapear_propriedades(m1, m2),
                            aplicacao_industrial=self._inferir_aplicacao(m1, m2, "heuristica"),
                        )
                    )
        return analogias

    def extrair_funcional(self, corpus: List[Morfema]) -> List[Analogia]:
        """
        Funcional mineral: mesma função, estrutura cristalográfica diferente.

        Exemplo: isolamento térmico em aerogel de sílica vs. isolamento
        em estruturas porosas de zeólitas.
        """
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._funcao_equivalente(m1, m2):
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.FUNCIONAL,
                            forca=self._calcular_similaridade_funcional(m1, m2),
                            mapeamento=self._mapear_funcoes(m1, m2),
                            aplicacao_industrial=self._inferir_aplicacao(m1, m2, "funcional"),
                        )
                    )
        return analogias

    def extrair_homologica(self, corpus: List[Morfema]) -> List[Analogia]:
        """
        Homológica mineral: mesma origem cristalográfica / elemento base.

        Exemplo clássico: diamante, grafite, grafeno (carbono allotrópico).
        """
        analogias: List[Analogia] = []
        for i, m1 in enumerate(corpus):
            for m2 in corpus[i + 1 :]:
                if self._origem_comum(m1, m2):
                    analogias.append(
                        Analogia(
                            fonte=m1,
                            alvo=m2,
                            tipo=TipoAnalogia.HOMOLOGICA,
                            forca=self._calcular_proximidade_estrutural(m1, m2),
                            mapeamento=self._mapear_estrutura(m1, m2),
                            aplicacao_industrial=self._inferir_aplicacao(m1, m2, "homologica"),
                        )
                    )
        return analogias

    # --- Critérios específicos ---

    def _emergencia_nao_linear(self, m1: Morfema, m2: Morfema) -> bool:
        """Verifica se propriedades comuns têm comportamento não-linear."""
        props_comuns = set(m1.propriedades.keys()) & set(m2.propriedades.keys())
        if len(props_comuns) < 2:
            return False
        v1 = m1.vetor_propriedades()
        v2 = m2.vetor_propriedades()
        if len(v1) < 2 or len(v2) < 2:
            return False
        try:
            corr = float(np.corrcoef(v1, v2)[0, 1])
            return abs(corr) < 0.3  # Baixa correlação = emergência
        except Exception:
            return False

    def _funcao_equivalente(self, m1: Morfema, m2: Morfema) -> bool:
        return m1.descritores.get("funcao") == m2.descritores.get("funcao")

    def _origem_comum(self, m1: Morfema, m2: Morfema) -> bool:
        return m1.descritores.get("elemento_base") == m2.descritores.get("elemento_base")

    # --- Cálculo de força ---

    def _calcular_forca_emergencia(self, m1: Morfema, m2: Morfema) -> float:
        # Use cosine similarity on COMMON properties only
        props_comuns = sorted(set(m1.propriedades.keys()) & set(m2.propriedades.keys()))
        if len(props_comuns) >= 2:
            vals1 = [m1.propriedades[k] for k in props_comuns]
            vals2 = [m2.propriedades[k] for k in props_comuns]
            return cosseno(vals1, vals2)
        # Fallback to descriptor overlap
        return sobreposicao_descritores(
            {"descritores": list(m1.descritores.values())},
            {"descritores": list(m2.descritores.values())},
        )

    def _calcular_similaridade_funcional(self, m1: Morfema, m2: Morfema) -> float:
        return distancia_combinada(
            {"descritores": list(m1.descritores.values()), "propriedades": m1.propriedades},
            {"descritores": list(m2.descritores.values()), "propriedades": m2.propriedades},
        )

    def _calcular_proximidade_estrutural(self, m1: Morfema, m2: Morfema) -> float:
        v1, v2 = m1.vetor_propriedades().tolist(), m2.vetor_propriedades().tolist()
        if len(v1) > 0 and len(v2) > 0 and len(v1) == len(v2):
            return cosseno(v1, v2)
        return 0.5

    # --- Mapeamentos ---

    def _mapear_propriedades(self, m1: Morfema, m2: Morfema) -> Dict[str, str]:
        comuns = set(m1.propriedades.keys()) & set(m2.propriedades.keys())
        return {k: k for k in comuns}

    def _mapear_funcoes(self, m1: Morfema, m2: Morfema) -> Dict[str, str]:
        return {"funcao": str(m1.descritores.get("funcao", ""))}

    def _mapear_estrutura(self, m1: Morfema, m2: Morfema) -> Dict[str, str]:
        return {
            "estrutura_cristalina": "equivalente",
            "sistema": str(m1.descritores.get("sistema_cristalino", "")),
        }

    def _inferir_aplicacao(self, m1: Morfema, m2: Morfema, tipo: str) -> str:
        aplicacoes = {
            "heuristica": f"Novo material compósito inspirado em {m1.id}+{m2.id}",
            "funcional": (
                f"Substituição sustentável de {m1.id} por {m2.id} "
                f"em {m1.descritores.get('funcao', 'aplicação')}"
            ),
            "homologica": (
                f"Engenharia de allotropos: otimização de "
                f"{m1.descritores.get('elemento_base', 'material')}"
            ),
        }
        return aplicacoes.get(tipo, "Pesquisa básica em materiais")
