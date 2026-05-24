# Semiomorfologia Vieiriana

> Framework agnóstico de extração de analogias nas 4 morfologias naturais
> Transposição computacional do Algoritmo PANVIEIRA
>
> **v3.1.0** — TAP-PAN, CSI, Diálogo com Algoritmos, Grafos Bipartidos, Extensão Quântica e Extratores com Dados Reais

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/) [![License](https://img.shields.io/badge/License-Semiomorfologica_Vieiriana-green.svg)](LICENSE) [![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20367826-blue.svg)](https://doi.org/10.5281/zenodo.20367826) [![Version](https://img.shields.io/badge/version-3.1.0-orange.svg)](https://github.com/guilherme-machado-ceo/semiomorfologia-vieiriana) [![Tests 95](https://img.shields.io/badge/tests-95%20passed-success.svg)](tests/)

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

---

## Novidades na v3.0.0

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

## Novidades na v3.1.0

### Extratores com Dados Reais

Os 4 extratores (Mineral, Vegetal, Animal, Humano) agora operam com dados
determinísticos reais de APIs científicas, substituindo os stubs aleatórios
(`np.random.uniform`) da v2.0. Cada extrator consulta bases de conhecimento
reais com fallback gracefully degradado:

| Extrator | Fonte Primária | Fallback |
|----------|---------------|----------|
| `ExtratorMineral` | PubChem CID | Propriedades cristalográficas determinísticas |
| `ExtratorVegetal` | GBIF (Occurrence API) | Dados da World Flora Online (WFO) |
| `ExtratorAnimal` | GBIF (Species API) | Dados morfológicos canônicos |
| `ExtratorHumano` | Wikidata (SPARQL) | Dados biológicos de referência |

O design é **offline-first**: quando não há conexão com a API, cada extrator
usa um catálogo embutido de propriedades reais, garantindo resultados
determinísticos e reproduzíveis em qualquer ambiente.

---

## Manual de Implantação para Equipes Não-Especialistas

Este manual destina-se a pesquisadores, analistas e profissionais que precisam
instalar e executar o framework sem conhecimento prévio de Python avançado,
CI/CD ou infraestrutura de software. Siga os passos na ordem apresentada.

### 1. Pré-requisitos

Antes de começar, verifique se você tem os seguintes itens instalados:

| Item | Versão Mínima | Como Verificar | Link de Download |
|------|--------------|----------------|-----------------|
| **Python** | 3.8+ | `python --version` | [python.org/downloads](https://www.python.org/downloads/) |
| **pip** | 21.0+ | `pip --version` | Incluído no Python 3.8+ |
| **Git** | 2.30+ | `git --version` | [git-scm.com](https://git-scm.com/) |

**Nota para Windows:** Durante a instalação do Python, marque a opção
*"Add Python to PATH"*. Caso contrário, os comandos `python` e `pip` não
serão reconhecidos no terminal. Se isso acontecer, reinstale o Python com
essa opção marcada.

**Nota para macOS:** O Python vindo com o sistema (Apple Python) é
incompatível. Instale via Homebrew (`brew install python`) ou pelo site oficial.

### 2. Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|-----------|--------|-------------|
| **RAM** | 4 GB | 8 GB |
| **Disco** | 500 MB livres | 2 GB livres |
| **CPU** | Qualquer processador moderno | Multicore (para paralelismo) |
| **Internet** | Não obrigatória | Necessária para APIs (PubChem, GBIF, Wikidata) |

> O framework funciona completamente **offline** no modo leve. A conexão com
> internet é necessária apenas para consultar dados reais das APIs científicas
> (PubChem, GBIF, Wikidata). Sem internet, os extratores usam catálogos
> embutidos automaticamente.

### 3. Instalação Passo a Passo

#### 3.1 Clonar o Repositório

Abra o terminal (PowerShell no Windows, Terminal no macOS/Linux) e execute:

    git clone https://github.com/guilherme-machado-ceo/semiomorfologia-vieiriana.git
    cd semiomorfologia-vieiriana

#### 3.2 Criar e Ativar Ambiente Virtual

O ambiente virtual isola as dependências do projeto do resto do sistema,
evitando conflitos entre versões de bibliotecas.

**Windows (PowerShell):**

    python -m venv venv
    .\venv\Scripts\Activate.ps1

**macOS/Linux:**

    python3 -m venv venv
    source venv/bin/activate

> Após ativar, você verá `(venv)` no início da linha do terminal. Isso indica
> que o ambiente virtual está ativo. Se fechar o terminal, será necessário
> ativar novamente com o comando acima.

#### 3.3 Instalar o Framework

Existem **4 modos de instalação**, do mais leve ao mais completo.
Escolha apenas um:

**Modo Leve (recomendado para começar — funciona offline):**

    pip install -e .

Isso instala apenas as dependências essenciais: numpy, scipy, scikit-learn.
Ocupa ~50 MB de disco e funciona em 4 GB de RAM. Inclui todos os 95 testes,
os 4 extratores com catálogos embutidos, TAP-PAN, CSI, Hylomorphism, MapReduce,
KMeans, Grafos Bipartidos e Anti-Unificação.

**Modo com Embeddings Semânticos (requer ~8 GB de RAM):**

    pip install -e ".[embeddings]"

Adiciona sentence-transformers e PyTorch para embeddings densos.
Recomendado se você planeja processar textos longos ou precisa de alta
precisão na detecção de similaridade semântica.

**Modo com APIs Científicas (requer internet):**

    pip install -e ".[api]"

Adiciona suporte a FastAPI (servidor HTTP), SPARQLWrapper (Wikidata),
requests (PubChem, GBIF) e NetworkX/pyvis (visualização). Ideal para
produção ou integração com sistemas externos.

**Modo Completo (todos os recursos):**

    pip install -e ".[all]"

Instala todas as dependências opcionais, incluindo embeddings, APIs e
visualização interativa.

**Modo Quântico Experimental (opcional, avançado):**

    pip install -e ".[quantum]"

Adiciona qiskit para protótipos de computação quântica. Requer ~2 GB
adicionais de disco. Funciona apenas em fallback clássico se qiskit
não estiver disponível.

#### 3.4 Verificar Instalação

Execute os testes para confirmar que tudo está funcionando:

    python -m pytest tests/ -v

Você deve ver `95 passed` (ou mais). Qualquer falha indica um problema
de instalação — consulte a seção [Solução de Problemas](#8-solução-de-problemas)
abaixo.

### 4. Primeiro Exemplo Prático (5 minutos)

Crie um arquivo chamado `meu_primeiro_teste.py` e cole o seguinte código:

```python
from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico
from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao

# 1. Iniciar o motor
motor = MotorSemiomorfologico()

# 2. Criar morfemas do corpus mineral
grafeno = Morfema(
    "grafeno", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
    descritores={"elemento_base": "carbono", "funcao": "condutividade"},
    propriedades={"condutividade": 0.98, "flexibilidade": 0.95}
)
diamante = Morfema(
    "diamante", DominioNatural.MINERAL, NivelOrganizacao.MOLECULAR,
    descritores={"elemento_base": "carbono", "funcao": "dureza"},
    propriedades={"dureza": 1.0, "brilho": 0.99}
)

# 3. Extrair analogias
corpus = [grafeno, diamante]
resultados = motor.extrair_analogias_dominio(corpus, DominioNatural.MINERAL)

# 4. Ver resultados
for tipo, analogias in resultados.items():
    for a in analogias:
        print(f"{a.fonte.id} -> {a.alvo.id} | {tipo.value} | forca={a.forca:.3f}")
        if a.aplicacao_industrial:
            print(f"  Aplicacao: {a.aplicacao_industrial}")
```

Execute com:

    python meu_primeiro_teste.py

**Saída esperada:**

```
grafeno -> diamante | homologica | forca=0.500
  Aplicacao: Engenharia de allotropos: otimização de carbono
```

> O output pode variar ligeiramente dependendo da versão. O importante é
> que o programa execute sem erros e produza ao menos uma analogia.

### 5. Exemplo Completo com TAP-PAN

Para verificar se um texto segue o padrão PANVIEIRA (paralelismo vieiriano):

```python
from semiomorfologia.similaridade.tap_pan import TAPPAN

tap = TAPPAN()

instancias = [
    "a natureza insensivel o perseguiu nas pedras",
    "a natureza vegetativa o perseguiu nos espinhos",
    "a natureza sensitiva o perseguiu nas aves",
    "a natureza racional o perseguiu nos homens",
]
S = ["insensivel", "vegetativa", "sensitiva", "racional"]
C = ["pedras", "espinhos", "aves", "homens"]

resultado = tap.executar(instancias, S, C)

print(f"Aderencia ao PANVIEIRA: {resultado.aderencia}")
print(f"Variancia de G: {resultado.etapa1_variancia_G:.4f}")
print(f"Chi-quadrado (independencia): {resultado.etapa2_chi2:.4f}")
print(f"AIC modelo PAN: {resultado.etapa4_aic_pan:.2f}")
```

### 6. Usando os Extratores com Dados Reais

Os extratores consultam APIs científicas automaticamente quando há internet.
Sem internet, usam catálogos embutidos:

```python
from semiomorfologia.extratores import ExtratorMineral, ExtratorVegetal
from semiomorfologia.core.ontologia import Morfema, DominioNatural, NivelOrganizacao

# Mineral com dados reais do PubChem
extrator_min = ExtratorMineral()
m1 = Morfema("ferro", DominioNatural.MINERAL, NivelOrganizacao.ATOMICO,
             descritores={"elemento_base": "ferro", "funcao": "condutividade"},
             propriedades={"condutividade": 0.17, "dureza": 0.40})
m2 = Morfema("cobre", DominioNatural.MINERAL, NivelOrganizacao.ATOMICO,
             descritores={"elemento_base": "cobre", "funcao": "condutividade"},
             propriedades={"condutividade": 0.59, "dureza": 0.30})

resultados_min = extrator_min.processar([m1, m2])
for tipo, analogias in resultados_min.items():
    for a in analogias:
        print(f"[MINERAL] {a}")

# Vegetal com dados reais do GBIF
extrator_veg = ExtratorVegetal()
v1 = Morfema("eucalipto", DominioNatural.VEGETAL, NivelOrganizacao.ORGANICO,
             descritores={"ambiente": "tropical", "processo": "fotossintese", "familia": "Myrtaceae"},
             propriedades={"crescimento": 0.90, "resistencia_seca": 0.70})

resultados_veg = extrator_veg.processar([v1])
print(f"[VEGETAL] {len(resultados_veg)} tipos de analogia processados")
```

### 7. Glossário Rápido

| Termo | Explicação Simples |
|-------|-------------------|
| **Morfema** | Unidade básica de análise (ex: "grafeno", "cacto", "tardigrado") |
| **Sintagma** | Conjunto de morfemas organizados em paralelo |
| **Analogia** | Relação descoberta entre dois morfemas |
| **ABSTRACT** | Operação que reduz N termos a 1 genérico |
| **EXPAND** | Operação que gera N instâncias a partir de 1 genérico |
| **CONTRACT** | Operação que encontra o que há de comum entre duas coisas |
| **SERIALIZE** | Operação que formaliza a analogia encontrada |
| **PANVIEIRA** | O algoritmo central: ABSTRACT + EXPAND + SERIALIZE + CONTRACT |
| **TAP-PAN** | Teste que verifica se um texto segue o padrão PANVIEIRA |
| **CSI** | Métrica de coerência semântica interna |
| **FAME** | Avaliação de qualidade de uma analogia (6 dimensões) |
| **Corpus** | Conjunto de morfemas de entrada para análise |
| **Dominio** | Um dos 4 reinos da natureza: mineral, vegetal, animal, humano |
| **Heurística** | Analogia por emergência não-linear (descoberta surpreendente) |
| **Funcional** | Analogia por mesma função em estrutura diferente |
| **Homológica** | Analogia por mesma origem/evolução |

### 8. Solução de Problemas

**Problema: `python` não é reconhecido (Windows)**

O Python não está no PATH. Solução:

    # Opção 1: Reinstalar Python marcando "Add to PATH"
    # Opção 2: Usar o launcher py
    py -m venv venv
    .\venv\Scripts\Activate.ps1

**Problema: `Activate.ps1` não pode ser carregado (política de execução)**

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Se o PowerShell pedir confirmação, digite `S` e pressione Enter.

**Problema: `pip install` falha com erro de compilação (C++/Rust)**

Isso ocorre no modo `embeddings` (PyTorch) em máquinas sem compilador.
Solução: use o modo leve que não precisa de compilação:

    pip install -e .

**Problema: Testes falham com `ModuleNotFoundError`**

O pacote não foi instalado corretamente. Execute:

    pip install -e .
    python -m pytest tests/ -v

**Problema: Erro de conexão ao consultar APIs (PubChem, GBIF)**

Os extratores funcionam **offline** com catálogos embutidos. Se quiser
dados online, verifique sua conexão com a internet. As APIs usadas são:

- PubChem: `https://pubchem.ncbi.nlm.nih.gov/` (sem autenticação)
- GBIF: `https://api.gbif.org/` (sem autenticação)
- Wikidata: `https://query.wikidata.org/sparql` (sem autenticação)

Nenhuma exige chave de API ou cadastro.

**Problema: `UnicodeEncodeError` no Windows**

    # Adicione ao topo do seu script Python:
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

**Problema: Memória insuficiente (OOM)**

Se estiver no modo embeddings (sentence-transformers), o modelo ocupa ~500 MB
de RAM. Solução: use o modo leve (`pip install -e .`) que roda em 4 GB.

### 9. Organização da Equipe Recomendada

Para equipes que desejam utilizar o framework em projetos de pesquisa:

| Papel | Responsabilidade | Conhecimento Necessário |
|-------|-----------------|------------------------|
| **Pesquisador Principal** | Define corpus, interpreta analogias | Conhecimento do domínio científico |
| **Analista de Dados** | Prepara dados, executa extrações | Python básico (este manual basta) |
| **Engenheiro de Software** | Integra o framework em sistemas | Python intermediário + APIs |

### 10. Fluxo de Trabalho Típico

```
1. Definir pergunta de pesquisa
   "Quais analogias existem entre minerais condutores?"

2. Preparar corpus de morfemas
   Morfema("ferro", ..., propriedades={...})
   Morfema("cobre", ..., propriedades={...})
   Morfema("aluminio", ..., propriedades={...})

3. Executar extração
   motor.extrair_analogias_dominio(corpus, DominioNatural.MINERAL)

4. Avaliar qualidade
   AvaliadorFAME().avaliar_contrato(contrato)

5. Verificar aderência ao padrão
   TAPPAN().executar(instancias, S, C)

6. Interpretar resultados e gerar conhecimento aplicado
   motor.gerar_conhecimento_aplicado(analogias)
```

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
    python -m pytest tests/ -v             # 95+ passed

---

## Estrutura do Repositório

    src/semiomorfologia/
      core/ontologia.py             # Morfema, Sintagma, Analogia
      extratores/                   # 4 extratores com dados reais (mineral, vegetal, animal, humano)
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
    tests/                          # 95 testes (pytest)
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
