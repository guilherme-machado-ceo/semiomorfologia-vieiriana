import os
from typing import Dict, List, Any, Tuple


class AntiUnificador:
    def __init__(self, limiar_frequencia: float = 0.6):
        self.limiar = limiar_frequencia
        self.contagem = {}

    def anti_unificar(self, m1: Dict, m2: Dict) -> Dict[str, Any]:
        gen = {"geral": {}, "especifico1": {}, "especifico2": {}, "grau_similaridade": 0.0}
        props1, props2 = m1.get("propriedades", {}), m2.get("propriedades", {})
        todas_chaves = list(set(list(props1.keys()) + list(props2.keys())))
        for k in todas_chaves:
            v1, v2 = props1.get(k), props2.get(k)
            if v1 is not None and v2 is not None:
                if v1 == v2:
                    gen["geral"][k] = v1
                elif isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    gen["geral"][k] = round((v1 + v2) / 2, 4)
                    gen["especifico1"][k] = v1
                    gen["especifico2"][k] = v2
                elif isinstance(v1, str) and isinstance(v2, str):
                    if self._strings_similares(v1, v2):
                        gen["geral"][k] = v1
                    else:
                        gen["geral"][k] = self._variavel_generica(k)
                        gen["especifico1"][k] = v1
                        gen["especifico2"][k] = v2
                else:
                    gen["geral"][k] = self._variavel_generica(k)
                    gen["especifico1"][k] = v1
                    gen["especifico2"][k] = v2
            elif v1 is not None:
                gen["especifico1"][k] = v1
            elif v2 is not None:
                gen["especifico2"][k] = v2
        desc1 = set(str(d) for d in m1.get("descritores", []))
        desc2 = set(str(d) for d in m2.get("descritores", []))
        gen["descritores_comuns"] = list(desc1 & desc2)
        gen["descritores_especificos1"] = list(desc1 - desc2)
        gen["descritores_especificos2"] = list(desc2 - desc1)
        n = max(len(todas_chaves), 1)
        gen["grau_similaridade"] = round(len(gen["geral"]) / n, 4)
        return gen

    def _strings_similares(self, s1: str, s2: str) -> bool:
        from difflib import SequenceMatcher
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio() > 0.7

    def _variavel_generica(self, chave: str) -> str:
        return f"?{chave}_variavel"

    def registrar(self, morfema: Dict):
        desc = tuple(sorted(str(d) for d in morfema.get("descritores", [])))
        if desc not in self.contagem:
            self.contagem[desc] = {"frequencia": 0, "exemplos": []}
        self.contagem[desc]["frequencia"] += 1
        if len(self.contagem[desc]["exemplos"]) < 5:
            self.contagem[desc]["exemplos"].append(morfema.get("nome", "??"))

    def classificar(self, morfema: Dict) -> str:
        desc = tuple(sorted(str(d) for d in morfema.get("descritores", [])))
        total = sum(c["frequencia"] for c in self.contagem.values())
        if desc in self.contagem and total >= 3:
            freq = self.contagem[desc]["frequencia"]
            if freq / total > self.limiar:
                return "comum"
        return "especifico"

    def contrato(self, m1: Dict, m2: Dict) -> Dict[str, Any]:
        au = self.anti_unificar(m1, m2)
        c1 = self.classificar(m1)
        c2 = self.classificar(m2)
        if c1 == "comum" and c2 == "comum":
            au["tipo_contrato"] = "comum_comum"
        elif c1 == "comum" or c2 == "comum":
            au["tipo_contrato"] = "comum_especifico"
        else:
            au["tipo_contrato"] = "especifico_especifico"
        au["c1_classe"] = c1
        au["c2_classe"] = c2
        return au
