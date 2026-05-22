"""
Avaliação de Technology Readiness Level (TRL) para proposições tecnológicas.
Escala 1-9 adaptada para analogias semiomorfológicas.
"""
from enum import Enum
from typing import Dict

from semiomorfologia.core.ontologia import Analogia, TipoAnalogia, DominioNatural


class TRLNivel(Enum):
    """Níveis TRL padronizados pela NASA/EC."""
    TRL1 = (1, "Princípio básico observado")
    TRL2 = (2, "Conceito tecnológico formulado")
    TRL3 = (3, "Prova de conceito experimental")
    TRL4 = (4, "Validação em laboratório")
    TRL5 = (5, "Validação em ambiente relevante")
    TRL6 = (6, "Demonstração de protótipo")
    TRL7 = (7, "Demonstração em ambiente operacional")
    TRL8 = (8, "Sistema completo qualificado")
    TRL9 = (9, "Sistema comprovado em missão")

    def __init__(self, nivel: int, descricao: str) -> None:
        self.nivel = nivel
        self.descricao = descricao


class AvaliadorTRL:
    """Avalia TRL inicial baseado no tipo de analogia e domínios envolvidos."""

    def avaliar(self, analogia: Analogia) -> Dict[str, any]:
        nivel = self._calcular_nivel(analogia)
        return {
            "nivel": nivel.nivel,
            "descricao": nivel.descricao,
            "justificativa": self._justificar(analogia, nivel),
            "proximo_passo": self._proximo_passo(nivel),
        }

    def _calcular_nivel(self, analogia: Analogia) -> TRLNivel:
        base = 2 if analogia.tipo == TipoAnalogia.HEURISTICA else 4

        # Bonus por maturidade de domínio
        if analogia.fonte.dominio == DominioNatural.HUMANO and analogia.alvo.dominio == DominioNatural.ANIMAL:
            base += 3  # Modelos animais bem estabelecidos
        elif analogia.fonte.dominio == analogia.alvo.dominio:
            base += 1  # Mesmo domínio = mais previsível

        # Bonus por força da analogia
        if analogia.forca > 0.9:
            base += 1

        nivel = min(max(base, 1), 9)
        return list(TRLNivel)[nivel - 1]

    def _justificar(self, analogia: Analogia, nivel: TRLNivel) -> str:
        justificativas = {
            TipoAnalogia.HEURISTICA: "Analogia heurística requer validação experimental inicial.",
            TipoAnalogia.FUNCIONAL: "Analogia funcional permite prototipagem acelerada.",
            TipoAnalogia.HOMOLOGICA: "Analogia homológica beneficia-se de conhecimento acumulado.",
        }
        return justificativas.get(analogia.tipo, "Avaliação padrão.")

    def _proximo_passo(self, nivel: TRLNivel) -> str:
        proximos = {
            1: "Revisão bibliográfica e formulação de hipótese",
            2: "Simulação computacional preliminar",
            3: "Experimento de prova de conceito",
            4: "Validação em ambiente controlado",
            5: "Teste em campo/ambiente alvo",
            6: "Desenvolvimento de protótipo integrado",
            7: "Demonstração operacional completa",
            8: "Qualificação e certificação",
            9: "Implantação e monitoramento",
        }
        return proximos.get(nivel.nivel, "Reavaliação estratégica")
