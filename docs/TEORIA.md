# Fundamentação Teórica

## Criação Original

Este framework é criação intelectual original de **Guilherme Gonçalves Machado**,
desenvolvido sob a égide da **Hubstry Deep Tech**.

Contato: guilhermemachado@hubstry.onmicrosoft.com
Site: www.hubstry.dev
ORCID: 0009-0008-1083-0784

---

## 1. Vieira e a Teoria dos Conjuntos Semelhantes

Baseado na análise de Jamil Almansur Haddad em *Vieira e o Barroco Brasileiro*
(Companhia Editora Nacional, São Paulo, 1957), particularmente nas páginas que
formalizam a estrutura de paralelismo não-progressivo dos sermões vieirianos.

A contribuição fundamental de Haddad consiste em demonstrar que o estilo
sermônico de Antônio Vieira obedece a um padrão composicional regular e
recorrente: a disposição de expressões em séries paralelas que convergem para
um mesmo conteúdo conceptual. Essa convergência não é acidental nem meramente
retórica — ela constitui o operador central da hermenêutica vieiriana, por
meio do qual o pregador simultaneamente argumenta, persuade e revela verdades
teológicas através da estruturação formal da linguagem. A Teoria dos Conjuntos
Semelhantes é, portanto, simultaneamente uma teoria do estilo e uma teoria do
pensamento: a forma do sermão é o conteúdo do sermão.

### 1.1 O Paralelismo Sintático

Vieira constrói períodos onde quatro (ou mais) expressões se dispõem em paralelo:

> "A natureza insensível o perseguiu nas pedras;
> a vegetativa, nos espinhos;
> a sensitiva, nas aves;
> a racional, nos homens" (Vieira, *Sermão da Sexagésima*)

Cada expressão possui:
- **Sujeito** diferente (insensível / vegetativa / sensitiva / racional)
- **Mesma estrutura sintática** ("a natureza X, nos Y")
- **Mesmo conteúdo conceptual** (a natureza persegue/age)

O paralelismo vieiriano não é, contudo, um paralelismo progressivo no sentido
clássico das progrymnasmata. Ao contrário do paralelismo progressivo — onde cada
expressão acrescenta informação nova ao argumento — o paralelismo não-progressivo
de Vieira opera por convergência: todas as expressões apontam para o mesmo
conteúdo conceptual, sondando-o por ângulos diferentes sem avançar linearmente.
Essa não-progressão é a marca distintiva do barroco sermonário e o fundamento
sobre o qual o algoritmo PANVIEIRA será posteriormente construído. O efeito
retórico é o de uma espiral hermenêutica: cada instância particular ilumina uma
faceta do genérico, e o genérico, por sua vez, confere unidade à multiplicidade
das instâncias.

### 1.2 A Redução ao Genérico

Haddad formaliza: as quatro expressões reduzem-se a uma só:

> **"a natureza [genérica] o perseguiu [em 4 modos]"**

A "primeira coluna de quatro termos pode reduzir-se a um só, genérico" (Haddad, 1957, p. 14-15).

Esta operação de redução é estruturalmente idêntica a uma operação de `fold`
ou `reduce` em programação funcional: dada uma coleção de elementos que partilham
uma estrutura comum, a operação de contração extrai o invariante que os unifica.
No caso vieiriano, esse invariante é o "conteúdo conceptual" que permanece
inalterado quando se abstraem as diferenças formais entre as instâncias. A
redução ao genérico é, assim, o complemento necessário da expansão paralela:
se a expansão multiplica o genérico em instâncias particulares, a contração
restitui a unidade subjacente. É esse movimento dialético entre expansão e
contração que constitui a circularidade iterativa do padrão PANVIEIRA.

### 1.3 A Reiteração Enfática

O processo de reiteração multiplica o mesmo conteúdo conceptual com variações formais.
Vieira não repete — **reitera enfaticamente**, criando:
- Circularidade do estilo
- Pressão da mais absoluta unidade
- Parada para refletir, ruminar, esgotar numa sondagem

Haddad denomina esta propriedade "tendência à circularidade do estilo" e o caracteriza
como "estilo de estase": aprofundamento do mesmo ponto por sondagem em múltiplas
direções específicas, com retorno ao centro. A reiteração não é redundância
vazia, mas um mecanismo de aprofundamento: cada retorno ao genérico carrega
consigo o acúmulo de compreensão obtido pelas instâncias particulares. Trata-se
de um processo de aproximação assintótica ao significado, onde cada ciclo
de expansão-contração refina a compreensão do invariante G. Essa propriedade
é fundamental para a aplicação computacional do padrão, pois garante que a
recursividade do algoritmo PANVIEIRA converge para um resultado estável em vez
de divergir ou oscilar indefinidamente.

---

## 2. Do PANVIEIRA à Semiomorfologia

