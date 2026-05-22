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

### 1.2 A Redução ao Genérico

Haddad formaliza: as quatro expressões reduzem-se a uma só:

> **"a natureza [genérica] o perseguiu [em 4 modos]"**

A "primeira coluna de quatro termos pode reduzir-se a um só, genérico" (Haddad, 1957, p. 14-15).

### 1.3 A Reiteração Enfática

O processo de reiteração multiplica o mesmo conteúdo conceptual com variações formais.
Vieira não repete — **reitera enfaticamente**, criando:
- Circularidade do estilo
- Pressão da mais absoluta unidade
- Parada para refletir, ruminar, esgotar numa sondagem

Haddad denomina esta propriedade "tendência à circularidade do estilo" e o caracteriza
como "estilo de estase": aprofundamento do mesmo ponto por sondagem em múltiplas
direções específicas, com retorno ao centro.

---

## 2. Do PANVIEIRA à Semiomorfologia

O presente framework (**Semiomorfologia Vieiriana**) é a transposição computacional
do **Algoritmo PANVIEIRA**, formalizado pelo autor em preprint (Zenodo, Maio 2026).

### 2.1 O Algoritmo PANVIEIRA

O PANVIEIRA abstrai a estrutura vieiriana como padrão computacional agnóstico,
instanciável em qualquer sistema semiótico. É definido como tupla:

**PANVIEIRA = ⟨G, {Sᵢ}, {Cᵢ}, ⊗, π, ρ⟩**

Onde:
- **G** = termo genérico (invariante) — equivalente ao "conteúdo conceptual" de Haddad
- **{Sᵢ}** = conjunto de diferenciadores específicos — as variações formais
- **{Cᵢ}** = conjunto de loci de aplicação — os territórios/especificações
- **⊗** = operador de composição
- **π** = projeção de superfície (serialização)
- **ρ** = redução (contração ao genérico)

### 2.2 As Quatro Operações

| Operação | Função | Equivalente Computacional |
|----------|--------|---------------------------|
| **ABSTRACT** | Extrai invariante G de expressões | `fold` / `reduce` |
| **EXPAND** | Gera instâncias por composição | `map` em programação funcional |
| **SERIALIZE** | Projeta conjunto paralelo em sequência | pipeline / lista ordenada |
| **CONTRACT** | Reduz série ao genérico | `fold` inverso |

A propriedade de **circularidade iterativa**: G → EXPAND → SERIALIZE → CONTRACT → G

### 2.3 Isomorfismos do Padrão

O PANVIEIRA demonstra que a estrutura vieiriana é isomórfica a:

- **Programação funcional**: `map(f, [x₁..xₙ])` — f é invariante G
- **Eletrônica**: circuito em paralelo com tensão invariante
- **Lógica formal**: quantificação universal ∀ com instanciação
- **Herança OOP**: classe base (G) + classes derivadas (Sᵢ)
- **Ritual litúrgico**: ladainha — invocação central + epítetos variáveis

### 2.4 Recursividade

Cada diferenciador Sᵢ pode ser ele próprio uma tupla PANVIEIRA com invariante
interno G'. O algoritmo é aplicável recursivamente em qualquer nível de análise —
propriedade que permite análise fractal de textos barrocos e, no presente framework,
a extração de analogias aninhadas entre domínios naturais.

---

## 3. Transposição para a Semiomorfologia

| Conceito PANVIEIRA | Estrutura Computacional |
|--------------------|------------------------|
| G (invariante) | `Sintagma.extrair_generico()` |
| {Sᵢ} (diferenciadores) | Lista de `Morfema` no `Sintagma` |
| {Cᵢ} (loci) | `descritores` e `propriedades` de cada `Morfema` |
| EXPAND | `Motor.compor_sintagma()` |
| SERIALIZE | Leitura linear do `Sintagma.morfemas` |
| CONTRACT | `Sintagma.extrair_generico()` (redução N→1) |
| CIRCULARIDADE | `Motor.reiterar_enfaticamente()` |

### 3.1 Os 4 Domínios como Morfologias

Vieira organiza a natureza em quatro escalas:
1. **Mineral** (insensível) — pedras
2. **Vegetal** (vegetativa) — espinhos/plantas
3. **Animal** (sensitiva) — aves
4. **Humana** (racional) — homens

Cada escala é uma **morfologia** — uma forma de organização da matéria com
propriedades emergentes específicas. O algoritmo extrai analogias dentro e entre
essas morfologias, preservando a estrutura G/{Sᵢ}/{Cᵢ} em cada domínio.

### 3.2 Os 3 Tipos de Analogia

A tipologia de analogia do framework mapeia-se às operações PANVIEIRA:

| Tipo | Operação PANVIEIRA | Descrição |
|------|-------------------|-----------|
| **Heurística** | ABSTRACT não-óbvio | Descoberta de emergências não-lineares entre domínios distintos |
| **Funcional** | EXPAND com ⊗ diferente | Mesma função G, estruturas Sᵢ/Cᵢ diferentes |
| **Homológica** | CIRCLE recursivo | Mesma origem G, instanciações diversas em níveis distintos |

---

## 4. Corpus Teórico do Autor

O presente framework articula-se com a linha de pesquisa do autor em semiótica
computacional:

- **Semiografia (2025)** — DOI: 10.5281/zenodo.19546051. Matriz N-dimensional
  para modelagem semiótica. O PANVIEIRA é a instância 2D dessa matriz.

- **Instância Mínima Tripla (2025)** — DOI: 10.5281/zenodo.19431553. Teoriza
  a polissemia constitutiva emergente de um gesto em três sistemas semióticos.
  O PANVIEIRA generaliza para n instâncias, com n ≥ 2.

- **PANVIEIRA (2026)** — Preprint Zenodo. Formalização do algoritmo agnóstico
  extraído da prosa sermônica de Vieira.

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

---

*Documento mantido por Guilherme Gonçalves Machado | Hubstry Deep Tech*  
*Contato: guilhermemachado@hubstry.onmicrosoft.com | www.hubstry.dev*
