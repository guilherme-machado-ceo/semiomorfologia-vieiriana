# Corpus PANVIEIRA (v1)

Texto-base: transcrições do Wikisource em português (domínio público), com a ortografia das transcrições preservada. O Sermão da Sexagésima é subpágina de *Sermões do padre Antonio Vieira* (Lisboa, J.M.C. Seabra e T.Q. Antunes, 1855). Os outros dois sermões são páginas avulsas do Wikisource; a edição-fonte dessas transcrições e as datas indicadas nos títulos (1640 e 1670) ainda precisam ser conferidas.

| Arquivo | Conteúdo |
|---|---|
| `corpus-panvieira-wikisource-v1.json` | 3 sermões (Sexagésima; Pelo Bom Sucesso das Armas de Portugal contra as de Holanda; Do Mandato), 104 parágrafos numerados, com página, revisão, URL, data de coleta e SHA-256 de cada texto |
| `manual-anotacao-v3.txt` | Manual de anotação **vigente** (v3), usado nas anotações cegas da pasta `anotacoes/` |
| `manual-anotacao-v2.txt` | Manual anterior (v2), mantido para histórico |
| `anotacoes/claude-opus55-manual-v3.jsonl` | Anotação cega do Claude Opus 5.5 com o manual v3 (um registro por bloco de parágrafos) |
| `anotacoes/gemini4argon-manual-v3.jsonl` | Anotação cega do Gemini 4 Argon com o manual v3; o bloco 1 da Sexagésima falhou por tempo esgotado e foi refeito (vale a última resposta bem-sucedida) |
| `anotacoes/correspondencia-v3.csv` | Correspondência entre os anotadores gerada por `scripts/gerar_concordancia.py` (casamento bipartido ótimo, pontuação e mapeamento de ramos) |

As anotações são **propostas de modelos**, não conjunto-ouro: ainda não passaram por adjudicação humana.

Os exemplos dos manuais v2 e v3 foram tirados dos próprios sermões anotados (entre eles a ocorrência canônica abaixo). O reconhecimento desses trechos pelos modelos não é evidência independente; a medição futura deve separar um conjunto de desenvolvimento do manual de um conjunto de medição.

O gerador descarta as estruturas que o próprio anotador marcou com confiança zero, as que têm menos de dois ramos e as que citam trecho inexistente; as demais inconsistências (elipse, G sem forma explícita, G diferente do texto, trechos sobrepostos) ficam como alertas. Além de `concordante`, a correspondência registra o estado `mesma_passagem`: os dois modelos marcaram a mesma passagem, mas delimitaram G, S ou C de modo diferente.

O último parágrafo do Sermão do Mandato (`189440-p031`) contém resíduo de folha de estilo do Wikisource. O arquivo do corpus foi mantido intacto, porque é a fonte exata que os anotadores receberam; o resíduo é removido apenas na geração dos dados da plataforma.

Pendência da v2 do corpus: Sermão de Santo António (aos peixes), cujo título no Wikisource difere do buscado.

## Fundamentação teórica

O padrão anotado foi descrito pela crítica antes da sua formalização computacional:

- HADDAD, Jamil Almansur. *Vieira e o Barroco Brasileiro*. São Paulo: Companhia Editora Nacional, 1957, especialmente p. 14-15, onde a série paralela da Sexagésima é reduzida a um só termo genérico. Haddad caracteriza também a "tendência à circularidade do estilo" e o "estilo de estase" (ver `docs/TEORIA.md`).
- A expressão "pluralidade de forma unitária", usada no site e no paper, deve ser conferida contra o texto de Haddad antes de ser atribuída a ele entre aspas.

**Contribuição do PANVIEIRA** (distinta da de Haddad): formalização da estrutura como tupla ⟨G, {Sᵢ}, {Cᵢ}⟩, critérios operacionais de inclusão (manual v3), anotação reprodutível do corpus e medida da reconhecibilidade do padrão por anotadores independentes.

## Ocorrência canônica

| Parágrafo | Trecho | Papel |
|---|---|---|
| `239684-p003` (Sermão da Sexagésima) | "A natureza insensivel o perseguiu nas pedras; a vegetativa, nos espinhos; a sensitiva, nas aves; a racional, nos homens." | exemplo analisado por Haddad (1957, p. 14-15); G = "o perseguiu", elidido do 2º ramo em diante; categoria nuclear; é exemplo positivo do manual, portanto o reconhecimento pelos modelos não conta como evidência |

As demais ocorrências estão nos arquivos de anotação; cada uma remete ao parágrafo pelo identificador `pageid-pNNN`.
