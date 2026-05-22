"""
Ontologia Semiomorfológica
Unidades fundamentais: Morfema, Sintagma, Analogia, NivelOrganizacao
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np


class TipoAnalogia(Enum):
    """Três tipos de analogia prescritas pelo algoritmo."""
    HEURISTICA = "heuristica"
    FUNCIONAL = "funcional"
    HOMOLOGICA = "homologica"


class DominioNatural(Enum):
    """Os quatro domínios da natureza (conjuntos semelhantes vieirianos)."""
    MINERAL = "mineral"
    VEGETAL = "vegetal"
    ANIMAL = "animal"
    HUMANO = "humano"


class NivelOrganizacao(Enum):
    """Níveis de organização para extração morfológica."""
    ATOMICO = "atomico"
    MOLECULAR = "molecular"
    CELULAR = "celular"
    TISSULAR = "tissular"
    ORGANICO = "organico"
    ECOSSISTEMICO = "ecossistemico"


@dataclass
class Morfema:
    """
    Unidade mínima de forma/significado na semiomorfologia.

    Equivalente computacional ao termo individual no paralelismo vieiriano,
    e.g., "nas pedras", "nos espinhos", "nas aves", "nos homens".
    """
    id: str
    dominio: DominioNatural
    nivel: NivelOrganizacao
    descritores: Dict[str, Any] = field(default_factory=dict)
    propriedades: Dict[str, float] = field(default_factory=dict)

    def vetor_propriedades(self) -> np.ndarray:
        """Retorna vetor numérico das propriedades para cálculos de distância."""
        if not self.propriedades:
            return np.array([])
        return np.array(list(self.propriedades.values()), dtype=float)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Morfema):
            return NotImplemented
        return self.id == other.id


@dataclass
class Sintagma:
    """
    Agrupamento paralelístico de morfemas (conjunto semelhante vieiriano).

    Exemplo vieiriano:
        "A natureza insensível o perseguiu nas pedras;
         a vegetativa, nos espinhos;
         a sensitiva, nas aves;
         a racional, nos homens"

    → Reduz-se ao genérico: "a natureza [genérica] o perseguiu [em 4 modos]"
    """
    id: str
    morfemas: List[Morfema] = field(default_factory=list)
    tipo_reiteracao: str = "paralelistica"
    conteudo_generico: Optional[str] = None

    def extrair_generico(self) -> str:
        """
        Reduz a primeira coluna de N termos a um só genérico.

        Algoritmo: interseção semântica dos descritores comuns + domínio base.
        """
        if not self.morfemas:
            self.conteudo_generico = "vazio"
            return self.conteudo_generico

        # Interseção de chaves de descritores
        descritores_comuns: set[str] = set.intersection(
            *[set(m.descritores.keys()) for m in self.morfemas]
        )

        dominio_base = self.morfemas[0].dominio.value
        self.conteudo_generico = f"conjunto_{dominio_base}_generico"
        return self.conteudo_generico

    def adicionar_morfema(self, morfema: Morfema) -> None:
        """Adiciona morfema e invalida cache do genérico."""
        self.morfemas.append(morfema)
        self.conteudo_generico = None


@dataclass
class Analogia:
    """
    Relação de analogia entre dois morfemas/sintagmas.

    Representa a 'ponte' cognitiva entre duas unidades morfológicas,
    classificada em heurística, funcional ou homológica.
    """
    fonte: Morfema
    alvo: Morfema
    tipo: TipoAnalogia
    forca: float  # 0.0 a 1.0
    mapeamento: Dict[str, str] = field(default_factory=dict)
    aplicacao_industrial: Optional[str] = None

    def serializar(self) -> Dict[str, Any]:
        """Serializa para dicionário JSON-friendly."""
        return {
            "fonte_id": self.fonte.id,
            "alvo_id": self.alvo.id,
            "tipo": self.tipo.value,
            "forca": round(float(self.forca), 3),
            "mapeamento": self.mapeamento,
            "aplicacao": self.aplicacao_industrial,
        }

    def __repr__(self) -> str:
        return (
            f"Analogia({self.fonte.id} → {self.alvo.id} | "
            f"{self.tipo.value} | força={self.forca:.2f})"
        )
