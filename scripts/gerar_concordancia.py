"""
Gera os dados da vertical Humanidades Digitais (concordanciador) e do
painel de Governança de IA a partir do corpus e das anotações cegas.

Uso:
    python scripts/gerar_concordancia.py

Entradas:
    corpus/corpus-panvieira-wikisource-v1.json
    corpus/anotacoes/*.jsonl      (uma anotação por modelo, mesmo manual)

Saídas:
    src/semiomorfologia/web/dados/concordancia.json
    corpus/anotacoes/correspondencia-v3.csv

Princípios:
- Validação independente: G, S, C e G_forma são conferidos contra o texto
  do parágrafo; não se confia no campo "trechos_literais_ok" do anotador.
- Posições: cada trecho é localizado por deslocamento de caracteres, em
  ordem ao longo do parágrafo, para distinguir repetições literais
  (ex.: "Outra parte… Outra parte").
- Casamento entre anotadores: bipartido ótimo (algoritmo húngaro) por
  parágrafo, com mapeamento ótimo entre ramos; nada é guloso.
- As anotações dos dois modelos são preservadas integralmente, inclusive
  quando concordam.
"""
import csv
import json
import pathlib
import re
import unicodedata
from datetime import datetime, timezone

import numpy as np
from scipy.optimize import linear_sum_assignment

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CORPUS = RAIZ / "corpus" / "corpus-panvieira-wikisource-v1.json"
ANOTACOES = {
    "claude": RAIZ / "corpus" / "anotacoes" / "claude-opus55-manual-v3.jsonl",
    "gemini": RAIZ / "corpus" / "anotacoes" / "gemini4argon-manual-v3.jsonl",
}
NOMES = {"claude": "Claude Opus 5.5", "gemini": "Gemini 4 Argon"}
SAIDA = RAIZ / "src" / "semiomorfologia" / "web" / "dados" / "concordancia.json"
CORRESP = RAIZ / "corpus" / "anotacoes" / "correspondencia-v3.csv"
CONTEXTO = 90
LIMIAR_G = 0.5        # semelhança mínima de G (lema igual conta 1,0)
LIMIAR_RAMOS = 0.5    # proporção mínima de ramos casados (pelo maior número de ramos)
LIMIAR_RAMO = 0.3     # sobreposição mínima (Jaccard de caracteres) para casar um ramo
CSS_WIKISOURCE = re.compile(r"\.mw-parser-output[^{}]*\{[^{}]*\}")


# ---------------------------------------------------------------- utilidades

def _nulo(v):
    """Normaliza ausência: None, "", "null", "None" → None."""
    if v is None:
        return None
    if isinstance(v, str) and v.strip().lower() in ("", "null", "none"):
        return None
    return v


