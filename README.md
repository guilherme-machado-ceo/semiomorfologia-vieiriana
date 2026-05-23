# Semiomorfologia Vieiriana

> Framework agnostico de extracao de analogias nas 4 morfologias naturais
> Transposicao computacional do Algoritmo PANVIEIRA
>
> **v2.0.0** -- Metricas reais, embeddings semanticos, anti-unificacao e avaliacao FAME

---

## Criacao Original

**Autor:** Guilherme Goncalves Machado
**ORCID:** 0009-0008-1083-0784
**Contato:** guilhermemachado@hubstry.onmicrosoft.com
**Site:** www.hubstry.dev

Este framework e criacao intelectual original de Guilherme Goncalves Machado,
resultado de pesquisa independente sobre a estilistica barroca de Vieira e sua
transposicao para formalizacao algoritmica computacional. A influencia teorica
de Jamil Almansur Haddad (Vieira e o Barroco Brasileiro, Companhia Editora
Nacional, Sao Paulo, 1957) e reconhecida como fundamento estrutural, mas a
arquitetura algoritmica, a ontologia semiomorfologica e o sistema de extracao
de analogias sao criacao original do autor.

O framework e a transposicao computacional do **Algoritmo PANVIEIRA**
(preprint Zenodo, 2026), que formaliza a estrutura de paralelismo
nao-progressivo vieiriano como padrao agnostico instanciavel em qualquer
sistema semiotico.

---

## O que e

Este projeto formaliza algoritmicamente a estilistica barroca de Vieira --
especificamente o processo de **reiteracao enfatica**, a **reducao de N termos
a 1 generico** e o **paralelismo sintatico** -- como um sistema computacional
de descoberta de analogias entre dominios naturais.

Baseado no Algoritmo PANVIEIRA, o framework opera com quatro operacoes
fundamentais: **ABSTRACT, EXPAND, SERIALIZE, CONTRACT**, com propriedade de
circularidade iterativa.

| Dominio | Escopo | Extrator | Exemplos |
|---------|--------|----------|----------|
| **Mineral** | Pedras, minerios, terras raras | `ExtratorMineral` | Materiais avancados, eletronica |
| **Vegetal** | Plantas, florestas, fitoquimica | `ExtratorVegetal` | Agronegocio, farmacologia |
| **Animal** | Fauna, sistemas zoologicos | `ExtratorAnimal` | Robotica biomimetica |
| **Humano** | Fisiologia, linguas naturais | `ExtratorHumano` | IA explicavel, medicina de precisao |

Cada dominio implementa **3 tipos de analogia**:

- **Heuristica** -- emergencias nao-lineares e convergencias nao-obvias
- **Funcional** -- mesma funcao em estrutura diferente
- **Homologica** -- mesma origem/evolucao, funcao pode divergir

---

## Novidades na v2.0.0

### Metricas de Similaridade Reais (Tarefa 1.1)

**8 algoritmos** substituindo stubs aleatorios:

- **Cosseno** -- Angular, vetores de propriedades
- **Jaccard** -- Conjuntista, descritores e dominios
- **Pearson** -- Correlacao, alinhamento linear
- **Spearman** -- Correlacao (rank), relacoes monotonicas
- **Euclidiana** -- Distancia, proximidade espacial
- **Manhattan** -- Distancia, robusta a outliers
- **Sobreposicao de Descritores** -- Hibrida, descritores semanticos
- **Distancia Combinada** -- Ponderada, score composto (0-1)

### Motor Semantico com Embeddings (Tarefa 1.2)

**Fallback de 3 niveis** -- funciona ate em 8GB RAM:

1. **Nivel 3:** Sentence-Transformers (sentence-transformers + PyTorch)
2. **Nivel 2:** TF-IDF (scikit-learn)
3. **Nivel 1:** Hash fingerprint + SequenceMatcher (stdlib)

### Anti-Unificacao HDTP (Tarefa 1.3)

Operacao **CONTRACT** do PANVIEIRA como anti-unificacao:
extrai o generico G entre dois morfemas, identifica especificos
e calcula grau de similaridade.

### Avaliacao FAME (Tarefa 1.4)

**6 dimensoes** com media harmonica: Analogia, Significancia,
Novidade, Solidez, Utilidade, Informatividade.

---

## Uso Rapido

    from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico
    from semiomorfologia.core.ontologia import DominioNatural, NivelOrganizacao, Morfema
    from semiomorfologia.similaridade.anti_unificacao import AntiUnificador
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    motor = MotorSemiomorfologico()
    grafeno = Morfema("grafeno", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
        descritores={"elemento_base": "carbono"}, propriedades={"condutividade": 0.98})
    resultados = motor.extrair_analogias_dominio([grafeno, ...], DominioNatural.MINERAL)
    au = AntiUnificador()
    contrato = au.contrato(m1_dict, m2_dict)
    avaliador = AvaliadorFAME()
    fame = avaliador.avaliar_contrato(contrato)

## Instalacao

    pip install -r requirements-lite.txt   # Leve (8GB RAM)
    pip install -e ".[embeddings]"         # Completa (com embeddings)
    python -m pytest tests/ -v             # 42 passed

---

## Estrutura do Repositorio

    src/semiomorfologia/
      core/ontologia.py           # Morfema, Sintagma, Analogia
      extratores/                 # 4 extratores (mineral, vegetal, animal, humano)
      motor/semiomorfologico.py   # Orquestrador PANVIEIRA
      similaridade/               # [v2.0] 8 metricas + Motor Semantico + Anti-Unificacao
      avaliacao/fame.py           # [v2.0] FAME: 6 dimensoes
    tests/                        # 42 testes (pytest)
    requirements-lite.txt         # Sem torch

## Citacao

> MACHADO, G. G. **Algoritmo PANVIEIRA: Formalizacao algoritmica do
> paralelismo nao-progressivo vieiriano.** 2026. Preprint Zenodo.
> **ORCID:** 0009-0008-1083-0784

## Licenca

**Licenca Semiomorfologica Vieiriana v1.0** -- Uso academico livre.
**Uso comercial requer autorizacao previa do autor.**
Contato: guilhermemachado@hubstry.onmicrosoft.com | www.hubstry.dev

---

**Desenvolvido por Guilherme Goncalves Machado | Hubstry Deep Tech (c) 2026**