O presente framework (**Semiomorfologia Vieiriana**) é a transposição computacional
do **Algoritmo PANVIEIRA**, formalizado pelo autor em preprint (Zenodo, Maio 2026).
A Semiomorfologia Vieiriana toma o padrão abstrato identificado por Haddad na
prosa sermonária e o transpõe para um sistema computacional capaz de detectar,
extrair, compor e validar instâncias desse padrão em domínios semióticos
diversos. O algoritmo PANVIEIRA funciona como o núcleo formal desse sistema,
definindo as operações primitivas e as propriedades invariantes que governam
a instanciação do padrão em qualquer sistema de signos.

### 2.1 O Algoritmo PANVIEIRA

O PANVIEIRA abstrai a estrutura vieiriana como padrão computacional agnóstico,
instanciável em qualquer sistema semiótico. É definido como tupla:

**PANVIEIRA = ⟨G, {Sᵢ}, {Cᵢ}, ⊗, π, ρ, 𝒫⟩**

Onde:
- **G** = termo genérico (invariante) — equivalente ao "conteúdo conceptual" de Haddad
- **{Sᵢ}** = conjunto de diferenciadores específicos — as variações formais
- **{Cᵢ}** = conjunto de loci de aplicação — os territórios/especificações
- **⊗** = operador de composição
- **π** = projeção de superfície (serialização)
- **ρ** = redução (contração ao genérico)
- **𝒫** = horizonte hermenêutico — conjunto de restrições semiótico-contextuais

O componente **𝒫** (horizonte hermenêutico) é um acréscimo formal que
especifica as condições de interpretação válidas para cada instância do padrão.
Sem esse componente, o algoritmo seria puramente sintático; com ele, o PANVIEIRA
adquire capacidade hermenêutica, pois cada domínio de aplicação pode definir
suas próprias restrições sobre como G, Sᵢ, Cᵢ e ⊗ devem ser interpretados.
Essa propriedade é essencial para que o framework possa operar em domínios
culturalmente distintos sem perder a coerência formal do padrão.

#### 2.1.1 Definições Formais

O algoritmo PANVIEIRA repousa sobre cinco definições primitivas que constituem
o vocabulário formal do sistema. Essas definições operam sobre um sistema
semiótico arbitrário Σ, garantindo a agnosticidade do algoritmo em relação
ao domínio de aplicação.

**Definição 1 — Termo Genérico G ∈ Σ**: Elemento de Σ que funciona como
abstração máxima de uma classe de expressões. G é o invariante estrutural do
padrão PANVIEIRA. Formalmente, para todo conjunto de expressões {e₁, e₂, ..., eₙ}
que seguem o padrão, existe um único G tal que `CONTRACT({eᵢ}) = G`. O termo
genérico é o "centro" da circularidade vieiriana: ele permanece idêntico a si
mesmo enquanto as instâncias particulares variam ao seu redor. Na prosa de
Vieira, G corresponde ao "conteúdo conceptual" identificado por Haddad; em
sistemas semióticos distintos, G pode assumir formas variadas — um tema musical,
um símbolo visual, uma classe de objetos — desde que funcione como invariante.

**Definição 2 — Diferenciador Sᵢ ∈ Σ**: Elemento que especifica G numa direção
particular. Cada Sᵢ introduz uma diferença que distingue uma instância das demais
sem alterar o invariante subjacente. A relação entre G e Sᵢ é análoga à relação
entre um paradigma e seus membros em linguística estrutural: Sᵢ preenche uma
posição variável numa estrutura fixa. No exemplo do Sermão da Sexagésima, os
diferenciadores são os qualificadores da natureza (insensível, vegetativa,
sensitiva, racional). A multiplicidade dos diferenciadores é o que confere riqueza
e profundidade ao padrão: quanto mais Sᵢ distintos, mais completo o mapeamento
do espaço de variação em torno de G.

**Definição 3 — Locus Cᵢ ∈ Σ**: Elemento que situa a instância num contexto ou
campo de aplicação particular. Enquanto Sᵢ especifica a direção da variação, Cᵢ
especifica o território em que a variação se manifesta. No sermão vieiriano, os
loci são os domínios concretos onde a ação da natureza se expressa: pedras,
espinhos, aves, homens. A distinção entre Sᵢ e Cᵢ é analítica — em muitos
casos, o diferenciador e o locus se fundem num único elemento composicional —
mas a separação formal é necessária para que o algoritmo possa operar sobre
sistemas onde a especificação direcional e a contextualização territorial são
operacionalmente distintas.

**Definição 4 — Operador de Composição ⊗**: Operação de concatenação, combinação
ou articulação no sistema semiótico Σ. O operador ⊗ é responsável por gerar cada
instância eᵢ a partir dos componentes do padrão: `eᵢ = Sᵢ ⊗ G ⊗ Cᵢ`. A
natureza de ⊗ depende do sistema semiótico em que o PANVIEIRA é instanciado:
em língua natural, ⊗ pode ser a concatenação sintagmática; em música, a
combinação melódica; em programação, a herança ou composição de objetos. A
generalidade de ⊗ é o que permite ao algoritmo ser verdadeiramente agnóstico.

