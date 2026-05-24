# Semiomorfologia Vieiriana

> Framework agnóstico de extração de analogias nas 4 morfologias naturais
> Transposição computacional do Algoritmo PANVIEIRA
>
> **v3.0.0** — TAP-PAN, CSI, Diálogo com Algoritmos, Grafos Bipartidos e Extensão Quântica

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/) [![License](https://img.shields.io/badge/License-Semiomorfologica_Vieiriana-green.svg)](LICENSE) [![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20367826-blue.svg)](https://doi.org/10.5281/zenodo.20367826) [![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)](https://github.com/guilherme-machado-ceo/semiomorfologia-vieiriana) [![Tests 95](https://img.shields.io/badge/tests-95%20passed-success.svg)](tests/)

---

## Criação Original

**Autor:** Guilherme Gonçalves Machado
**ORCID:** 0009-0008-1083-0784
**Contato:** guilhermemachado@hubstry.onmicrosoft.com
**Site:** www.hubstry.dev

Este framework é criação intelectual original de Guilherme Gonçalves Machado,
resultado de pesquisa independente sobre a estilística barroca de Vieira e sua
transposição para formalização algorítmica computacional. A influência teórica
de Jamil Almansur Haddad (*Vieira e o Barroco Brasileiro*, Companhia Editora
Nacional, São Paulo, 1957) é reconhecida como fundamento estrutural, mas a
arquitetura algorítmica, a ontologia semiomorfologica e o sistema de extração
de analogias são criação original do autor.

O framework é a transposição computacional do **Algoritmo PANVIEIRA**
(preprint Zenodo, 2026 — [DOI: 10.5281/zenodo.20367826](https://doi.org/10.5281/zenodo.20367826)),
que formaliza a estrutura de paralelismo não-progressivo vieiriano como
padrão agnóstico instanciável em qualquer sistema semiótico.

---

## O que é

Este projeto formaliza algoritmicamente a estilística barroca de Vieira —
especificamente o processo de **reiteração enfática**, a **redução de N termos
a 1 genérico** e o **paralelismo sintático** — como um sistema computacional
de descoberta de analogias entre domínios naturais.

Baseado no Algoritmo PANVIEIRA, o framework opera com quatro operações
fundamentais: **ABSTRACT, EXPAND, SERIALIZE, CONTRACT**, com propriedade de
circularidade iterativa.

| Domínio | Escopo | Extrator | Exemplos |
|---------|--------|----------|----------|
| **Mineral** | Pedras, minérios, terras raras | `ExtratorMineral` | Materiais avançados, eletrônica |
| **Vegetal** | Plantas, florestas, fitoquímica | `ExtratorVegetal` | Agronegócio, farmacologia |
| **Animal** | Fauna, sistemas zoológicos | `ExtratorAnimal` | Robótica biomimética |
| **Humano** | Fisiologia, línguas naturais | `ExtratorHumano` | IA explicável, medicina de precisão |

Cada domínio implementa **3 tipos de analogia**:

- **Heurística** — emergências não-lineares e convergências não-óbvias
- **Funcional** — mesma função em estrutura diferente
- **Homológica** — mesma origem/evolução, função pode divergir

---

## Novidades na v2.0.0

### Métricas de Similaridade Reais (Tarefa 1.1)

**8 algoritmos** substituindo stubs aleatórios:

- **Cosseno** — Angular, vetores de propriedades
- **Jaccard** — Conjuntista, descritores e domínios
- **Pearson** — Correlação, alinhamento linear
- **Spearman** — Correlação (rank), relações monotônicas
- **Euclidiana** — Distância, proximidade espacial
- **Manhattan** — Distância, robusta a outliers
- **Sobreposição de Descritores** — Híbrida, descritores semânticos
- **Distância Combinada** — Ponderada, score composto (0-1)

### Motor Semântico com Embeddings (Tarefa 1.2)

**Fallback de 3 níveis** — funciona até em 8GB de RAM:

1. **Nível 3:** Sentence-Transformers (sentence-transformers + PyTorch)
2. **Nível 2:** TF-IDF (scikit-learn)
3. **Nível 1:** Hash fingerprint + SequenceMatcher (stdlib)

### Anti-Unificação HDTP (Tarefa 1.3)

Operação **CONTRACT** do PANVIEIRA como anti-unificação:
extrai o genérico G entre dois morfemas, identifica específicos
e calcula grau de similaridade.

### Avaliação FAME (Tarefa 1.4)

**6 dimensões** com média harmônica: Analogia, Significância,
Novidade, Solidez, Utilidade, Informatividade.

### Teste de Aderência ao Padrão (TAP-PAN)

Procedimento estatístico em 4 etapas que verifica se um sistema semiótico
realmente adere ao padrão PANVIEIRA: invariância de G (cosseno em
embeddings), independência entre {Sᵢ} e {Cᵢ} (qui-quadrado), validação
cruzada por exclusão (leave-one-out), e benchmark contra modelos nulos
(AIC/BIC).

### Coerência Semântica Interna (CSI)

Métrica que distingue padrões semióticos genuínos de coincidências
formais. CSI(G, {Sᵢ}, {Cᵢ}) = (1/n) * somatório de sim(φ(eᵢ), ē_φ),
onde φ é uma função de embebição semântico e ē_φ é o centróide semântico.
O limiar τ é determinado empiricamente via distribuição nula (bootstrap).

### Horizonte Hermenêutico P

Restrições contextuais formais como parâmetro do algoritmo,
respeitando a decisão gadameriana de que todo entendimento ocorre dentro
de um horizonte histórico. Cada ρ_j ∈ P é testada como restrição lógica
sobre G, Sᵢ, Cᵢ e ⊗.

### Diálogo com Algoritmos Clássicos

- **MapReduce**: EXPAND ≈ Map, CONTRACT ≈ Reduce
- **Hylomorphism**: PANVIEIRA como composição unfold + fold
- **Grafos Bipartidos**: EXPAND via arestas semânticas (escalabilidade)
- **K-Means**: ABSTRACT via clustering de embeddings
- **Unificação de Robinson**: CONTRACT como unificação lógica

### Visualização por Grafo Bipartido

EXPAND opera sobre arestas de um grafo bipartido Sᵢ-Cᵢ (não produto
cartesiano), evitando explosão combinatória semântica. Integrado com
NetworkX + pyvis para visualização interativa.

### H-PANVIEIRA (Quântico Híbrido)

Protótipo experimental com qiskit: orquestração clássica + kernel
quântico (EXPAND no QPU via superposição, Grover para busca de loci,
VQE para ABSTRACT). Requer instalação separada: `pip install -e ".[quantum]"`

---

## Uso Rápido

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

## Instalação

    pip install -r requirements-lite.txt   # Leve (8GB de RAM)
    pip install -e ".[embeddings]"         # Com embeddings semânticos
    pip install -e ".[all]"                # Completa (embeddings + quantum)
    pip install -e ".[quantum]"            # Módulo quântico experimental
    python -m pytest tests/ -v             # 77+ passed

---

## Estrutura do Repositório

    src/semiomorfologia/
      core/ontologia.py             # Morfema, Sintagma, Analogia
      extratores/                   # 4 extratores (mineral, vegetal, animal, humano)
      motor/
        semiomorfologico.py         # Orquestrador PANVIEIRA
        hylomorphism.py             # [v3.0] Hylomorphism (unfold/fold)
        mapreduce_engine.py         # [v3.0] EXPAND/CONTRACT paralelizados
        abstract_kmeans.py          # [v3.0] ABSTRACT via clustering
      similaridade/
        metricas.py                 # [v2.0] 8 métricas de similaridade
        semantica.py                # [v2.0] Motor Semântico (3 níveis)
        anti_unificacao.py          # [v2.0] HDTP anti-unificação
        tap_pan.py                  # [v3.0] TAP-PAN (4 etapas)
        csi.py                      # [v3.0] CSI com limiar τ
      avaliacao/fame.py             # [v2.0] FAME: 6 dimensões
      visualizacao/
        grafo_bipartido.py          # [v3.0] EXPAND via grafo bipartido (NetworkX + pyvis)
      quantum/                       # [v3.0] Módulo quântico experimental
        hpanvieira.py               # Orquestrador híbrido
        qexpand.py                  # EXPAND quântico (superposição)
        qcontract.py                # CONTRACT quântico (interferência)
        grover_locus.py              # Grover search para loci
    tests/                          # 59+ testes (pytest)
    docs/TEORIA.md                  # Fundamentação teórica completa
    requirements-lite.txt           # Sem torch

## Citação

> MACHADO, G. G. **PANVIEIRA: Um Algoritmo Agnóstico para Instanciação de
> Série e Paralelo como Estrutura Semiótica Universal — Da Retórica
> Vieiriana à Computação.** 2026. Zenodo.
> **DOI:** [10.5281/zenodo.20367826](https://doi.org/10.5281/zenodo.20367826)
> **ORCID:** 0009-0008-1083-0784

## Referência Acadêmica

A fundamentação teórica completa do framework, incluindo 5 definições
formais, 8 proposições (TAP-PAN, CSI, MDL), diálogo com algoritmos
clássicos e roteiro de extensões quânticas, está documentada em
`docs/TEORIA.md` e no [preprint no Zenodo](https://zenodo.org/records/20367826).

## Licença

**Licença Semiomorfológica Vieiriana v1.0** — Uso acadêmico livre.
**Uso comercial requer autorização prévia do autor.**
Contato: guilhermemachado@hubstry.onmicrosoft.com | www.hubstry.dev

---

**Desenvolvido por Guilherme Gonçalves Machado | Hubstry Deep Tech © 2026**