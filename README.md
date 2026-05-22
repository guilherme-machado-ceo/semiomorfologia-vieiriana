# Semiomorfologia Vieiriana

> Framework agnóstico de extração de analogias nas 4 morfologias naturais  
> Transposição computacional do Algoritmo PANVIEIRA

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
arquitetura algorítmica, a ontologia semiomorfológica e o sistema de extração
de analogias são criação original do autor.

O framework é a transposição computacional do **Algoritmo PANVIEIRA**
(preprint Zenodo, 2026), que formaliza a estrutura de paralelismo
não-progressivo vieiriano como padrão agnóstico instanciável em qualquer
sistema semiótico.

---

## Hubstry Deep Tech

Este projeto é desenvolvido e mantido pela **Hubstry Deep Tech**, um *operating
deep tech venture builder* focado em pesquisa, desenvolvimento e criação de
ativos tecnológicos proprietários.

Nosso modelo atua prioritariamente em **B2B** e **B2G**, permitindo que empresas
e instituições acessem e co-desenvolvam tecnologias avançadas com maior eficiência
de capital e soberania tecnológica, reduzindo custo, tempo e risco de inovação.

Estruturamos e escalamos soluções em áreas estratégicas, criando barreiras de
entrada relevantes e capturando valor antecipado em ciclos tecnológicos emergentes.
Adicionalmente, operamos modelos **B2B2C**, ampliando a distribuição e captura
de valor das tecnologias desenvolvidas.

No horizonte estratégico, acompanhamos a crescente atomização do consumo
impulsionada por IA, que tende a transformar indivíduos em operadores
tecnológicos independentes. Esse movimento orienta nossa capacidade de
antecipar novos modelos de mercado e posicionar ativos para capturar valor
também em contextos **B2C** emergentes.

Em síntese, a **Hubstry** transforma incerteza tecnológica em vantagem
competitiva estruturada e de longo prazo.

---

## O que é

Este projeto formaliza algoritmicamente a estilística barroca de Vieira —
especificamente o processo de **reiteração enfática**, a **redução de N termos
a 1 genérico** e o **paralelismo sintático** — como um sistema computacional
de descoberta de analogias entre domínios naturais.

Baseado no Algoritmo PANVIEIRA (⟨G, {Sᵢ}, {Cᵢ}, ⊗, π, ρ⟩), o framework opera
com quatro operações fundamentais: **ABSTRACT, EXPAND, SERIALIZE, CONTRACT**,
com propriedade de circularidade iterativa (G → EXPAND → CONTRACT → G).

| Domínio | Escopo | Extrator |
|---------|--------|----------|
| **Mineral** | Pedras, minérios, terras raras | `ExtratorMineral` |
| **Vegetal** | Plantas, florestas, fitoquímica | `ExtratorVegetal` |
| **Animal** | Fauna, sistemas zoológicos | `ExtratorAnimal` |
| **Humano** | Fisiologia, biologia, línguas naturais | `ExtratorHumano` |

Cada domínio implementa **3 tipos de analogia**:
- **Heurística** — descoberta de emergências não-lineares
- **Funcional** — mesma função, estrutura diferente
- **Homológica** — mesma origem, função pode divergir

---

## Uso Rápido

```python
from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico
from semiomorfologia.core.ontologia import DominioNatural, NivelOrganizacao, Morfema

# Criar motor
motor = MotorSemiomorfologico()

# Definir morfemas (unidades de análise)
grafeno = Morfema(
    id="grafeno",
    dominio=DominioNatural.MINERAL,
    nivel=NivelOrganizacao.MOLECULAR,
    descritores={"elemento_base": "carbono", "funcao": "condutividade"},
    propriedades={"condutividade": 0.98, "flexibilidade": 0.95}
)

# ... adicionar mais morfemas e processar
resultados = motor.extrair_analogias_dominio([grafeno, ...], DominioNatural.MINERAL)
```

Veja `examples/` para demonstrações completas e `docs/TEORIA.md` para a
fundamentação teórica (Vieira, Haddad, PANVIEIRA).

---

## Estrutura do Repositório

```
semiomorfologia-vieiriana/
├── src/semiomorfologia/      # Código-fonte principal
│   ├── core/                 # Ontologia: Morfema, Sintagma, Analogia
│   ├── extratores/           # 4 extratores especializados
│   ├── motor/                # Orquestrador vieiriano
│   └── aplicacao/            # Camada industrial (TRL, mercado)
├── tests/                    # Testes unitários (pytest)
├── examples/                 # Demonstrações executáveis
├── scripts/                  # Scripts PowerShell/Shell
├── docs/                     # Documentação teórica
└── output/                   # Resultados gerados (gitignored)
```

---

## Arquitetura

```
┌─────────────────────────────────────────────┐
│  1. FUNDAÇÃO TEÓRICA (Vieira/Haddad/PANVIEIRA)│
├─────────────────────────────────────────────┤
│  2. ONTOLOGIA (4 Domínios × 3 Analogias)    │
├─────────────────────────────────────────────┤
│  3. COMPOSIÇÃO → Redução N termos → 1 genérico │
│  4. REITERAÇÃO → Enfática circular/paralela │
│  5. EXTRAÇÃO → 3 algoritmos por domínio     │
│  6. PONTES → Cruzadas inter-domínios        │
├─────────────────────────────────────────────┤
│  7. APLICAÇÃO → TRL, Mercado, Setores       │
└─────────────────────────────────────────────┘
```

---

## Licença

**Licença Semiomorfológica Vieiriana v1.0**

Copyright (c) 2026 Guilherme Gonçalves Machado

Este software é disponibilizado para uso acadêmico, educacional, de pesquisa e
não-comercial de forma livre e gratuita, desde que a atribuição de criação
original seja mantida.

**A exploração comercial deste software — incluindo venda direta, uso em produtos
ou serviços comerciais, licenciamento a terceiros ou incorporação em soluções
enterprise/governamentais pagas — REQUER AUTORIZAÇÃO PRÉVIA E ESCRITA do autor.**

Para solicitar autorização comercial, entre em contato:  
📧 guilhermemachado@hubstry.onmicrosoft.com  
🌐 www.hubstry.dev

Veja [LICENSE](LICENSE) para o texto completo.

---

**Desenvolvido por Guilherme Gonçalves Machado | Hubstry Deep Tech © 2026**  
**ORCID:** 0009-0008-1083-0784