**Definição 5 — Horizonte Hermenêutico 𝒫**: Conjunto de restrições
semiótico-contextuais 𝒫 = {ρ₁, ρ₂, ..., ρₘ} que especificam as condições de
interpretação de G, Sᵢ, Cᵢ e ⊗ em um dado domínio histórico ou cultural. O
horizonte hermenêutico garante que a instanciação do padrão não se reduza a uma
operação puramente mecânica de substituição, mas respeite as convenções
interpretativas do domínio. Por exemplo, no contexto da exegese bíblica, 𝒫
pode incluir restrições sobre quais passagens são paralelizáveis; no contexto
musical, restrições sobre quais intervalos harmônicos são admissíveis. Cada
ρₖ em 𝒢 é uma restrição que filtra ou pondera as instanciações válidas.

#### 2.1.2 Propriedades Formais

Sobre as cinco definições primitivas, o algoritmo PANVIEIRA possui oito
proposições formais que estabelecem suas propriedades invariantes, condições
de parada recursiva e métricas de validação. Essas proposições constituem o
esqueleto lógico do sistema e permitem verificações formais e empíricas da
correção das instanciações.

**Proposição 1 — Invariância de G**: Para toda instância eᵢ = Sᵢ ⊗ G ⊗ Cᵢ,
`CONTRACT({eᵢ}) = G`. Esta é a propriedade fundamental do padrão: não importa
quantas instanciações particulares sejam geradas por `EXPAND`, a operação de
`CONTRACT` deve sempre restituir o mesmo invariante G. A invariância é a
condição necessária para que a circularidade iterativa do padrão se mantenha
estável: se `CONTRACT` produzisse resultados diferentes a cada ciclo, o sistema
divergiria e a "pressão de unidade" vieiriana se perderia.

**Proposição 2 — Equivalência Genérica**: ∀i,j: `ABSTRACT(eᵢ) = ABSTRACT(eⱼ) = G`.
Esta proposição assegura que toda e qualquer instância gerada pelo padrão
compartilha o mesmo genérico. Ela é uma consequência direta da Proposição 1,
mas é enunciada separadamente porque define a noção de "conjunto semelhante"
no sentido haddadiano: duas expressões são semelhantes se e somente se suas
abstrações coincidem. Formalmente, a relação de semelhança assim definida é
uma relação de equivalência — é reflexiva, simétrica e transitiva.

**Proposição 3 — Diferença Específica**: ∃i ≠ j: eᵢ ≠ eⱼ. Se todas as
instâncias fossem idênticas, o padrão colapsaria numa repetição trivial. A
Proposição 3 exige que haja pelo menos duas instâncias distintas, garantindo
que a expansão produz variação genuína. Em termos computacionais, essa
propriedade implica que o conjunto {Sᵢ} × {Cᵢ} deve possuir cardinalidade
mínima de 2, o que confere ao padrão sua capacidade de expressar pluralidade
sem perder unidade.

**Proposição 4 — Recursividade com Critérios de Parada**: Cada Sᵢ pode ser ele
próprio uma tupla PANVIEIRA. A recursão é interrompida quando: (a) MDL não
reduz descrição; (b) G' é estável sob perturbação; (c) escala semântica mínima
atingida; (d) H(G|{Sᵢ⊗G⊗Cᵢ}) ≈ 0. Esta proposição é a mais complexa do
sistema, pois define as condições exatas em que a recursividade — que permite
análises fractais de textos e estruturas — deve cessar. O critério (a)
recorre ao Minimum Description Length (MDL) de Rissanen: se a descrição do
subpadrão não comprime os dados, não há ganho em recursar. O critério (b)
exige estabilidade do invariante sob perturbação — se pequenas variações nos
dados de entrada produzem grandes variações em G', o subpadrão não é robusto. O
critério (c) estabelece um limite mínimo de granularidade semântica abaixo
do qual a recursão perde significado. O critério (d) exige que a entropia
condicional de G dado o conjunto de instâncias seja próxima de zero, o que
indica que G captura toda a informação relevante das instâncias.

**Proposição 5 — Agnosticidade**: O algoritmo é definido sobre Σ arbitrário.
O PANVIEIRA não assume nenhuma propriedade específica do sistema semiótico
Σ sobre o qual opera. Essa agnosticidade é o que permite ao algoritmo ser
instanciado em língua natural, música, artes visuais, rituais litúrgicos,
programação orientada a objetos, bases de dados relacionais e qualquer outro
sistema que admita a distinção entre invariante e variante. Formalmente,
todas as definições e proposições são enunciadas em termos de Σ sem impor
restrições sobre a natureza dos elementos de Σ.

**Proposição 6 — Testabilidade do Padrão (TAP-PAN)**: O TAP-PAN é um protocolo
de validação empírica em quatro etapas para verificar se um dado conjunto de
expressões efetivamente segue o padrão PANVIEIRA. As etapas são: (1) invariância
de G — verificar via cosseno em embeddings que todas as abstrações são
semanticamente similares (cos ≥ 0,85); (2) independência Sᵢ/Cᵢ — verificar via
teste qui-quadrado que os diferenciadores e loci são estatisticamente
independentes (χ², p > 0,05); (3) validação cruzada por exclusão — remover
cada instância e verificar que `ABSTRACT` do conjunto reduzido permanece G;
(4) benchmark contra modelos nulos — comparar AIC/BIC do modelo PANVIEIRA com
modelos nulos (aleatório, unigrama, bigrama) para garantir que o padrão
efetivamente comprime os dados melhor que as alternativas.