def _tokens(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return set(re.findall(r"\w+", s))


def _jac_tokens(a, b):
    a, b = _tokens(a), _tokens(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def _jac_pos(p, q):
    """Jaccard entre dois intervalos de caracteres [ini, fim)."""
    if not p or not q:
        return 0.0
    inter = max(0, min(p[1], q[1]) - max(p[0], q[0]))
    uniao = max(p[1], q[1]) - min(p[0], q[0])
    return inter / uniao if uniao else 0.0


# ------------------------------------------------------- leitura e validação

def _ler(caminho):
    """Lê o JSONL; para cada bloco, vale a última resposta bem-sucedida."""
    blocos = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        r = json.loads(linha)
        chave = (r.get("revid"), r.get("bloco"))
        ok = not (r.get("erro") or r.get("erro_json"))
        anterior = blocos.get(chave)
        if anterior is None or ok or not anterior[0]:
            blocos[chave] = (ok, r)
    return list(blocos.values())


def _localizar(texto, e):
    """Localiza G, S, C e G_forma por posição, em ordem no parágrafo.

    Devolve (ramos com posições, posição de G, problemas).
    """
    problemas, ramos, cursor = [], [], 0
    for r in e.get("ramos", []):
        S, C, Gf = r.get("S") or "", r.get("C") or "", _nulo(r.get("G_forma"))
        s_i = texto.find(S, cursor) if S else -1
        if S and s_i < 0:
            s_i = texto.find(S)
            if s_i >= 0:
                problemas.append("posicao_fora_de_ordem")
        c_ini = s_i + len(S) if s_i >= 0 else cursor
        c_i = texto.find(C, c_ini) if C else -1
        if C and c_i < 0:
            c_i = texto.find(C)
            if c_i >= 0:
                problemas.append("posicao_fora_de_ordem")
        g_i = -1
        if Gf:
            g_i = texto.find(Gf, s_i if s_i >= 0 else cursor)
            if g_i < 0:
                g_i = texto.find(Gf)
        if (S and s_i < 0) or (C and c_i < 0) or (Gf and g_i < 0):
            problemas.append("nao_literal")
        elidido = bool(r.get("G_elidido"))
        if elidido and Gf:
            problemas.append("elipse_inconsistente")
        if not elidido and not Gf:
            problemas.append("elipse_inconsistente")
        ramos.append({
            "S": S, "C": C, "G_elidido": elidido, "G_forma": Gf,
            "S_referente": r.get("S_referente"), "C_funcao": r.get("C_funcao"),
            "S_pos": [s_i, s_i + len(S)] if s_i >= 0 else None,
            "C_pos": [c_i, c_i + len(C)] if c_i >= 0 else None,
            "G_pos": [g_i, g_i + len(Gf)] if g_i >= 0 else None,
        })
        cursor = max([cursor] + [p[1] for p in (ramos[-1]["S_pos"], ramos[-1]["C_pos"], ramos[-1]["G_pos"]) if p])
    G = e.get("G") or ""
    g_pos = next((r["G_pos"] for r in ramos if r["G_pos"]), None)
    if g_pos is None and G:
        i = texto.find(G)
        g_pos = [i, i + len(G)] if i >= 0 else None
        if g_pos is None:
            problemas.append("nao_literal")
    return ramos, g_pos, sorted(set(problemas))


def _kwic(texto, pos):
    if not pos:
        return texto[:CONTEXTO], "", texto[CONTEXTO:2 * CONTEXTO]
    i, f = pos
    esq = texto[max(0, i - CONTEXTO):i]
    dir_ = texto[f:f + CONTEXTO]
    return ("…" if i > CONTEXTO else "") + esq, texto[i:f], dir_ + ("…" if f + CONTEXTO < len(texto) else "")


def _estruturas(modelo, caminho, paragrafos):
    """Valida e posiciona as estruturas de um modelo."""
    validas, auditoria = [], {"estruturas_brutas": 0, "nao_literais_descartadas": 0,
                              "elipse_inconsistente": 0, "posicao_fora_de_ordem": 0,
                              "blocos_sem_resposta": 0}
    sem_resposta = set()
    for ok, r in _ler(caminho):
        if not ok:
            auditoria["blocos_sem_resposta"] += 1
            sem_resposta.update(r.get("paragrafos", []))
            continue
        for e in (r.get("anotacao") or {}).get("estruturas", []):
            auditoria["estruturas_brutas"] += 1
            pid = e.get("paragrafo_id")
            if pid not in paragrafos:
                auditoria["nao_literais_descartadas"] += 1
                continue
            texto = paragrafos[pid]["texto"]
            ramos, g_pos, problemas = _localizar(texto, e)
            if "nao_literal" in problemas:
                auditoria["nao_literais_descartadas"] += 1
                continue
            for p in ("elipse_inconsistente", "posicao_fora_de_ordem"):
                if p in problemas:
                    auditoria[p] += 1
            esq, chave, dir_ = _kwic(texto, g_pos)
            validas.append({
                "id": f"{modelo}-{len(validas) + 1:03d}", "modelo": modelo,
                "paragrafo_id": pid, "categoria": e.get("categoria") or "nuclear",
                "G": e.get("G") or "", "G_lema": e.get("G_lema") or "", "G_pos": g_pos,
                "ramos": ramos, "confianca": e.get("confianca"),
                "justificativa": e.get("justificativa"), "alertas": [p for p in problemas],
                "esquerda": esq, "chave": chave, "direita": dir_,
            })
    return validas, auditoria, sem_resposta


# ------------------------------------------------------------- casamento

def _sim_ramo(r1, r2):
    s = _jac_pos(r1["S_pos"], r2["S_pos"]) if r1["S_pos"] and r2["S_pos"] else _jac_tokens(r1["S"], r2["S"])
    c = _jac_pos(r1["C_pos"], r2["C_pos"]) if r1["C_pos"] and r2["C_pos"] else _jac_tokens(r1["C"], r2["C"])
    return (s + c) / 2


def _casar_ramos(e1, e2):
    r1, r2 = e1["ramos"], e2["ramos"]
    if not r1 or not r2:
        return 0.0, []
    m = np.array([[_sim_ramo(a, b) for b in r2] for a in r1])
    li, co = linear_sum_assignment(-m)
    mapa = [[int(i), int(j), round(float(m[i, j]), 3)] for i, j in zip(li, co) if m[i, j] >= LIMIAR_RAMO]
    return len(mapa) / max(len(r1), len(r2)), mapa


def _sim_G(e1, e2):
    l1, l2 = _tokens(e1["G_lema"]), _tokens(e2["G_lema"])
    if l1 and l1 == l2:
        return 1.0
    return _jac_tokens(e1["G"], e2["G"])


def _casar(estr_a, estr_b):
    """Casamento bipartido ótimo por parágrafo. Devolve lista de pares com detalhes."""
    pares = []
    pids = {e["paragrafo_id"] for e in estr_a} & {e["paragrafo_id"] for e in estr_b}
    for pid in sorted(pids):
        A = [e for e in estr_a if e["paragrafo_id"] == pid]
        B = [e for e in estr_b if e["paragrafo_id"] == pid]
        score = np.zeros((len(A), len(B)))
        info = {}
        for i, a in enumerate(A):
            for j, b in enumerate(B):
                g = _sim_G(a, b)
                prop, mapa = _casar_ramos(a, b)
                if g >= LIMIAR_G and prop >= LIMIAR_RAMOS:
                    score[i, j] = 0.4 * g + 0.6 * prop
                    info[(i, j)] = (round(float(score[i, j]), 3), mapa)
        li, co = linear_sum_assignment(-score)
        for i, j in zip(li, co):
            if score[i, j] > 0:
                s, mapa = info[(i, j)]
                pares.append((A[i], B[j], s, mapa))
    return pares


# ------------------------------------------------------------------ main

def main():
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    paragrafos, sermoes = {}, []
    for s in corpus:
        titulo = s["titulo"].split("/")[-1]
        sermoes.append({"pageid": s["pageid"], "titulo": titulo, "url": s["url"],
                        "revid": s["revid"], "n_paragrafos": len(s["paragrafos"])})
        for n, p in enumerate(s["paragrafos"], 1):
            # Resíduo de estilo do Wikisource (último parágrafo do Mandato): removido
            # só na exibição; o corpus v1 fica intacto como fonte das anotações.
            texto = CSS_WIKISOURCE.sub("", p["texto"]).strip()
            paragrafos[p["id"]] = {"texto": texto, "sermao": titulo, "n": n, "url": s["url"]}

    estr, auditoria, sem_resposta = {}, {}, set()
    for m, caminho in ANOTACOES.items():
        estr[m], auditoria[m], sr = _estruturas(m, caminho, paragrafos)
        sem_resposta |= sr

    base, outro = "claude", "gemini"
    cob = lambda es: [e for e in es if e["paragrafo_id"] not in sem_resposta]
    pares = _casar(cob(estr[base]), cob(estr[outro]))
    casados_a = {id(a): (b, s, mp) for a, b, s, mp in pares}
    casados_b = {id(b) for _, b, _, _ in pares}

    ocorrencias = []

    def nova(anots, status, score=None, mapa=None):
        prim = anots.get(base) or anots.get(outro)
        p = paragrafos[prim["paragrafo_id"]]
        ocorrencias.append({
            "id": f"oc{len(ocorrencias) + 1:04d}", "paragrafo_id": prim["paragrafo_id"],
            "sermao": p["sermao"], "paragrafo": p["n"], "fonte": p["url"],
            "modelos": [m for m in (base, outro) if m in anots],
            "status": status, "match_score": score, "branch_mapping": mapa or [],
            "anotacoes": anots, "validacao": "nao_validado",
            "cobertura_completa": prim["paragrafo_id"] not in sem_resposta,
        })

    for a in estr[base]:
        if id(a) in casados_a:
            b, s, mp = casados_a[id(a)]
            nova({base: a, outro: b}, "concordante", s, mp)
        else:
            nova({base: a}, "so_" + base if a["paragrafo_id"] not in sem_resposta else "sem_resposta")
    for b in estr[outro]:
        if id(b) not in casados_b:
            nova({outro: b}, "so_" + outro if b["paragrafo_id"] not in sem_resposta else "sem_resposta")
    ocorrencias.sort(key=lambda o: (o["sermao"], o["paragrafo"],
                                    (o["anotacoes"].get(base) or o["anotacoes"][outro])["G_pos"] or [0])[0])
    for i, o in enumerate(ocorrencias, 1):
        o["id"] = f"oc{i:04d}"

    n_a, n_b, comuns = len(cob(estr[base])), len(cob(estr[outro])), len(pares)
    pa, pb = comuns / n_a, comuns / n_b
    mesma_cat = sum(1 for a, b, _, _ in pares if a["categoria"] == b["categoria"])

    def conf(m, concordante):
        alvo = [o["anotacoes"][m]["confianca"] for o in ocorrencias
                if m in o["anotacoes"] and o["cobertura_completa"]
                and (o["status"] == "concordante") == concordante
                and isinstance(o["anotacoes"][m]["confianca"], (int, float))]
        return round(sum(alvo) / len(alvo), 2) if alvo else None

    governanca = {
        "manual": "v3",
        "criterio_casamento": (f"bipartido ótimo por parágrafo (algoritmo húngaro); G semelhante "
                               f"(lema igual ou Jaccard ≥ {LIMIAR_G}) e ≥ {int(LIMIAR_RAMOS * 100)}% dos ramos "
                               f"casados por sobreposição de posição ≥ {LIMIAR_RAMO}"),
        "modelos": {m: {"nome": NOMES[m], "estruturas": len(estr[m]), **auditoria[m],
                        "confianca_media_concordantes": conf(m, True),
                        "confianca_media_isoladas": conf(m, False)} for m in ANOTACOES},
        "concordantes": comuns,
        "confirmadas_claude": round(pa, 3), "confirmadas_gemini": round(pb, 3),
        "f1": round(2 * pa * pb / (pa + pb), 3) if pa + pb else 0.0,
        "mesma_categoria": mesma_cat,
        "paragrafos_sem_resposta": sorted(sem_resposta),
        "base_da_concordancia": f"{len(paragrafos) - len(sem_resposta)} de {len(paragrafos)} parágrafos processados pelos dois modelos",
    }

    for s in sermoes:
        pids = [k for k, v in paragrafos.items() if v["sermao"] == s["titulo"]]
        s["palavras"] = sum(len(re.findall(r"\w+", paragrafos[k]["texto"])) for k in pids)
        s["paragrafos_com_ocorrencia"] = len({o["paragrafo_id"] for o in ocorrencias if o["sermao"] == s["titulo"]})

    with CORRESP.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["candidate_id", "paragraph_id", "claude_id", "gemini_id", "match_status",
                    "match_score", "branch_mapping", "categoria_claude", "categoria_gemini",
                    "G_claude", "G_gemini"])
        for o in ocorrencias:
            a, b = o["anotacoes"].get(base), o["anotacoes"].get(outro)
            w.writerow([o["id"], o["paragrafo_id"], a["id"] if a else "", b["id"] if b else "",
                        o["status"], "" if o["match_score"] is None else o["match_score"],
                        json.dumps(o["branch_mapping"]), a["categoria"] if a else "",
                        b["categoria"] if b else "", a["G"] if a else "", b["G"] if b else ""])

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps({
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "edicao": "Sermões do padre Antonio Vieira. Lisboa: J.M.C. Seabra e T.Q. Antunes, 1855 (Wikisource, domínio público)",
        "sermoes": sermoes, "ocorrencias": ocorrencias, "governanca": governanca,
        "paragrafos": {k: v["texto"] for k, v in paragrafos.items()},
    }, ensure_ascii=False), encoding="utf-8")
    print(f"{len(ocorrencias)} ocorrências ({comuns} concordantes) -> {SAIDA.relative_to(RAIZ)}")
    for m in ANOTACOES:
        print(m, auditoria[m])


if __name__ == "__main__":
    main()
