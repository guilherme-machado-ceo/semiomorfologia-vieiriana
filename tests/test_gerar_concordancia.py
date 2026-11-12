"""Testes do gerador de dados do concordanciador (scripts/gerar_concordancia.py)."""
import importlib.util
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gerar", RAIZ / "scripts" / "gerar_concordancia.py")
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

DADOS = RAIZ / "src" / "semiomorfologia" / "web" / "dados" / "concordancia.json"


def _ramo(S, C, Gf=None, elidido=False):
    return {"S": S, "C": C, "G_forma": Gf, "G_elidido": elidido}


def test_nulo_normaliza_texto_null():
    assert G._nulo("null") is None and G._nulo("None") is None and G._nulo("") is None
    assert G._nulo("caiu") == "caiu"


def test_posicoes_distinguem_repeticao_literal_de_S():
    texto = "Uma parte caiu entre espinhos. Outra parte caiu sobre pedras. Outra parte caiu no caminho."
    e = {"G": "caiu", "ramos": [_ramo("Uma parte", "entre espinhos", "caiu"),
                                _ramo("Outra parte", "sobre pedras", "caiu"),
                                _ramo("Outra parte", "no caminho", "caiu")]}
    ramos, g_pos, problemas = G._localizar(texto, e)
    assert problemas == []
    s2, s3 = ramos[1]["S_pos"], ramos[2]["S_pos"]
    assert s2 != s3 and texto[s3[0]:s3[1]] == "Outra parte" and s3[0] > s2[0]
    assert texto[ramos[2]["G_pos"][0]:ramos[2]["G_pos"][1]] == "caiu" and ramos[2]["G_pos"][0] > s3[0]


def test_validacao_independente_detecta_nao_literal_e_elipse():
    texto = "A natureza insensivel o perseguiu nas pedras; a vegetativa, nos espinhos."
    inventado = {"G": "o perseguiu", "ramos": [_ramo("A natureza insensivel", "nos rios", "o perseguiu")]}
    assert "nao_literal" in G._localizar(texto, inventado)[2]
    contradicao = {"G": "o perseguiu", "ramos": [_ramo("a vegetativa", "nos espinhos", "null", elidido=False)]}
    assert "elipse_inconsistente" in G._localizar(texto, contradicao)[2]


def test_casamento_otimo_nao_e_guloso():
    texto = "o mar ferve no verão; o rio ferve no inverno. o mar gela no verão; o rio gela no inverno."

    def estr(gf, s1, c1, s2, c2):
        e = {"G": gf, "G_lema": "", "ramos": [_ramo(s1, c1, gf), _ramo(s2, c2, None, True)]}
        ramos, g_pos, _ = G._localizar(texto, e)
        return {**e, "paragrafo_id": "p", "ramos": ramos, "G_pos": g_pos}

    a1 = estr("ferve", "o mar", "no verão", "o rio", "no inverno")
    b_gela = estr("gela", "o mar", "no verão", "o rio", "no inverno")
    b_ferve = estr("ferve", "o mar", "no verão", "o rio", "no inverno")
    pares = G._casar([a1], [b_gela, b_ferve])
    assert len(pares) == 1 and pares[0][1]["G"] == "ferve"


def test_dados_preservam_as_duas_anotacoes():
    d = json.loads(DADOS.read_text(encoding="utf-8"))
    concordantes = [o for o in d["ocorrencias"] if o["status"] == "concordante"]
    assert concordantes
    for o in concordantes:
        assert set(o["anotacoes"]) == {"claude", "gemini"}
        assert o["anotacoes"]["claude"]["id"].startswith("claude-")
        assert o["anotacoes"]["gemini"]["id"].startswith("gemini-")
    ids_g = [o["anotacoes"]["gemini"]["id"] for o in d["ocorrencias"] if "gemini" in o["anotacoes"]]
    assert len(ids_g) == len(set(ids_g)), "cada estrutura do Gemini aparece uma única vez"


def test_um_unico_ramo_casado_nao_e_concordancia():
    texto = "Dá-me o pão do céu, e me dá a água da fonte; o vinho guardo eu."
    a = {"G": "Dá-me", "G_lema": "dar", "ramos": [_ramo("o pão", "do céu", "Dá-me"),
                                                  _ramo("o vinho", "guardo eu", None, True)]}
    b = {"G": "me dá", "G_lema": "dar", "ramos": [_ramo("o pão", "do céu", "Dá-me"),
                                                  _ramo("a água", "da fonte", "me dá")]}
    est = []
    for e in (a, b):
        ramos, g_pos, _ = G._localizar(texto, e)
        est.append({**e, "paragrafo_id": "p", "ramos": ramos, "G_pos": g_pos})
    prop, mapa = G._casar_ramos(est[0], est[1])
    assert prop == 0.0 and mapa == []
    assert G._casar([est[0]], [est[1]]) == []


