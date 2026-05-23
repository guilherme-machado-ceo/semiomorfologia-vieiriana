import math
from typing import Dict, List, Any
from collections import Counter

class AvaliadorFAME:
    def __init__(self):
        self.resultados = []

    def avaliar(self, pontuacao: float, dimensoes: Dict[str, float] = None) -> Dict[str, Any]:
        if dimensoes is None:
            dimensoes = self._inferir_dimensoes(pontuacao)
        f = round(dimensoes.get("analogia", pontuacao * 0.9), 4)
        a = round(dimensoes.get("significancia", pontuacao * 0.85), 4)
        m = round(dimensoes.get("novidade", max(0, 1.0 - pontuacao) * 0.8), 4)
        e = round(dimensoes.get("solidez", min(1.0, pontuacao * 1.1)), 4)
        u = round(dimensoes.get("utilidade", pontuacao * 0.75), 4)
        i = round(dimensoes.get("informatividade", pontuacao * 0.95), 4)
        vals = [v for v in [f, a, m, e, u, i] if v > 0]
        h = round(len(vals) / sum(1.0 / v for v in vals), 4) if vals else 0.0
        r = {"fame": f, "analogia": f, "significancia": a, "novidade": m, "solidez": e,
             "utilidade": u, "informatividade": i, "media_harmonica": h}
        self.resultados.append(r)
        return r

    def _inferir_dimensoes(self, p: float) -> Dict[str, float]:
        return {"analogia": p * 0.9, "significancia": p * 0.85, "novidade": max(0, 1 - p) * 0.8,
                "solidez": min(1, p * 1.1), "utilidade": p * 0.75, "informatividade": p * 0.95}

    def avaliar_conjunto(self, pontuacoes: List[float]) -> Dict[str, Any]:
        rs = [self.avaliar(p) for p in pontuacoes]
        stats = {}
        for d in ["fame", "analogia", "significancia", "novidade", "solidez", "utilidade", "informatividade", "media_harmonica"]:
            vals = [r[d] for r in rs]
            stats[d] = {"media": round(sum(vals) / len(vals), 4),
                        "min": round(min(vals), 4), "max": round(max(vals), 4)}
        return stats

    def avaliar_contrato(self, resultado_au: Dict) -> Dict[str, Any]:
        g = resultado_au.get("grau_similaridade", 0)
        return self.avaliar(g, {"analogia": g, "significancia": g * 0.9,
                                "novidade": 1 - g, "solidez": min(1, g * 1.05),
                                "utilidade": g * 0.8, "informatividade": g * 0.95})
