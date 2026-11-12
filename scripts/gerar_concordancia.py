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
- Posições: cada ramo é ancorado na janela contígua mais compacta que
  contém S, C e G_forma como palavras inteiras; as janelas dos ramos são
  escolhidas em conjunto, na ordem do texto (ex.: "Outra parte… Outra
  parte" ficam em lugares distintos; "é" não casa dentro de "prégador").
- Triagem: estruturas que o próprio anotador marcou com confiança zero,
  com menos de dois ramos ou com trecho não literal são descartadas e
  contadas na auditoria; as demais inconsistências viram alertas.
- Casamento entre anotadores: bipartido ótimo (algoritmo húngaro) por
  parágrafo, com mapeamento ótimo entre ramos; nada é guloso.
- As anotações dos dois modelos são preservadas integralmente, inclusive
  quando concordam.
"""
import csv
import hashlib
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
EDICOES = {239684: "Sermões do padre Antonio Vieira. Lisboa: J.M.C. Seabra e T.Q. Antunes, 1855"}
NOMES = {"claude": "Claude Opus 5.5", "gemini": "Gemini 4 Argon"}
SAIDA = RAIZ / "src" / "semiomorfologia" / "web" / "dados" / "concordancia.json"
CORRESP = RAIZ / "corpus" / "anotacoes" / "correspondencia-v3.csv"
CONTEXTO = 90
LIMIAR_G = 0.5        # semelhança mínima de G (lema igual conta 1,0)
LIMIAR_RAMOS = 0.5    # proporção mínima de ramos casados (pelo maior número de ramos)
LIMIAR_RAMO = 0.3     # sobreposição mínima (Jaccard de caracteres) para casar um ramo
MAX_JANELAS = 12       # candidatas de posição guardadas por ramo
MAX_RAMO = 400         # extensão (caracteres) acima da qual um ramo é sinalizado como disperso
LIMIAR_PASSAGEM = 0.5  # sobreposição mínima das extensões para "mesma passagem"
ALERTAS = ("elipse_inconsistente", "posicao_fora_de_ordem", "ramo_disperso", "ramo_incompleto",
           "trechos_sobrepostos", "sem_G_explicito", "G_difere_do_texto")
MIN_RAMOS_CASADOS = 2  # pluralidade: um par só concorda se preservar pelo menos dois ramos
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


def _ocorrencias(texto, cadeia):
    """Todas as ocorrências da cadeia com fronteira de palavra: [(ini, fim)].

    "é" não casa dentro de "prégador"; "ha" não casa dentro de "haver".
    """
    if not cadeia:
        return []
    achados, i = [], texto.find(cadeia)
    while i >= 0:
        f = i + len(cadeia)
        antes = i > 0 and texto[i - 1].isalnum() and cadeia[0].isalnum()
        depois = f < len(texto) and texto[f].isalnum() and cadeia[-1].isalnum()
        if not (antes or depois):
            achados.append((i, f))
        i = texto.find(cadeia, i + 1)
    return achados


def _janelas(texto, S, C, Gf):
    """Candidatas de um ramo: combinações de S, C e G_forma, da mais compacta à menos.

    A ordem interna é livre (sujeito–verbo ou verbo–sujeito); os trechos de um
    mesmo ramo não se sobrepõem. Devolve [(ini, fim, S_pos, C_pos, G_pos)] ou None
    se algum trecho não existe no texto como palavra inteira.
    """
    partes = [(n, _ocorrencias(texto, c)) for n, c in (("S", S), ("C", C), ("G", Gf)) if c]
    if not partes or any(not occ for _, occ in partes):
        return None
    def combinar(sem_sobreposicao):
        combos = [{}]
        for n, occ in partes:
            combos = [{**c, n: o} for c in combos for o in occ
                      if not sem_sobreposicao or all(o[1] <= x[0] or o[0] >= x[1] for x in c.values())]
            combos.sort(key=lambda c: max(x[1] for x in c.values()) - min(x[0] for x in c.values()))
            combos = combos[:MAX_JANELAS * 4]
        return combos

    # Se o anotador delimitou trechos que se sobrepõem (S contido em C, por exemplo),
    # aceita-se a sobreposição; _localizar sinaliza o caso.
    combos = combinar(True) or combinar(False)
    jan = [(min(x[0] for x in c.values()), max(x[1] for x in c.values()),
            c.get("S"), c.get("C"), c.get("G")) for c in combos]
    jan.sort(key=lambda w: (w[1] - w[0], w[0]))
    return jan[:MAX_JANELAS] or None


def _localizar(texto, e):
    """Ancora cada ramo na janela contígua mais compacta que contém S, C e G_forma.

    As janelas dos ramos são escolhidas em conjunto (programação dinâmica), na
    ordem do texto, minimizando a extensão total da estrutura. Devolve
    (ramos com posições, posição de G, problemas).
    """
    problemas, dados, cands = [], [], []
    for r in e.get("ramos", []):
        S, C, Gf = (r.get("S") or "").strip(), (r.get("C") or "").strip(), _nulo(r.get("G_forma"))
        Gf = Gf.strip() if isinstance(Gf, str) else Gf
        elidido = bool(r.get("G_elidido"))
        if elidido == bool(Gf):
            problemas.append("elipse_inconsistente")
        if not S or not C:
            problemas.append("ramo_incompleto")
        jan = _janelas(texto, S, C, Gf)
        if jan is None:
            problemas.append("nao_literal")
            jan = []
        dados.append({"S": S, "C": C, "G_elidido": elidido, "G_forma": Gf,
                      "S_referente": r.get("S_referente"), "C_funcao": r.get("C_funcao")})
        cands.append(jan)

    escolha = [None] * len(cands)
    if cands and all(cands):
        FORA = 10 ** 6  # custo de voltar no texto: só se não houver caminho em ordem
        custo = [[w[1] - w[0] for w in cands[0]]]
        veio = [[None] * len(cands[0])]
        for i in range(1, len(cands)):
            linha, de = [], []
            for w in cands[i]:
                melhor, k_m = None, None
                for k, v in enumerate(cands[i - 1]):
                    em_ordem = w[0] >= v[0] and (w[0], w[1]) != (v[0], v[1])
                    passo = max(0, w[0] - v[1]) if em_ordem else FORA + abs(w[0] - v[0])
                    c = custo[i - 1][k] + passo
                    if melhor is None or c < melhor:
                        melhor, k_m = c, k
                linha.append(melhor + (w[1] - w[0]))
                de.append(k_m)
            custo.append(linha)
            veio.append(de)
        j = min(range(len(custo[-1])), key=lambda k: custo[-1][k])
        if custo[-1][j] >= FORA:
            problemas.append("posicao_fora_de_ordem")
        for i in range(len(cands) - 1, -1, -1):
            escolha[i] = cands[i][j]
            j = veio[i][j]

    ramos = []
    for d, w in zip(dados, escolha):
        ramos.append({**d, "S_pos": list(w[2]) if w and w[2] else None,
                      "C_pos": list(w[3]) if w and w[3] else None,
                      "G_pos": list(w[4]) if w and w[4] else None})
        if w and w[1] - w[0] > MAX_RAMO:
            problemas.append("ramo_disperso")
        tr = sorted(p for p in (ramos[-1]["S_pos"], ramos[-1]["C_pos"], ramos[-1]["G_pos"]) if p)
        if any(x[1] > y[0] for x, y in zip(tr, tr[1:])):
            problemas.append("trechos_sobrepostos")

    G = (e.get("G") or "").strip()
    g_pos = next((r["G_pos"] for r in ramos if r["G_pos"]), None)
    if g_pos is None and G:
        # G só aparece fora dos ramos (antecedente): a ocorrência mais próxima da estrutura
        ini = min((p[0] for r in ramos for p in (r["S_pos"], r["C_pos"]) if p), default=0)
        occ = _ocorrencias(texto, G)
        if occ:
            g_pos = list(min(occ, key=lambda o: abs(o[0] - ini)))
        else:
            problemas.append("nao_literal")
    if not any(r["G_forma"] for r in ramos):
        problemas.append("sem_G_explicito")
    if g_pos and G and texto[g_pos[0]:g_pos[1]].lower() != G.lower():
        problemas.append("G_difere_do_texto")
    return ramos, g_pos, sorted(set(problemas))


def _extensao(e):
    """Intervalo [ini, fim) que cobre todos os trechos localizados da estrutura."""
    pos = [p for r in e["ramos"] for p in (r["S_pos"], r["C_pos"], r["G_pos"]) if p]
    return [min(p[0] for p in pos), max(p[1] for p in pos)] if pos else None


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
                              "paragrafo_desconhecido": 0, "rejeitadas_pelo_anotador": 0,
                              "menos_de_dois_ramos": 0, "com_alerta": 0,
                              **{a: 0 for a in ALERTAS}, "blocos_sem_resposta": 0}
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
                auditoria["paragrafo_desconhecido"] += 1
                continue
            conf = e.get("confianca")
            if isinstance(conf, (int, float)) and not isinstance(conf, bool) and conf <= 0:
                # o próprio anotador declarou confiança zero (falso positivo descartado)
                auditoria["rejeitadas_pelo_anotador"] += 1
                continue
            if len(e.get("ramos") or []) < 2:
                auditoria["menos_de_dois_ramos"] += 1
                continue
            texto = paragrafos[pid]["texto"]
            ramos, g_pos, problemas = _localizar(texto, e)
            if "nao_literal" in problemas:
                auditoria["nao_literais_descartadas"] += 1
                continue
            for p in ALERTAS:
                if p in problemas:
                    auditoria[p] += 1
            auditoria["com_alerta"] += bool(problemas)
            esq, chave, dir_ = _kwic(texto, g_pos)
            validas.append({
                "id": f"{modelo}-{len(validas) + 1:03d}", "modelo": modelo,
                "paragrafo_id": pid,
                "categoria": e.get("categoria") if e.get("categoria") in ("nuclear", "expandido") else "expandido",
                "G": e.get("G") or "", "G_lema": e.get("G_lema") or "", "G_pos": g_pos,
                "ramos": ramos,
                "confianca": conf if isinstance(conf, (int, float)) and not isinstance(conf, bool) else None,
                "justificativa": e.get("justificativa"), "alertas": [p for p in problemas],
                "esquerda": esq, "chave": chave, "direita": dir_,
            })
            validas[-1]["extensao"] = _extensao(validas[-1])
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
    if len(mapa) < MIN_RAMOS_CASADOS:
        return 0.0, []
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
        fonte = f"https://pt.wikisource.org/w/index.php?oldid={s['revid']}"  # revisão exata coletada
        sermoes.append({"pageid": s["pageid"], "titulo": titulo, "url": fonte, "pagina": s["url"],
                        "revid": s["revid"], "obtido_em": s.get("obtido_em"), "sha256": s.get("sha256"),
                        "edicao": EDICOES.get(s["pageid"], "edição-fonte da transcrição do Wikisource a conferir"),
                        "n_paragrafos": len(s["paragrafos"])})
        for n, p in enumerate(s["paragrafos"], 1):
            # Resíduo de estilo do Wikisource (último parágrafo do Mandato): removido
            # só na exibição; o corpus v1 fica intacto como fonte das anotações.
            texto = CSS_WIKISOURCE.sub("", p["texto"]).strip()
            paragrafos[p["id"]] = {"texto": texto, "sermao": titulo, "n": n, "url": fonte,
                                   "ordem": len(sermoes)}

    estr, auditoria, sem_resposta = {}, {}, set()
    for m, caminho in ANOTACOES.items():
        estr[m], auditoria[m], sr = _estruturas(m, caminho, paragrafos)
        sem_resposta |= sr

    base, outro = "claude", "gemini"
    cob = lambda es: [e for e in es if e["paragrafo_id"] not in sem_resposta]
    pares = _casar(cob(estr[base]), cob(estr[outro]))
    casados_a = {id(a): (b, s, mp) for a, b, s, mp in pares}
    casados_b = {id(b) for _, b, _, _ in pares}

    # Segunda passada: estruturas não casadas que recobrem a mesma passagem
    # (extensões sobrepostas), mas com delimitação divergente de G, S ou C.
    passagem_a, passagem_b = {}, set()
    for pid in sorted({e["paragrafo_id"] for e in cob(estr[base])}):
        A = [e for e in cob(estr[base]) if e["paragrafo_id"] == pid and id(e) not in casados_a and e["extensao"]]
        B = [e for e in cob(estr[outro]) if e["paragrafo_id"] == pid and id(e) not in casados_b and e["extensao"]]
        if not A or not B:
            continue
        m = np.array([[_jac_pos(a["extensao"], b["extensao"]) for b in B] for a in A])
        for i, j in zip(*linear_sum_assignment(-m)):
            if m[i, j] >= LIMIAR_PASSAGEM:
                passagem_a[id(A[i])] = (B[j], round(float(m[i, j]), 3))
                passagem_b.add(id(B[j]))

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
        elif id(a) in passagem_a:
            b, s = passagem_a[id(a)]
            nova({base: a, outro: b}, "mesma_passagem", s)
        else:
            nova({base: a}, "so_" + base if a["paragrafo_id"] not in sem_resposta else "sem_resposta")
    for b in estr[outro]:
        if id(b) not in casados_b and id(b) not in passagem_b:
            nova({outro: b}, "so_" + outro if b["paragrafo_id"] not in sem_resposta else "sem_resposta")
    def ordem(o):
        prim = o["anotacoes"].get(base) or o["anotacoes"][outro]
        return (paragrafos[o["paragrafo_id"]]["ordem"], o["paragrafo"], (prim["extensao"] or [0])[0])

    ocorrencias.sort(key=ordem)
    for i, o in enumerate(ocorrencias, 1):
        o["id"] = f"oc{i:04d}"

    n_a, n_b, comuns = len(cob(estr[base])), len(cob(estr[outro])), len(pares)
    pa, pb = (comuns / n_a if n_a else 0.0), (comuns / n_b if n_b else 0.0)
    n_pass = len(passagem_a)
    ra, rb = ((comuns + n_pass) / n_a if n_a else 0.0), ((comuns + n_pass) / n_b if n_b else 0.0)
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
                               f"casados, com no mínimo {MIN_RAMOS_CASADOS}, por sobreposição de posição ≥ {LIMIAR_RAMO}"),
        "modelos": {m: {"nome": NOMES[m], "estruturas": len(estr[m]), **auditoria[m],
                        "confianca_media_concordantes": conf(m, True),
                        "confianca_media_isoladas": conf(m, False)} for m in ANOTACOES},
        "concordantes": comuns,
        "confirmadas_claude": round(pa, 3), "confirmadas_gemini": round(pb, 3),
        "f1": round(2 * pa * pb / (pa + pb), 3) if pa + pb else 0.0,
        "mesma_categoria": mesma_cat,
        "mesma_passagem": n_pass,
        "criterio_mesma_passagem": (f"estruturas não casadas cujas extensões no parágrafo se sobrepõem "
                                    f"(Jaccard ≥ {LIMIAR_PASSAGEM}), com G, S ou C delimitados de modo diferente"),
        "f1_por_passagem": round(2 * ra * rb / (ra + rb), 3) if ra + rb else 0.0,
        "validadas_por_humano": 0,
        "entradas_sha256": {c.name: hashlib.sha256(c.read_bytes()).hexdigest()
                            for c in [CORPUS, *ANOTACOES.values()]},
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
        "edicao": "Transcrições do Wikisource em português (domínio público); edição-fonte indicada por sermão",
        "sermoes": sermoes, "ocorrencias": ocorrencias, "governanca": governanca,
        "paragrafos": {k: v["texto"] for k, v in paragrafos.items()},
    }, ensure_ascii=False), encoding="utf-8")
    print(f"{len(ocorrencias)} ocorrências ({comuns} concordantes, {n_pass} mesma passagem) -> {SAIDA.relative_to(RAIZ)}")
    for m in ANOTACOES:
        print(m, auditoria[m])


if __name__ == "__main__":
    main()