**Proposição 7 — Coerência Semântica Interna (CSI)**: CSI(G, {Sᵢ}, {Cᵢ}) =
(1/n) Σ sim(φ(eᵢ), ē_φ), onde φ é embedding, ē_φ é o centróide dos embeddings,
e sim é similaridade cosseno. A métrica CSI mede o grau de coesão semântica de
um conjunto de instâncias PANVIEIRA: quanto mais próximo de 1, mais coeso é o
conjunto. O limiar de aceitação é definido como CSI > τ, onde τ = p₇₅ da
distribuição nula empírica gerada por permutações aleatórias dos componentes.
Esse limiar dinâmico adapta-se ao domínio, evitando que a métrica seja nem
muito frouxa (aceitando padrões espúrios) nem muito restritiva (rejeitando
padrões genuínos em domínios de alta variabilidade semântica).

**Proposição 8 — Circularidade**: G → `EXPAND` → `SERIALIZE` → `CONTRACT` → G.
Esta proposição formaliza a propriedade mais distintiva do padrão vieiriano:
a circularidade iterativa. O ciclo completo — abstração, expansão, serialização
e contração — constitui uma unidade operacional fechada. A cada iteração do
ciclo, o sistema opera uma "espiral hermenêutica" que aprofunda a compreensão
do invariante G. Formalmente, `CONTRACT(SERIALIZE(EXPAND(G))) = G` é uma
propriedade de idempotência que garante a estabilidade do sistema sob iteração.

### 2.2 As Quatro Operações

| Operação | Função | Equivalente Computacional |
|----------|--------|---------------------------|
| **ABSTRACT** | Extrai invariante G de expressões | `fold` / `reduce` |
| **EXPAND** | Gera instâncias por composição | `map` em programação funcional |
| **SERIALIZE** | Projeta conjunto paralelo em sequência | pipeline / lista ordenada |
| **CONTRACT** | Reduz série ao genérico | `fold` inverso |

A propriedade de **circularidade iterativa**: G → `EXPAND` → `SERIALIZE` → `CONTRACT` → G

As quatro operações constituem o núcleo funcional do framework Semiomorfologia
Vieiriana. Cada operação corresponde a um estágio do processo hermenêutico
vieiriano: `ABSTRACT` é o momento de percepção do invariante (o pregador
identifica o tema unificador); `EXPAND` é o momento de variação (o pregador
multiplica o tema em instâncias particulares); `SERIALIZE` é o momento de
disposição retórica (o pregador ordena as instâncias em sequência sermônica);
e `CONTRACT` é o momento de recapitulação (o pregador reconduz a multiplicidade
à unidade). A correspondência entre operações computacionais e estágios
hermenêuticos não é meramente analógica — ela é estrutural: tanto o sermão
quanto o algoritmo realizam o mesmo movimento formal de expansão e contração
em torno de um invariante.

### 2.3 Isomorfismos do Padrão

O PANVIEIRA demonstra que a estrutura vieiriana é isomórfica a:

- **Programação funcional**: `map(f, [x₁..xₙ])` — f é invariante G
- **Eletrônica**: circuito em paralelo com tensão invariante
- **Lógica formal**: quantificação universal ∀ com instanciação
- **Herança OOP**: classe base (G) + classes derivadas (Sᵢ)
- **Ritual litúrgico**: ladainha — invocação central + epítetos variáveis

Esses isomorfismos não são curiosidades superficiais, mas evidências de que o
padrão PANVIEIRA captura uma estrutura formal profunda e recorrente em sistemas
de organização semiótica e computacional. Cada isomorfismo oferece uma perspectiva
complementar sobre o padrão: a programação funcional revela sua estrutura
morfismática; a eletrônica, suas propriedades de invariância sob composição
paralela; a lógica formal, sua relação com quantificação e unificação; a OOP,
sua aplicabilidade como mecanismo de generalização; e o ritual litúrgico, sua
dimensão performativa e iterativa. A pluralidade de isomorfismos reforça a
tese de que o PANVIEIRA é um padrão universal de organização semiótica,
e não uma peculiaridade da prosa barroca portuguesa.

### 2.4 Recursividade

Cada diferenciador Sᵢ pode ser ele próprio uma tupla PANVIEIRA com invariante
interno G'. O algoritmo é aplicável recursivamente em qualquer nível de análise —
propriedade que permite análise fractal de textos barrocos e, no presente framework,
a extração de analogias aninhadas entre domínios naturais. A recursividade é
controlada pelos quatro critérios de parada enunciados na Proposição 4, garantindo
que o processo de decomposição não proceda infinitamente. Na prática, cada nível
recursivo revela uma camada adicional de estrutura semiótica: o primeiro nível
identifica os padrões macroscópicos; os níveis subsequentes decompõem cada
instância em subpadrões, e assim por diante, até que os critérios de parada
sejam satisfeitos. Essa propriedade é particularmente valiosa para a análise
de textos barrocos, onde a complexidade composicional frequentemente envolve
várias camadas de paralelismo encaixado.

