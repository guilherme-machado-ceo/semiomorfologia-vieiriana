# Semiomorfologia Vieiriana

> Framework agnóstico de extração de analogias nas 4 morfologias naturais  
> Baseado na *Teoria dos Conjuntos Semelhantes* de Damaso Alonso / Vieira

---

## O que é

Este projeto formaliza algoritmicamente a estilística barroca de Vieira — especificamente o processo de **reiteração enfática**, a **redução de N termos a 1 genérico** e o **paralelismo sintático** — como um sistema computacional de descoberta de analogias entre domínios naturais:

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

## Instalação (Windows 11 / PowerShell / 8GB RAM)

### Requisitos
- Python 3.10+
- ~50MB de disco (sem dependências pesadas)
- 8GB RAM são suficientes (não usa PyTorch/TensorFlow)

### Passo a passo no PowerShell

```powershell
# 1. Clone o repositório
git clone https://github.com/seu-usuario/semiomorfologia-vieiriana.git
cd semiomorfologia-vieiriana

# 2. Crie ambiente virtual (recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instale dependências leves
pip install -r requirements.txt

# 4. Execute testes
python -m pytest tests/ -v

# 5. Rode um exemplo
python examples/demo_completo.py
```

Ou use o script automatizado:
```powershell
.\scripts\setup_windows.ps1
```

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

Veja `examples/` para demonstrações completas.

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
│  1. FUNDAÇÃO TEÓRICA (Vieira/Damaso Alonso) │
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

MIT License — veja [LICENSE](LICENSE).

---

> *"As quatro expressões possuem o mesmo conteúdo conceptual. Genéricamente iguais, diferem especificamente."*  
> — Vieira, via Damaso Alonso
