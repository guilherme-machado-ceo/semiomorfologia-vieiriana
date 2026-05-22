# Fundamentação Teórica

## Vieira e a Teoria dos Conjuntos Semelhantes

Baseado nas páginas 14-15 de *Vieira e o Barroco Brasileiro* (Damaso Alonso, 1962).

### Passo 1: O Paralelismo Sintático

Vieira constrói períodos onde quatro (ou mais) expressões se dispõem em paralelo:

> "A natureza insensível o perseguiu nas pedras;  
> a vegetativa, nos espinhos;  
> a sensitiva, nas aves;  
> a racional, nos homens"

Cada expressão possui:
- **Sujeito** diferente (insensível / vegetativa / sensitiva / racional)
- **Mesma estrutura sintática** ("a natureza X, nos Y")
- **Mesmo conteúdo conceptual** (a natureza persegue/age)

### Passo 2: A Redução ao Genérico

Damaso Alonso formaliza: as quatro expressões reduzem-se a uma só:

> **"a natureza [genérica] o perseguiu [em 4 modos]"**

A "primeira coluna de quatro termos pode reduzir-se a um só, genérico".

### Passo 3: A Reiteração Enfática

O processo de reiteração multiplica o mesmo conteúdo conceptual com variações formais. Vieira não repete — **reitera enfaticamente**, criando:
- Circularidade do estilo
- Pressão da mais absoluta unidade
- Parada para refletir, ruminar, esgotar numa sondagem

## Transposição Algorítmica

| Conceito Vieiriano | Estrutura Computacional |
|--------------------|------------------------|
| 4 expressões paralelas | `Sintagma` com lista de `Morfema` |
| Redução ao genérico | `Sintagma.extrair_generico()` |
| Reiteração enfática | `Motor.reiterar_enfaticamente()` |
| Mesmo conteúdo, formas diferentes | `TipoAnalogia.HEURISTICA` |
| Mesma função, origens diferentes | `TipoAnalogia.FUNCIONAL` |
| Mesma origem, funções divergentes | `TipoAnalogia.HOMOLOGICA` |

## Os 4 Domínios como Morfologias

Vieira organiza a natureza em quatro escalas:
1. **Mineral** (insensível) — pedras
2. **Vegetal** (vegetativa) — espinhos/plantas
3. **Animal** (sensitiva) — aves
4. **Humana** (racional) — homens

Cada escala é uma **morfologia** — uma forma de organização da matéria com propriedades emergentes específicas. O algoritmo extrai analogias dentro e entre essas morfologias.