---

## 3. Transposição para a Semiomorfologia

| Conceito PANVIEIRA | Estrutura Computacional |
|--------------------|------------------------|
| G (invariante) | `Sintagma.extrair_generico()` |
| {Sᵢ} (diferenciadores) | Lista de `Morfema` no `Sintagma` |
| {Cᵢ} (loci) | `descritores` e `propriedades` de cada `Morfema` |
| 𝒫 (horizonte hermenêutico) | Parâmetros de validação do `Motor` |
| `EXPAND` | `Motor.compor_sintagma()` |
| `SERIALIZE` | Leitura linear do `Sintagma.morfemas` |
| `CONTRACT` | `Sintagma.extrair_generico()` (redução N→1) |
| CIRCULARIDADE | `Motor.reiterar_enfaticamente()` |

A tabela acima resume o mapeamento entre os conceitos formais do PANVIEIRA e
as estruturas computacionais da Semiomorfologia Vieiriana. Cada conceito
abstrato é realizado como um componente concreto no sistema: o invariante G
é extraído pelo método `extrair_generico()` da classe `Sintagma`; os
diferenciadores são representados como instâncias da classe `Morfema`; e as
quatro operações são implementadas como métodos da classe `Motor`. O horizonte
hermenêutico 𝒫 é materializado como o conjunto de parâmetros de validação
que o `Motor` utiliza para filtrar instanciações inválidas. Esse mapeamento
preserva a estrutura formal do padrão enquanto o torna executável em código.

### 3.1 Os 4 Domínios como Morfologias

Vieira organiza a natureza em quatro escalas:
1. **Mineral** (insensível) — pedras
2. **Vegetal** (vegetativa) — espinhos/plantas
3. **Animal** (sensitiva) — aves
4. **Humana** (racional) — homens

Cada escala é uma **morfologia** — uma forma de organização da matéria com
propriedades emergentes específicas. O algoritmo extrai analogias dentro e entre
essas morfologias, preservando a estrutura G/{Sᵢ}/{Cᵢ} em cada domínio. A
escolha desses quatro domínios não é arbitrária: ela corresponde à grande cadeia
do ser (scala naturae) da filosofia medieval e renascentista, que ordena os
entes segundo seu grau de perfeição. Vieira utiliza essa hierarquia como
esqueleto argumentativo para demonstrar que a ação divina se manifesta em todos
os níveis da criação, do mais rudimentar ao mais elevado. Na Semiomorfologia,
cada domínio é modelado como um conjunto de morfemas com propriedades e
descritores específicos, permitindo que o algoritmo gere analogias
interdominiais que preservam tanto a estrutura formal quanto o conteúdo
semântico do raciocínio vieiriano.

### 3.2 Os 3 Tipos de Analogia

A tipologia de analogia do framework mapeia-se às operações PANVIEIRA:

| Tipo | Operação PANVIEIRA | Descrição |
|------|-------------------|-----------|
| **Heurística** | `ABSTRACT` não-óbvio | Descoberta de emergências não-lineares entre domínios distintos |
| **Funcional** | `EXPAND` com ⊗ diferente | Mesma função G, estruturas Sᵢ/Cᵢ diferentes |
| **Homológica** | CIRCLE recursivo | Mesma origem G, instanciações diversas em níveis distintos |

A analogia heurística é a mais inovadora do framework: ela detecta conexões
não-óbvias entre domínios que não partilham estrutura superficial, mas cujos
invariantes abstratos coincidem. A analogia funcional corresponde ao uso
clássico de paralelismo em Vieira — quando o pregador demonstra que o mesmo
princípio opera de maneiras diferentes em contextos distintos. A analogia
homológica é a mais profunda: ela identifica estruturas que derivam de uma
mesma origem comum e se diversificaram ao longo de níveis recursivos de
instanciação, revelando a arquitetura fractal do raciocínio barroco.

### 3.3 Instâncias em Outros Sistemas Semióticos

Uma das consequências mais notáveis da agnosticidade do PANVIEIRA (Proposição 5)
é sua capacidade de instanciar-se em sistemas semióticos radicalmente diversos.
A tabela abaixo sistematiza essas instanciações, mostrando como cada componente
formal do padrão se realiza em domínios específicos:

