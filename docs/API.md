# Referência da API

## Classes Principais

### `Morfema`
Unidade mínima de análise.

```python
Morfema(
    id: str,
    dominio: DominioNatural,
    nivel: NivelOrganizacao,
    descritores: dict = {},
    propriedades: dict = {}
)
```

### `Sintagma`
Agrupamento paralelístico com redução ao genérico.

```python
s = Sintagma(id="s1", morfemas=[m1, m2, m3])
s.extrair_generico()  # → "conjunto_mineral_generico"
```

### `MotorSemiomorfologico`
Orquestrador principal.

```python
motor = MotorSemiomorfologico()

# Composição
sintagma = motor.compor_sintagma(corpus)

# Extração
resultados = motor.extrair_analogias_dominio(corpus, DominioNatural.MINERAL)
# resultados[TipoAnalogia.HEURISTICA] → List[Analogia]

# Pontes cruzadas
pontes = motor.extrair_analogias_cruzadas({DominioNatural.MINERAL: corpus1, ...})

# Conhecimento aplicado
conhecimentos = motor.gerar_conhecimento_aplicado(analogias)
```

## Extratores Especializados

Cada extrator implementa 3 métodos:
- `extrair_heuristica(corpus)` → analogias de descoberta
- `extrair_funcional(corpus)` → analogias de função
- `extrair_homologica(corpus)` → analogias de origem

## Avaliadores

### `AvaliadorTRL`
```python
avaliador = AvaliadorTRL()
resultado = avaliador.avaliar(analogia)
# {"nivel": 4, "descricao": "Validação em laboratório", ...}
```

### `AvaliadorMercado`
```python
avaliador = AvaliadorMercado()
resultado = avaliador.avaliar(analogia)
# {"potencial": "ALTO", "riscos": [...], "investimento_necessario": "R$ 5-15M"}
```
