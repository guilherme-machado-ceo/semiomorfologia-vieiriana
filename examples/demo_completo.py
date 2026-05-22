#!/usr/bin/env python3
"""
Demonstração completa do Framework Semiomorfológico Vieiriano.
Executa todo o pipeline: ingestão → composição → extração → aplicação.

Uso:
    python examples/demo_completo.py
"""
from semiomorfologia.core.ontologia import (
    Morfema, DominioNatural, NivelOrganizacao, TipoAnalogia
)
from semiomorfologia.motor import MotorSemiomorfologico
from semiomorfologia.aplicacao import AvaliadorTRL, AvaliadorMercado


def criar_corpus_mineral() -> list[Morfema]:
    """Corpus demonstrativo: alotropos de carbono e terras raras."""
    return [
        Morfema(
            id="grafeno", dominio=DominioNatural.MINERAL, nivel=NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "carbono", "funcao": "condutividade_eletrica", "sistema_cristalino": "hexagonal"},
            propriedades={"condutividade": 0.98, "flexibilidade": 0.95, "transparencia": 0.97}
        ),
        Morfema(
            id="diamante", dominio=DominioNatural.MINERAL, nivel=NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "carbono", "funcao": "dureza_extrema", "sistema_cristalino": "cubico"},
            propriedades={"dureza": 1.0, "condutividade_termica": 0.95, "indice_refracao": 0.99}
        ),
        Morfema(
            id="grafite", dominio=DominioNatural.MINERAL, nivel=NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "carbono", "funcao": "lubrificacao", "sistema_cristalino": "hexagonal"},
            propriedades={"condutividade": 0.85, "flexibilidade": 0.30, "dureza": 0.15}
        ),
        Morfema(
            id="neodimio", dominio=DominioNatural.MINERAL, nivel=NivelOrganizacao.ATOMICO,
            descritores={"elemento_base": "neodimio", "funcao": "magnetismo", "sistema_cristalino": "hexagonal"},
            propriedades={"magnetismo": 0.99, "resistencia_corrosao": 0.60, "densidade": 0.85}
        ),
        Morfema(
            id="aerogel_silica", dominio=DominioNatural.MINERAL, nivel=NivelOrganizacao.MOLECULAR,
            descritores={"elemento_base": "silicio", "funcao": "isolamento_termico", "sistema_cristalino": "amorfo"},
            propriedades={"isolamento_termico": 0.98, "densidade": 0.05, "porosidade": 0.99}
        ),
    ]


def criar_corpus_vegetal() -> list[Morfema]:
    """Corpus demonstrativo: plantas de estresse extremo."""
    return [
        Morfema(
            id="cacto_opuntia", dominio=DominioNatural.VEGETAL, nivel=NivelOrganizacao.ORGANICO,
            descritores={"ambiente": "desertico", "processo": "CAM_fotossintese", "familia": "Cactaceae", "adaptacao": "succulencia"},
            propriedades={"retencao_agua": 0.95, "eficiencia_fotossintese": 0.88, "resistencia_UV": 0.90}
        ),
        Morfema(
            id="edelweiss", dominio=DominioNatural.VEGETAL, nivel=NivelOrganizacao.ORGANICO,
            descritores={"ambiente": "alpino", "processo": "protecao_UV", "familia": "Asteraceae", "adaptacao": "lanosidade"},
            propriedades={"resistencia_UV": 0.98, "isolamento_termico": 0.92, "retencao_agua": 0.75}
        ),
        Morfema(
            id="rizofora_mangle", dominio=DominioNatural.VEGETAL, nivel=NivelOrganizacao.ECOSSISTEMICO,
            descritores={"ambiente": "salino", "processo": "excrecao_sal", "familia": "Rhizophoraceae", "adaptacao": "viviparia"},
            propriedades={"tolerancia_sal": 0.95, "fixacao_coastal": 0.99, "filtracao": 0.90}
        ),
        Morfema(
            id="bambu_moso", dominio=DominioNatural.VEGETAL, nivel=NivelOrganizacao.ORGANICO,
            descritores={"ambiente": "florestal", "processo": "crescimento_rapido", "familia": "Poaceae", "adaptacao": "flexibilidade_mecanica"},
            propriedades={"taxa_crescimento": 0.99, "resistencia_tracao": 0.85, "flexibilidade": 0.90}
        ),
    ]


