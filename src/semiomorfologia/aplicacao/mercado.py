"""
Avaliação de potencial de mercado para proposições tecnológicas semiomorfológicas.
"""
from typing import Dict, List

from semiomorfologia.core.ontologia import Analogia


class AvaliadorMercado:
    """Avalia potencial comercial baseado em força da analogia e maturidade de domínio."""

    def avaliar(self, analogia: Analogia) -> Dict[str, any]:
        potencial = self._classificar_potencial(analogia)
        riscos = self._identificar_riscos(analogia)

        return {
            "potencial": potencial,
            "riscos": riscos,
            "estimativa_tempo_mercado": self._estimar_tempo(analogia, riscos),
            "investimento_necessario": self._estimar_investimento(analogia),
            "mercados_alvo": self._mapear_mercados(analogia),
        }

    def _classificar_potencial(self, analogia: Analogia) -> str:
        if analogia.forca > 0.9:
            return "ALTO - Inovação disruptiva com barreiras de entrada significativas"
        elif analogia.forca > 0.8:
            return "MÉDIO-ALTO - Melhoria incremental com adoção previsível"
        elif analogia.forca > 0.65:
            return "MÉDIO - Nicho especializado com competição estabelecida"
        else:
            return "BAIXO - Pesquisa básica, aplicação incerta"

    def _identificar_riscos(self, analogia: Analogia) -> List[str]:
        riscos = []
        if analogia.tipo.value == "heuristica":
            riscos.append("Risco técnico: validação experimental necessária")
        if analogia.fonte.dominio != analogia.alvo.dominio:
            riscos.append("Risco de transferência: escalabilidade entre domínios não comprovada")
        if analogia.forca < 0.7:
            riscos.append("Risco de relevância: força da analogia abaixo do threshold ideal")
        return riscos if riscos else ["Risco controlado - maturidade de domínio favorável"]

    def _estimar_tempo(self, analogia: Analogia, riscos: List[str]) -> str:
        base_anos = 3 if analogia.tipo.value == "heuristica" else 1.5
        penalidade = len(riscos) * 0.5
        return f"{base_anos + penalidade:.1f} anos até primeira comercialização"

    def _estimar_investimento(self, analogia: Analogia) -> str:
        if analogia.forca > 0.9:
            return "R$ 5-15M (P&D intensivo, proteção de PI)"
        elif analogia.forca > 0.8:
            return "R$ 1-5M (Desenvolvimento de protótipo, testes)"
        else:
            return "R$ 200K-1M (Pesquisa exploratória, parcerias acadêmicas)"

    def _mapear_mercados(self, analogia: Analogia) -> List[str]:
        mercados = {
            "mineral": ["Materiais Avançados", "Eletrônica", "Energia", "Aeroespacial"],
            "vegetal": ["Agronegócio", "Farmacêutica", "Cosméticos", "Construção Verde"],
            "animal": ["Robótica", "Aeroespacial", "Medicina", "Automotivo"],
            "humano": ["Biotech", "IA", "Medicina de Precisão", "EdTech"],
        }
        fonte = analogia.fonte.dominio.value
        alvo = analogia.alvo.dominio.value
        return list(set(mercados.get(fonte, []) + mercados.get(alvo, [])))