def test_posicao_respeita_fronteira_de_palavra():
    texto = "Para o prégador ha de haver regra: o pulpito é theatro, e o sermão comedia."
    e = {"G": "é", "ramos": [_ramo("o pulpito", "theatro", "é"), _ramo("o sermão", "comedia", None, True)]}
    ramos, g_pos, problemas = G._localizar(texto, e)
    assert "nao_literal" not in problemas
    assert texto[g_pos[0]:g_pos[1]] == "é" and texto[g_pos[0] - 1] == " " and texto[g_pos[1]] == " "
    assert g_pos[0] > texto.index("pulpito")  # não é o "é" de "prégador"
    assert G._ocorrencias(texto, "ha") == [(16, 18)]  # não casa dentro de "haver"


def test_ramo_em_ordem_verbo_sujeito_fica_na_janela_compacta():
    texto = ("A esposa e o esposo deram cada um a sua prova. Deu a esposa a cithara; "
             "deu o esposo o véu.")
    e = {"G": "Deu", "ramos": [_ramo("a esposa", "a cithara", "Deu"), _ramo("o esposo", "o véu", "deu")]}
    ramos, g_pos, problemas = G._localizar(texto, e)
    assert problemas == []
    # o verbo vem antes do sujeito: G fica à esquerda de S, e S não é a primeira menção
    assert ramos[0]["G_pos"][0] < ramos[0]["S_pos"][0] < ramos[0]["C_pos"][0]
    assert ramos[1]["S_pos"][0] == texto.rindex("o esposo") and ramos[1]["G_pos"][0] == texto.rindex("deu")
    assert g_pos == ramos[0]["G_pos"]


def test_triagem_descarta_o_que_o_anotador_rejeitou(tmp_path):
    texto = "Uma parte caiu entre espinhos. Outra parte caiu sobre pedras."
    est = {"paragrafo_id": "p1", "categoria": "nuclear", "G": "caiu", "G_lema": "cair",
           "ramos": [_ramo("Uma parte", "entre espinhos", "caiu"), _ramo("Outra parte", "sobre pedras", "caiu")]}
    linhas = [{"revid": 1, "bloco": 1, "paragrafos": ["p1"], "erro": None,
               "anotacao": {"estruturas": [{**est, "confianca": 0.9}, {**est, "confianca": 0.0},
                                           {**est, "confianca": 0.8, "ramos": est["ramos"][:1]}]}}]
    arq = tmp_path / "a.jsonl"
    arq.write_text("\n".join(json.dumps(x) for x in linhas), encoding="utf-8")
    validas, aud, _ = G._estruturas("teste", arq, {"p1": {"texto": texto}})
    assert len(validas) == 1 and validas[0]["extensao"] == [0, len(texto) - 1]
    assert aud["rejeitadas_pelo_anotador"] == 1 and aud["menos_de_dois_ramos"] == 1


def test_dados_publicados_em_ordem_e_com_posicoes_exatas():
    d = json.loads(DADOS.read_text(encoding="utf-8"))
    ordem = [s["titulo"] for s in d["sermoes"]]
    chaves = []
    for o in d["ocorrencias"]:
        texto = d["paragrafos"][o["paragrafo_id"]]
        prim = o["anotacoes"].get("claude") or o["anotacoes"]["gemini"]
        chaves.append((ordem.index(o["sermao"]), o["paragrafo"], prim["extensao"][0]))
        for a in o["anotacoes"].values():
            assert a["confianca"] is None or a["confianca"] > 0
            for r in a["ramos"]:
                for campo, pos in (("S", r["S_pos"]), ("C", r["C_pos"]), ("G_forma", r["G_pos"])):
                    if pos:
                        assert texto[pos[0]:pos[1]] == r[campo]
                        dentro = (pos[0] > 0 and texto[pos[0] - 1].isalnum() and r[campo][0].isalnum()) or \
                                 (pos[1] < len(texto) and texto[pos[1]].isalnum() and r[campo][-1].isalnum())
                        assert not dentro, (a["id"], campo)
    assert chaves == sorted(chaves)
    assert {o["status"] for o in d["ocorrencias"]} <= {"concordante", "mesma_passagem", "so_claude", "so_gemini"}
