import numpy as np
from typing import List, Dict, Any
from collections import Counter

def cosseno(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    a, b = np.array(v1, dtype=float), np.array(v2, dtype=float)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

def jaccard(conj1: set, conj2: set) -> float:
    if not conj1 and not conj2:
        return 1.0
    inter = len(conj1 & conj2)
    uni = len(conj1 | conj2)
    return inter / uni if uni > 0 else 0.0

def euclidiana(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    return 1.0 / (1.0 + float(np.linalg.norm(np.array(v1) - np.array(v2))))

def manhattan(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    return 1.0 / (1.0 + float(np.sum(np.abs(np.array(v1) - np.array(v2)))))

def pearson(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2) or len(v1) < 2:
        return 0.0
    a, b = np.array(v1, dtype=float), np.array(v2, dtype=float)
    ma, mb = np.mean(a), np.mean(b)
    da, db = a - ma, b - mb
    sd = np.sqrt(np.sum(da**2)) * np.sqrt(np.sum(db**2))
    if sd == 0:
        return 0.0
    return float(np.sum(da * db) / sd)

def spearman(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2) or len(v1) < 2:
        return 0.0
    from scipy.stats import spearmanr
    corr, _ = spearmanr(v1, v2)
    return float(abs(corr)) if not np.isnan(corr) else 0.0

def sobreposicao_descritores(m1: Dict[str, Any], m2: Dict[str, Any]) -> float:
    d1 = set(str(v) for v in m1.get("descritores", []))
    d2 = set(str(v) for v in m2.get("descritores", []))
    if not d1 and not d2:
        return 0.1
    return jaccard(d1, d2)

def distancia_combinada(m1: Dict, m2: Dict) -> float:
    pesos = {"descritores": 0.35, "propriedades": 0.30, "dominios": 0.20, "relacoes": 0.15}
    props = list(set(list(m1.get("propriedades", {}).keys()) + list(m2.get("propriedades", {}).keys())))
    vals1 = [m1.get("propriedades", {}).get(p, 0) for p in props]
    vals2 = [m2.get("propriedades", {}).get(p, 0) for p in props]
    comp = 0.0
    comp += pesos["descritores"] * sobreposicao_descritores(m1, m2)
    comp += pesos["propriedades"] * (cosseno(vals1, vals2) if vals1 else 0.0)
    dom1 = set(m1.get("dominios", []))
    dom2 = set(m2.get("dominios", []))
    comp += pesos["dominios"] * jaccard(dom1, dom2)
    r1 = set(str(r) for r in m1.get("relacoes", []))
    r2 = set(str(r) for r in m2.get("relacoes", []))
    comp += pesos["relacoes"] * jaccard(r1, r2)
    return comp
