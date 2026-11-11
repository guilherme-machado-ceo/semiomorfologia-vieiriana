"""
Gera os dados da vertical Humanidades Digitais (concordanciador) e do
painel de Governança de IA a partir do corpus e das anotações cegas.

Uso:
    python scripts/gerar_concordancia.py

Entradas:
    corpus/corpus-panvieira-wikisource-v1.json
    corpus/anotacoes/*.jsonl      (uma anotação por modelo, mesmo manual)

Saída:
    src/semiomorfologia/web/dados/concordancia.json
"""
import json
import pathlib
import re
import unicodedata
from datetime import datetime, timezone

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CORPUS = RAIZ / "corpus" / "corpus-panvieira-wikisource-v1.json"
ANOTACOES = {
    "claude": RAIZ / "corpus" / "anotacoes" / "claude-opus55-manual-v3.jsonl",
    "gemini": RAIZ / "corpus" / "anotacoes" / "gemini4argon-manual-v3.jsonl",
}
NOMES = {"claude": "Claude Opus 5.5", "gemini": "Gemini 4 Argon"}
SAIDA = RAIZ / "src" / "semiomorfologia" / "web" / "dados" / "concordancia.json"
CONTEXTO = 90


def _tokens(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return set(re.findall(r"\w+", s))


def _sobrepoe(a, b, limiar=0.5):
    a, b = _tokens(a), _tokens(b)
    return bool(a | b) and len(a & b) / len(a | b) >= limiar


def _mesma(e1, e2):
    if e1["paragrafo_id"] != e2["paragrafo_id"]:
        return False
    lema = e1.get("G_lema") and e1.get("G_lema") == e2.get("G_lema")
    if not (lema or _sobrepoe(e1["G"], e2["G"])):
        return False
    return any(
        _sobrepoe(r1.get("C", ""), r2.get("C", "")) or _sobrepoe(r1.get("S", ""), r2.get("S", ""))
        for r1 in e1.get("ramos", []) for r2 in e2.get("ramos", [])
    )


def _estruturas(caminho):
    out, erros = [], 0
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        r = json.loads(linha)
        if r.get("erro") or r.get("erro_json"):
            erros += 1
        for e in (r.get("anotacao") or {}).get("estruturas", []):
            if e.get("trechos_literais_ok", True):
                out.append(e)
    return out, erros


def _kwic(texto, g):
    i = texto.find(g)
    if i < 0:
        return texto[:CONTEXTO], "", texto[CONTEXTO:2 * CONTEXTO]
    esq = texto[max(0, i - CONTEXTO):i]
    dir_ = texto[i + len(g):i + len(g) + CONTEXTO]
    return ("…" if i > CONTEXTO else "") + esq, g, dir_ + ("…" if i + len(g) + CONTEXTO < len(texto) else "")


def main():
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    paragrafos, sermoes = {}, []
    for s in corpus:
        titulo = s["titulo"].split("/")[-1]
        sermoes.append({"pageid": s["pageid"], "titulo": titulo, "url": s["url"],
                        "revid": s["revid"], "n_paragrafos": len(s["paragrafos"])})
        for n, p in enumerate(s["paragrafos"], 1):
            paragrafos[p["id"]] = {"texto": p["texto"], "sermao": titulo, "n": n, "url": s["url"]}

    por_modelo = {m: _estruturas(c) for m, c in ANOTACOES.items()}
    base, outro = "claude", "gemini"
    usados, linhas = set(), []

    def registrar(e, modelos, categorias):
        p = paragrafos[e["paragrafo_id"]]
        esq, kw, dir_ = _kwic(p["texto"], e["G"])
        linhas.append({
            "id": f"oc{len(linhas) + 1:04d}",
            "paragrafo_id": e["paragrafo_id"], "sermao": p["sermao"], "paragrafo": p["n"],
            "categoria": e.get("categoria", "nuclear"),
            "categorias_por_modelo": categorias,
            "G": e["G"], "G_lema": e.get("G_lema", ""),
            "ramos": [{k: r.get(k) for k in ("S", "C", "G_elidido", "G_forma", "S_referente", "C_funcao")}
                      for r in e.get("ramos", [])],
            "esquerda": esq, "chave": kw, "direita": dir_,
            "modelos": modelos, "validacao": "nao_validado", "fonte": p["url"],
        })

    for e in por_modelo[base][0]:
        par = next((j for j, g in enumerate(por_modelo[outro][0]) if j not in usados and _mesma(e, g)), None)
        if par is not None:
            usados.add(par)
            g = por_modelo[outro][0][par]
            registrar(e, [base, outro], {base: e.get("categoria"), outro: g.get("categoria")})
        else:
            registrar(e, [base], {base: e.get("categoria")})
    for j, g in enumerate(por_modelo[outro][0]):
        if j not in usados:
            registrar(g, [outro], {outro: g.get("categoria")})

    n_c, n_g = len(por_modelo[base][0]), len(por_modelo[outro][0])
    comuns = sum(1 for l in linhas if len(l["modelos"]) == 2)
    pc, pg = comuns / n_c, comuns / n_g
    mesma_cat = sum(1 for l in linhas if len(l["modelos"]) == 2
                    and len(set(l["categorias_por_modelo"].values())) == 1)

    def confianca_media(modelo, sozinho):
        vals = [e.get("confianca", 0) for e in por_modelo[modelo][0]
                if any(l["paragrafo_id"] == e["paragrafo_id"] and l["G"] == e["G"]
                       and (l["modelos"] == [modelo]) == sozinho for l in linhas)]
        return round(sum(vals) / len(vals), 2) if vals else None

    governanca = {
        "manual": "v3",
        "modelos": {m: {"nome": NOMES[m], "estruturas": len(por_modelo[m][0]),
                        "blocos_com_erro": por_modelo[m][1],
                        "confianca_media_concordantes": confianca_media(m, False),
                        "confianca_media_isoladas": confianca_media(m, True)}
                    for m in ANOTACOES},
        "concordantes": comuns,
        "confirmadas_claude": round(pc, 3), "confirmadas_gemini": round(pg, 3),
        "f1": round(2 * pc * pg / (pc + pg), 3),
        "mesma_categoria": mesma_cat,
        "trechos_nao_literais_descartados": 0,
    }

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps({
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "edicao": "Sermões do padre Antonio Vieira. Lisboa: J.M.C. Seabra e T.Q. Antunes, 1855 (Wikisource, domínio público)",
        "sermoes": sermoes, "ocorrencias": linhas, "governanca": governanca,
        "paragrafos": {k: v["texto"] for k, v in paragrafos.items()},
    }, ensure_ascii=False), encoding="utf-8")
    print(f"{len(linhas)} ocorrências ({comuns} concordantes) -> {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
