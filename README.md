# Semiomorfologia Vieiriana

> Framework agnóstico de extração de analogias nas 4 morfologias naturais
> Transposição computacional do Algoritmo PANVIEIRA
>
> **v2.0.0** — Métricas reais, embeddings semânticos, anti-unificação e avaliação FAME

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
(preprint Zenodo, 2026), que formaliza a estrutura de paralelismo
não-progressivo vieiriano como padrão agnóstico instanciável em qualquer
sistema semiótico.

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
    pip install -e ".[embeddings]"         # Completa (com embeddings)
    python -m pytest tests/ -v             # 42 passed

---

## Estrutura do Repositório

    src/semiomorfologia/
      core/ontologia.py           # Morfema, Sintagma, Analogia
      extratores/                 # 4 extratores (mineral, vegetal, animal, humano)
      motor/semiomorfologico.py   # Orquestrador PANVIEIRA
      similaridade/               # [v2.0] 8 métricas + Motor Semântico + Anti-Unificação
      avaliacao/fame.py           # [v2.0] FAME: 6 dimensões
    tests/                        # 42 testes (pytest)
    requirements-lite.txt         # Sem torch

## Citação

> MACHADO, G. G. **Algoritmo PANVIEIRA: Formalização algorítmica do
> paralelismo não-progressivo vieiriano.** 2026. Preprint Zenodo.
> **ORCID:** 0009-0008-1083-0784

## Licença

**Licença Semiomorfológica Vieiriana v1.0** — Uso acadêmico livre.
**Uso comercial requer autorização prévia do autor.**
Contato: guilhermemachado@hubstry.onmicrosoft.com | www.hubstry.dev

---

**Desenvolvido por Guilherme Gonçalves Machado | Hubstry Deep Tech © 2026**