| Sistema Semiótico | G (invariante) | Sᵢ (diferenciador) | Cᵢ (locus) | Exemplo |
|-------------------|----------------|--------------------|------------|---------|
| **Língua natural** (Vieira) | Verbo / ação genérica | Tipo de natureza | Território de aplicação | "A natureza X o perseguiu em Y" |
| **Música** (coral) | Tema melódico | Voz (soprano, alto, etc.) | Registro (agudo, grave) | Fuga com sujeito em 4 vozes |
| **Artes visuais** | Símbolo central | Variação cromática | Quadrante da composição | Retábulo com 4 cenas paralelas |
| **Ritual litúrgico** | Invocação central | Epíteto divino | Intenção da prece | Ladainha com múltiplos epítetos |
| **OOP / Herança** | Classe base | Classe derivada | Contexto de uso | `Animal` → `Cão`, `Gato`, `Pássaro` |
| **SQL** | Schema relacional | Entidade (tabela) | Cláusula `WHERE` | `SELECT` sobre tabela filtrada |
| **Glossolalia** (Pentecostes) | Enunciação do Espírito | Língua (idioma) | Nação dos ouvintes | Atos 2:1-13 |

Cada instanciação preserva a estrutura fundamental G/{Sᵢ}/{Cᵢ} enquanto
adaptada às convenções do domínio. O caso da glossolalia pentecostal é
particularmente revelador: a narrativa de Atos dos Apóstolos descreve um
fenômeno estruturalmente idêntico ao padrão PANVIEIRA — um único invariante
(o enunciar do Espírito) manifesta-se em múltiplas línguas (diferenciadores)
para múltiplas nações (loci). Essa convergência entre exegese bíblica,
retórica barroca e teoria dos algoritmos reforça a tese de universalidade
do padrão.

---

## 4. Corpus Teórico do Autor

O presente framework articula-se com a linha de pesquisa do autor em semiótica
computacional. Cada obra citada abaixo contribui um componente essencial para a
arquitetura teórica da Semiomorfologia Vieiriana, formando um corpus coerente
que progride da fundamentação filosófica à formalização algorítmica e à
implementação computacional.

- **Semiografia (2025)** — DOI: 10.5281/zenodo.19546051. Matriz N-dimensional
  para modelagem semiótica. O PANVIEIRA é a instância 2D dessa matriz. A
  Semiografia fornece a base ontológica sobre a qual o PANVIEIRA é construído:
  toda instância do padrão é um ponto numa matriz semiótica de dimensionalidade
  arbitrária, e a operação `ABSTRACT` corresponde à projeção dessa matriz num
  subespaço de menor dimensionalidade.

- **Instância Mínima Tripla (2025)** — DOI: 10.5281/zenodo.19431553. Teoriza
  a polissemia constitutiva emergente de um gesto em três sistemas semióticos.
  O PANVIEIRA generaliza para n instâncias, com n ≥ 2. A Instância Mínima Tripla
  pode ser vista como um caso particular do PANVIEIRA onde n = 3 e os três
  diferenciadores operam em sistemas semióticos distintos (por exemplo, verbal,
  gestual e visual).

- **PANVIEIRA (2026)** — DOI: 10.5281/zenodo.20367826. Formalização do algoritmo agnóstico
  extraído da prosa sermônica de Vieira. Contém as cinco definições primitivas,
  as oito proposições formais e o protocolo TAP-PAN de testabilidade que
  constituem o núcleo matemático da Semiomorfologia Vieiriana.

- **Graúna — Gramática Universal Pancrônica** (em desenvolvimento) — Obra
  teórica em que o PANVIEIRA é elevado à categoria de operador pancrônico,
  aplicável a qualquer língua natural em qualquer período histórico. O conceito
  de "pancronia" designa a propriedade de um operador de funcionar independentemente
  da diacronia linguística: assim como o PANVIEIRA é agnóstico em relação ao
  sistema semiótico Σ (Proposição 5), o PANVIEIRA pancrônico é agnóstico em
  relação ao estágio diacrônico da língua. Graúna propõe que os padrões
  identificados por Haddad na prosa barroca são instâncias de operadores
  pancrônicos que governam a organização semiótica de todas as línguas naturais,
  não apenas do português seiscentista. Essa tese, se confirmada, teria
  implicações profundas para a linguística tipológica e para a teoria da
  mudança linguística, pois sugeriria que a recursividade e a circularidade
  do padrão PANVIEIRA são propriedades universais da cognição semiótica humana.

---

## 5. Referências

HADDAD, Jamil Almansur. *Vieira e o Barroco Brasileiro*. São Paulo: Companhia
Editora Nacional, 1957.

VIEIRA, Antônio. *Sermão da Sexagésima*. In: Sermões. Porto: Lello & Irmão, 1959.

MACHADO, Guilherme Gonçalves. *Semiografia: Sistema Formal para Análise Semiótica
Multidimensional*. Zenodo, 2025. DOI: 10.5281/zenodo.19546051.

MACHADO, Guilherme Gonçalves. *Instância Mínima Tripla*. Zenodo, 2025.
DOI: 10.5281/zenodo.19431553.

MACHADO, Guilherme Gonçalves. *PANVIEIRA: Um Algoritmo Agnóstico para Instanciação
de Série e Paralelo como Estrutura Semiótica Universal*. Zenodo, 2026.
DOI: 10.5281/zenodo.20367826.

