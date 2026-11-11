"""
Extração determinística do invariante G a partir de instâncias textuais.

Cada instância tem a forma eᵢ = Sᵢ ⊗ G ⊗ Cᵢ (composição por justaposição de
tokens). O invariante é estimado como a maior subsequência contígua de tokens
presente em todas as instâncias.

Limites conhecidos (documentados de propósito):
- Com uma única instância, G não é identificável: a função devolve a própria
  instância, e a circularidade não pode ser afirmada.
- Se os diferenciadores ou os loci compartilharem palavras entre si, pode
  haver mais de uma subsequência comum de mesmo tamanho. O desempate escolhe a
  candidata mais próxima do centro da primeira instância, porque na forma
  Sᵢ ⊗ G ⊗ Cᵢ o invariante ocupa a posição medial.
- Elipse (G omitido em ramos, como em "a vegetativa, nos espinhos") não é
  recuperável por comparação de cadeias; isso exige anotação ou extração
  estruturada sobre o texto, fora do escopo desta função.
"""

from typing import List, Optional, Tuple


def _tokens(texto: str) -> List[str]:
    return texto.split()


def _contem(seq: List[str], sub: List[str]) -> bool:
    n, m = len(seq), len(sub)
    return any(seq[i:i + m] == sub for i in range(n - m + 1))


def extrair_invariante(instancias: List[str]) -> str:
    """
    Devolve a maior subsequência contígua de tokens comum a todas as instâncias.

    Retorna "" se não houver instâncias ou nenhum token comum.
    """
    if not instancias:
        return ""
    if len(instancias) == 1:
        return instancias[0]

    seqs = [_tokens(t) for t in instancias]
    base = seqs[0]
    outras = seqs[1:]
    centro = (len(base) - 1) / 2.0

    for tamanho in range(len(base), 0, -1):
        candidatas: List[Tuple[float, int]] = []
        for ini in range(len(base) - tamanho + 1):
            sub = base[ini:ini + tamanho]
            if all(_contem(s, sub) for s in outras):
                meio = ini + (tamanho - 1) / 2.0
                candidatas.append((abs(meio - centro), ini))
        if candidatas:
            _, ini = min(candidatas)
            return " ".join(base[ini:ini + tamanho])
    return ""


def invariante_ou_none(instancias: List[str]) -> Optional[str]:
    """Versão que devolve None em vez de cadeia vazia."""
    g = extrair_invariante(instancias)
    return g if g else None