def criar_corpus_animal() -> list[Morfema]:
    """Corpus demonstrativo: fauna com adaptações extremas."""
    return [
        Morfema(
            id="tardigrado", dominio=DominioNatural.ANIMAL, nivel=NivelOrganizacao.CELULAR,
            descritores={"filum": "Tardigrada", "sistema": "tun_formacao", "adaptacao": "criptobiose", "orgao": "celulas"},
            propriedades={"resistencia_radiacao": 0.99, "desidratacao_reversivel": 0.98, "pressao_extrema": 0.95}
        ),
        Morfema(
            id="abelha_europeia", dominio=DominioNatural.ANIMAL, nivel=NivelOrganizacao.ECOSSISTEMICO,
            descritores={"filum": "Arthropoda", "sistema": "comunicacao_danca", "adaptacao": "forrageio_otimizado", "orgao": "antenas"},
            propriedades={"eficiencia_navegacao": 0.95, "comunicacao_social": 0.98, "otimizacao_energetica": 0.92}
        ),
        Morfema(
            id="tubarao_branco", dominio=DominioNatural.ANIMAL, nivel=NivelOrganizacao.TISSULAR,
            descritores={"filum": "Chordata", "sistema": "regeneracao_dente", "adaptacao": "hidrodinamica", "orgao": "dentes"},
            propriedades={"regeneracao": 0.99, "hidrodinamica": 0.95, "sensorial_eletro": 0.90}
        ),
        Morfema(
            id="polvo_comum", dominio=DominioNatural.ANIMAL, nivel=NivelOrganizacao.ORGANICO,
            descritores={"filum": "Mollusca", "sistema": "camuflagem_neural", "adaptacao": "mimetismo_textural", "orgao": "pele"},
            propriedades={"camuflagem": 0.99, "inteligencia_neural": 0.90, "adaptabilidade_mecanica": 0.88}
        ),
    ]


def criar_corpus_humano() -> list[Morfema]:
    """Corpus demonstrativo: fisiologia e linguagem."""
    return [
        Morfema(
            id="neuronio_espelho", dominio=DominioNatural.HUMANO, nivel=NivelOrganizacao.CELULAR,
            descritores={"tipo": "biologico", "sistema_biologico": "sistema_nervoso", "funcao_cognitiva": "empatia", "via": "desenvolvimento_neural", "estrutura_profunda": "replicacao"},
            propriedades={"sincronizacao": 0.92, "aprendizado_motor": 0.88, "compreensao_intencional": 0.85}
        ),
        Morfema(
            id="sintaxe_recursiva", dominio=DominioNatural.HUMANO, nivel=NivelOrganizacao.ECOSSISTEMICO,
            descritores={"tipo": "linguistico", "sistema_biologico": "linguagem", "funcao_cognitiva": "processamento_hierarquico", "via": "aquisicao_linguagem", "estrutura_profunda": "replicacao"},
            propriedades={"recursividade": 0.99, "geracao_infinita": 0.95, "ambiguidade_resolucao": 0.90}
        ),
        Morfema(
            id="microbioma_intestinal", dominio=DominioNatural.HUMANO, nivel=NivelOrganizacao.ECOSSISTEMICO,
            descritores={"tipo": "biologico", "sistema_biologico": "digestao", "funcao_cognitiva": "modulacao_emocional", "via": "desenvolvimento_microbiano", "tecido_alvo": "epitelio_intestinal"},
            propriedades={"diversidade": 0.98, "resiliencia": 0.85, "sinalizacao_neuro": 0.80}
        ),
        Morfema(
            id="morfema_linguistico", dominio=DominioNatural.HUMANO, nivel=NivelOrganizacao.MOLECULAR,
            descritores={"tipo": "linguistico", "sistema_biologico": "fonologia", "funcao_cognitiva": "distincao_categorial", "via": "aquisicao_fonemica", "estrutura_profunda": "distincao"},
            propriedades={"minimialidade": 0.95, "combinatoria": 0.99, "arbitrariedade": 0.90}
        ),
    ]