MACHADO, Guilherme Gonçalves. *Graúna: Gramática Universal Pancrônica*. Em
desenvolvimento. Hubstry Deep Tech, 2026.

DEAN, Jeffrey; GHEMAMAT, Sanjay. MapReduce: Simplified Data Processing on Large
Clusters. *Communications of the ACM*, v. 51, n. 1, p. 107-113, 2008.

MEIJER, Erik; FOKKINGA, Maarten. Functional Programming with Bananas, Lenses,
Envelopes and Barbed Wire. In: *Functional Programming Languages and Computer
Architecture*. Springer, 1992. p. 124-144.

RISSANEN, Jorma. Modeling by Shortest Data Description. *Automatica*, v. 14,
n. 5, p. 465-471, 1978.

REIMERS, Nils; GUREVYCH, Iryna. Sentence-BERT: Sentence Embeddings using
Siamese BERT-Networks. In: *Proceedings of EMNLP 2019*, p. 3982-3992, 2019.

DEVLIN, Jacob; CHANG, Ming-Wei; LEE, Kenton; TOUTANOVA, Kristina. BERT:
Pre-training of Deep Bidirectional Transformers for Language Understanding. In:
*Proceedings of NAACL-HLT 2019*, p. 4171-4186, 2019.

NIELSEN, Michael A.; CHUANG, Isaac L. *Quantum Computation and Quantum
Information*. Cambridge: Cambridge University Press, 10th Anniversary Edition, 2010.

---

## 6. Diálogo com Algoritmos Clássicos

O padrão PANVIEIRA não é uma estrutura isolada: ele mantém diálogos formais
significativos com diversos algoritmos clássicos da ciência da computação.
Esses diálogos não são meras analogias superficiais — eles revelam que a
estrutura identificada por Haddad na prosa de Vieira corresponde a padrões
recorrentes na computação, sugerindo que o PANVIEIRA captura uma classe geral
de operações de transformação e organização de dados.

### 6.1 MapReduce e Big Data Semiótico

O paradigma MapReduce, introduzido por Dean e Ghemawat (2008) para processamento
distribuído de grandes volumes de dados, mantém correspondência estrutural direta
com as operações centrais do PANVIEIRA. A fase `Map` corresponde à operação
`EXPAND`: ambos tomam um único invariante e o multiplicam em instâncias
particulares aplicando uma função sobre cada elemento de uma coleção. A fase
`Reduce` corresponde à operação `CONTRACT`: ambos agregam um conjunto de
instâncias num resultado único por meio de uma função combinadora. Essa
correspondência sugere que a arquitetura MapReduce pode ser repurada para
processamento em larga escala de corpora semióticos — o que se pode denominar
"Big Data Semiótico" —, onde cada nó do cluster executa `EXPAND` sobre um
subconjunto do corpus e um nó central executa `CONTRACT` sobre os resultados
parciais para extrair o invariante G global.

### 6.2 Catamorfismo e Anamorfismo

Na teoria das álgebras iniciais e das álgebras terminais, Meijer e Fokkinga
(1992) formalizaram as noções de catamorfismo (`fold` / destruição) e
anamorfismo (`unfold` / construção). O PANVIEIRA pode ser compreendido como um
hilmorfismo — a composição de um anamorfismo com um catamorfismo: primeiro,
`EXPAND` (anamorfismo) desdobra G em instâncias particulares; depois, `CONTRACT`
(catamorfismo) redobra as instâncias de volta a G. Essa estrutura de
hilmorfismo é exatamente a circularidade iterativa da Proposição 8. A vantagem
desse enquadramento é que ele permite ao PANVIEIRA herdar as leis formais dos
morfismos — em particular, as leis de fusão e de identidade — garantindo
propriedades de composicionalidade e otimização algorítmica.

### 6.3 Teoria dos Grafos

A estrutura do PANVIEIRA pode ser representada como um grafo série-paralelo:
os diferenciadores Sᵢ formam ramos paralelos conectados ao nó central G, e
os loci Cᵢ situam cada ramo num contexto terminal. A decomposição série-paralelo
oferece algoritmos eficientes para verificar se um dado grafo pode ser
reconhecido como instância PANVIEIRA. Adicionalmente, algoritmos clássicos de
grafos como Ford-Fulkerson (para fluxo máximo) e matching bipartido podem ser
adaptados para encontrar o mapeamento ótimo entre domínios de Sᵢ e Cᵢ,
maximizando a cobertura semântica das instanciações geradas.

### 6.4 Inteligência Artificial e Aprendizado de Máquina

O aprendizado de máquina oferece ferramentas concretas para implementar
as operações do PANVIEIRA. O algoritmo K-Means pode ser utilizado para
implementar `ABSTRACT`: dado um conjunto de expressões, o clustering identifica
os centróides que funcionam como invariantes G. Embeddings semânticos (como
Sentence-BERT de Reimers e Gurevych, 2019) fornecem representações vetoriais
que permitem calcular a similaridade cosseno requerida pelo TAP-PAN e pela
métrica CSI. Modelos de linguagem como BERT (Devlin et al., 2019) podem gerar
instâncias automáticas via `EXPAND` a partir de um G fornecido como prompt.
O princípio MDL de Rissanen (1978), já incorporado nos critérios de parada
recursiva da Proposição 4, é um pilar teórico compartilhado entre o PANVIEIRA
e a teoria da aprendizagem estatística.

