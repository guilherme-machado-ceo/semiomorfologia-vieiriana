#!/usr/bin/env python3
"""Demo mínima — 30 segundos para entender o framework."""
from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao
from semiomorfologia.motor import MotorSemiomorfologico

motor = MotorSemiomorfologico()

# 3 morfemas = 1 sintagma vieiriano
corpus = [
    Morfema("grafeno", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "carbono"}, propriedades={"condutividade": 0.98}),
    Morfema("diamante", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "carbono"}, propriedades={"dureza": 1.0}),
    Morfema("grafite", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "carbono"}, propriedades={"lubrificacao": 0.85}),
]

# Compor → Reduzir → Extrair
sintagma = motor.compor_sintagma(corpus)
print(f"Genérico: {sintagma.conteudo_generico}")

resultados = motor.extrair_analogias_dominio(corpus, DominioNatural.MINERAL)
for tipo, analogias in resultados.items():
    if analogias:
        print(f"{tipo.value}: {len(analogias)} analogias")
        for a in analogias[:2]:
            print(f"  • {a.fonte.id} ↔ {a.alvo.id} → {a.aplicacao_industrial}")