def main():
    print("=" * 70)
    print("FRAMEWORK SEMIOMORFOLÓGICO VIEIRIANO — DEMONSTRAÇÃO COMPLETA")
    print("=" * 70)

    motor = MotorSemiomorfologico()
    avaliador_trl = AvaliadorTRL()
    avaliador_mercado = AvaliadorMercado()

    # 1. INGESTÃO
    corpora = {
        DominioNatural.MINERAL: criar_corpus_mineral(),
        DominioNatural.VEGETAL: criar_corpus_vegetal(),
        DominioNatural.ANIMAL: criar_corpus_animal(),
        DominioNatural.HUMANO: criar_corpus_humano(),
    }

    print("\n[1] CORPORA INGESTADOS")
    for dom, corpus in corpora.items():
        print(f"    {dom.value:12s}: {len(corpus)} morfemas")

    # 2. COMPOSIÇÃO VIEIRIANA
    print("\n[2] COMPOSIÇÃO DE SINTAGMA (Redução N→1 genérico)")
    sintagma_carbono = motor.compor_sintagma(corpora[DominioNatural.MINERAL][:3])
    print(f"    Sintagma: {sintagma_carbono.id}")
    print(f"    Genérico extraído: {sintagma_carbono.conteudo_generico}")
    print(f"    Termos específicos: {[m.id for m in sintagma_carbono.morfemas]}")

    # 3. EXTRAÇÃO POR DOMÍNIO
    print("\n[3] EXTRAÇÃO DE ANALOGIAS (3 tipos × 4 domínios)")
    todos_resultados = {}
    for dominio, corpus in corpora.items():
        resultados = motor.extrair_analogias_dominio(corpus, dominio)
        todos_resultados[dominio] = resultados
        total = sum(len(v) for v in resultados.values())
        print(f"\n    {dominio.value.upper()}: {total} analogias")
        for tipo, analogias in resultados.items():
            if analogias:
                print(f"      • {tipo.value:12s}: {len(analogias)} encontradas")
                for a in analogias[:2]:
                    print(f"        - {a.fonte.id} ↔ {a.alvo.id} (força: {a.forca:.2f})")

    # 4. PONTES CRUZADAS
    print("\n[4] ANALOGIAS CRUZADAS (Pontes inter-domínios)")
    pontes = motor.extrair_analogias_cruzadas(corpora)
    print(f"    Total de pontes: {len(pontes)}")
    for p in pontes[:5]:
        print(f"      • {p.fonte.id} ({p.fonte.dominio.value}) ↔ {p.alvo.id} ({p.alvo.dominio.value})")

    # 5. CONHECIMENTO APLICADO
    print("\n[5] CONHECIMENTO CIENTÍFICO APLICADO")
    todas_analogias = []
    for res in todos_resultados.values():
        for analogias in res.values():
            todas_analogias.extend(analogias)
    todas_analogias.extend(pontes)

    conhecimentos = motor.gerar_conhecimento_aplicado(todas_analogias)
    print(f"    Proposições tecnológicas: {len(conhecimentos)}")

    for i, c in enumerate(conhecimentos[:5], 1):
        print(f"\n    [{i}] {c['proposicao_tecnologica']}")
        print(f"         Domínios: {c['dominio_fonte']} → {c['dominio_alvo']}")
        print(f"         Tipo: {c['tipo_analogia']} | Força: {c['forca']:.2f}")
        print(f"         TRL: {c['TRL_inicial']} | Mercado: {c['potencial_mercado']}")

    # 6. AVALIAÇÃO DETALHADA (TRL + Mercado)
    print("\n[6] AVALIAÇÃO DETALHADA TRL/MERCADO")
    for analogia in todas_analogias[:3]:
        trl = avaliador_trl.avaliar(analogia)
        mercado = avaliador_mercado.avaliar(analogia)
        print(f"\n    Analogia: {analogia.fonte.id} → {analogia.alvo.id}")
        print(f"      TRL {trl['nivel']}: {trl['descricao']}")
        print(f"      Mercado: {mercado['potencial']}")
        print(f"      Investimento: {mercado['investimento_necessario']}")

    print("\n" + "=" * 70)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 70)


if __name__ == "__main__":
    main()
