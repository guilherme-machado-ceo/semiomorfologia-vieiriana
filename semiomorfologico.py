"""
Motor Semiomorfológico Vieiriano
Orquestrador central que implementa:
    1. Composição de sintagmas (redução N→1 genérico)
    2. Reiteração enfática (circularidade vieiriana)
    3. Extração de analogias (3 tipos × 4 domínios)
    4. Pontes cruzadas (inter-domínios)
    5. Geração de conhecimento aplicado (TRL, mercado)
"""
from __future__ import annotations

from typing import List, Dict, Any, Optional

from semiomorfologia.core.ontologia import (
    Morfema, Sintagma, Analogia, TipoAnalogia, DominioNatural
)
from semiomorfologia.extratores import (
    ExtratorMineral, ExtratorVegetal, ExtratorAnimal, ExtratorHumano
)


class MotorSemiomorfologico:
    """
    Motor central do framework semiomorfológico.

    Implementa o processo vieiriano de reiteração enfática e redução
    ao genérico como pipeline computacional de descoberta de analogias.
    """

    def __init__(self) -> None:
        self.extratores = {
            DominioNatural.MINERAL: ExtratorMineral(),
            DominioNatural.VEGETAL: ExtratorVegetal(),
            DominioNatural.ANIMAL: ExtratorAnimal(),
            DominioNatural.HUMANO: ExtratorHumano(),
        }
        self.sintagmas: List[Sintagma] = []
        self.analogias_cruzadas: List[Analogia] = []
        self.base_conhecimento: Dict[str, Any] = {}

    def compor_sintagma(
        self, morfemas: List[Morfema], tipo_reiteracao: str = "paralelistica"
    ) -> Sintagma:
        """
        Composição vieiriana de sintagma paralelístico.

        Exemplo:
            "O carbono persegue a condutividade no grafeno;
             a dureza, no diamante;
             a lubrificação, na grafite"
        → Reduz-se ao genérico: "O carbono [genérico] [persegue 3 propriedades]"
        """
        if not morfemas:
            raise ValueError("Sintagma requer pelo menos um morfema")

        dominios = {m.dominio for m in morfemas}
        if len(dominios) > 1:
            # Sintagmas mistos são permitidos apenas para pontes cruzadas
            pass  # Relaxado para permitir composições híbridas

        sintagma = Sintagma(
            id=f"sintagma_{len(self.sintagmas)}_{morfemas[0].dominio.value}",
            morfemas=morfemas,
            tipo_reiteracao=tipo_reiteracao,
        )
        sintagma.extrair_generico()
        self.sintagmas.append(sintagma)
        return sintagma

    def reiterar_enfaticamente(
        self, sintagma_base: Sintagma, variacoes: List[List[Morfema]]
    ) -> List[Sintagma]:
        """
        Processo de reiteração enfática vieiriana.

        Multiplica o mesmo conteúdo conceptual com variações formais,
        criando circularidade estilística (marca vieiriana).
        """
        reiteracoes = [sintagma_base]
        for i, variacao in enumerate(variacoes):
            nova = Sintagma(
                id=f"reiteracao_{i}_{sintagma_base.id}",
                morfemas=variacao,
                tipo_reiteracao=sintagma_base.tipo_reiteracao,
            )
            nova.extrair_generico()
            reiteracoes.append(nova)
            self.sintagmas.append(nova)
        return reiteracoes

    def extrair_analogias_dominio(
        self, corpus: List[Morfema], dominio: DominioNatural
    ) -> Dict[TipoAnalogia, List[Analogia]]:
        """Executa os 3 algoritmos de extração para um domínio específico."""
        extrator = self.extratores[dominio]
        return extrator.processar(corpus)

    def extrair_analogias_cruzadas(
        self, corpus_multi: Dict[DominioNatural, List[Morfema]]
    ) -> List[Analogia]:
        """
        Extração de analogias TRANSVERSAIS entre domínios.

        Detecta isomorfismos estruturais profundos que conectam
        morfologias distintas (e.g., mineral↔vegetal na biomineralização).
        """
        analogias_cruzadas: List[Analogia] = []
        dominios = list(corpus_multi.keys())

        for i, d1 in enumerate(dominios):
            for d2 in dominios[i + 1 :]:
                for m1 in corpus_multi[d1]:
                    for m2 in corpus_multi[d2]:
                        if self._ponte_cruzada(m1, m2):
                            analogias_cruzadas.append(
                                Analogia(
                                    fonte=m1,
                                    alvo=m2,
                                    tipo=TipoAnalogia.HEURISTICA,
                                    forca=self._forca_ponte(m1, m2),
                                    mapeamento={
                                        "ponte": f"{d1.value}↔{d2.value}",
                                        "isomorfismo": "estrutural",
                                    },
                                    aplicacao_industrial=self._aplicacao_ponte(d1, d2, m1, m2),
                                )
                            )

        self.analogias_cruzadas.extend(analogias_cruzadas)
        return analogias_cruzadas

    def gerar_conhecimento_aplicado(
        self, analogias: List[Analogia]
    ) -> List[Dict[str, Any]]:
        """
        Camada de produção de conhecimento científico aplicado.

        Converte analogias em proposições tecnológicas avaliadas
        por TRL, potencial de mercado e setores industriais.
        """
        conhecimentos: List[Dict[str, Any]] = []
        for analogia in analogias:
            if analogia.forca > 0.75:  # Threshold de viabilidade
                conhecimento = {
                    "tipo_analogia": analogia.tipo.value,
                    "dominio_fonte": analogia.fonte.dominio.value,
                    "dominio_alvo": analogia.alvo.dominio.value,
                    "forca": float(analogia.forca),
                    "proposicao_tecnologica": analogia.aplicacao_industrial,
                    "potencial_mercado": self._avaliar_mercado(analogia),
                    "TRL_inicial": self._estimar_trl(analogia),
                    "dominios_aplicacao": self._mapear_dominios_aplicacao(analogia),
                }
                conhecimentos.append(conhecimento)
        return conhecimentos

    # --- Métodos internos ---

    def _ponte_cruzada(self, m1: Morfema, m2: Morfema) -> bool:
        """Detecta isomorfismos estruturais entre domínios distintos."""
        props_comuns = set(m1.propriedades.keys()) & set(m2.propriedades.keys())
        return len(props_comuns) >= 1 and m1.dominio != m2.dominio

    def _forca_ponte(self, m1: Morfema, m2: Morfema) -> float:
        # Use cosine similarity on aligned property vectors
        from semiomorfologia.similaridade.metricas import cosseno, sobreposicao_descritores
        v1, v2 = m1.vetor_propriedades().tolist(), m2.vetor_propriedades().tolist()
        if len(v1) > 0 and len(v2) > 0 and len(v1) == len(v2):
            return cosseno(v1, v2)
        # Fallback to descriptor overlap
        return sobreposicao_descritores(
            {"descritores": list(m1.descritores.values())},
            {"descritores": list(m2.descritores.values())},
        )

    def _aplicacao_ponte(
        self, d1: DominioNatural, d2: DominioNatural, m1: Morfema, m2: Morfema
    ) -> str:
        return f"Tecnologia híbrida {d1.value[:3]}/{d2.value[:3]}: {m1.id}↔{m2.id}"

    def _avaliar_mercado(self, analogia: Analogia) -> str:
        if analogia.forca > 0.9:
            return "Alto - inovação disruptiva potencial"
        elif analogia.forca > 0.8:
            return "Médio-Alto - melhoria incremental significativa"
        else:
            return "Médio - nicho especializado"

    def _estimar_trl(self, analogia: Analogia) -> int:
        base = 2 if analogia.tipo == TipoAnalogia.HEURISTICA else 4
        if (
            analogia.fonte.dominio == DominioNatural.HUMANO
            and analogia.alvo.dominio == DominioNatural.ANIMAL
        ):
            return min(base + 3, 9)
        return min(base + 1, 9)

    def _mapear_dominios_aplicacao(self, analogia: Analogia) -> List[str]:
        mapeamento = {
            DominioNatural.MINERAL: [
                "Materiais Avançados", "Mineração", "Eletrônica", "Energia"
            ],
            DominioNatural.VEGETAL: [
                "Agronegócio", "Farmacêutica", "Bioarquitetura", "Cosméticos"
            ],
            DominioNatural.ANIMAL: [
                "Robótica", "Aeroespacial", "Medicina", "Materiais"
            ],
            DominioNatural.HUMANO: [
                "Biotech", "IA", "Medicina de Precisão", "Linguística Computacional"
            ],
        }
        fonte_set = set(mapeamento.get(analogia.fonte.dominio, []))
        alvo_set = set(mapeamento.get(analogia.alvo.dominio, []))
        return sorted(list(fonte_set | alvo_set))