### 6.5 Lógica Formal e Unificação

O algoritmo de unificação de Robinson, fundamental para a resolução automática
em lógica de primeira ordem, guarda correspondência direta com a operação
`CONTRACT` do PANVIEIRA. A unificação encontra a substituição mais geral que
torna dois termos logicamente equivalentes; analogamente, `CONTRACT` encontra
o invariante mais geral que torna um conjunto de instâncias estruturalmente
equivalentes. Essa correspondência sugere que técnicas de prova automática de
teoremas podem ser aplicadas para verificar formalmente a correção de
instanciações PANVIEIRA, garantindo que `ABSTRACT(eᵢ) = G` para todo eᵢ no
conjunto, e que as instâncias geradas por `EXPAND` satisfazem as restrições
do horizonte hermenêutico 𝒫.

---

## 7. Extensões Quânticas (Roteiro)

A possibilidade de extensões quânticas para o PANVIEIRA abre um horizonte
teórico de grande alcance. O roteiro a seguir esquematiza duas vias principais
de quantização do algoritmo, identificando os componentes clássicos que podem
ser acelerados ou generalizados por meio de computação quântica.

### 7.1 Q-PANVIEIRA: Versão Totalmente Quântica

No Q-PANVIEIRA, o invariante G é colocado em superposição quântica sobre todas
as instanciações possíveis simultaneamente. Formalmente, o estado quântico do
sistema é: |Ψ⟩ = Σ αᵢ |Sᵢ ⊗ G ⊗ Cᵢ⟩, onde os coeficientes αᵢ são amplitudes
de probabilidade complexas. A operação `CONTRACT` é realizada via interferência
quântica: quando o sistema é medido, as amplitudes construtivas para as
instâncias que compartilham o mesmo G são amplificadas, enquanto as amplitudes
destrutivas para as instâncias que não compartilham G se cancelam. O resultado
da medição é, portanto, G com alta probabilidade. Essa abordagem permite que
a operação de abstração explore exponencialmente mais instanciações em tempo
polinomial, usando o paralelismo quântico inerente à superposição de estados.

### 7.2 H-PANVIEIRA: Versão Híbrida Clássico-Quântica

A versão híbrida propõe uma orquestração onde a maioria das operações permanece
clássica, mas componentes computacionalmente intensivos são delegados ao
processador quântico (QPU). Especificamente: a operação `EXPAND` é executada
no QPU usando circuitos de variação que geram superposições de instanciações;
a busca de loci ótimos (Cᵢ) é acelerada pelo algoritmo de Grover, que fornece
speedup quadrático sobre a busca clássica; e a operação `ABSTRACT` é
implementada via VQE (Variational Quantum Eigensolver), que minimiza a função
objetivo de distância entre as instâncias e o invariante candidato. Essa
abordagem é mais pragmática do que o Q-PANVIEIRA totalmente quântico, pois
requer menos qubits e é compatível com a arquitetura NISQ (Noisy
Intermediate-Scale Quantum) atual.

### 7.3 Mapeamento de Algoritmos Quânticos

A tabela abaixo sistematiza a correspondência entre algoritmos quânticos
clássicos e as operações do PANVIEIRA:

| Algoritmo Quântico | Operação PANVIEIRA | Função | Speedup Esperado |
|-------------------|-------------------|--------|-------------------|
| **Deutsch-Jozsa** | `CONTRACT` | Verificação de invariância de G (global vs. local) | Exponencial |
| **Grover** | Busca de Cᵢ | Busca do locus ótimo no espaço de instanciações | Quadrático |
| **Shor** | Decomposição de ⊗ | Fatoração do operador de composição em primos | Exponencial |
| **QAOA** | Otimização de ⊗ | Encontrar ⊗ que maximiza CSI | Quadrático (aprox.) |

O algoritmo de Deutsch-Jozsa é particularmente adequado para verificar a
Proposição 1 (Invariância de G) com um único acesso quântico ao oráculo,
enquanto classicamente seriam necessários múltiplos acessos. O algoritmo de
Grover pode acelerar a busca pelo locus Cᵢ que maximiza a coerência semântica
interna. O algoritmo de Shor pode decompor operadores de composição ⊗
complexos em componentes primitivos. O QAOA (Quantum Approximate Optimization
Algorithm) pode otimizar os parâmetros do operador ⊗ para maximizar a métrica
CSI sobre um dado corpus. Esses mapeamentos constituem um roteiro de pesquisa
que conecta a Semiomorfologia Vieiriana às fronteiras da computação quântica.

---

*Documento mantido por Guilherme Gonçalves Machado | Hubstry Deep Tech*
*Contato: guilhermemachado@hubstry.onmicrosoft.com | www.hubstry.dev*
