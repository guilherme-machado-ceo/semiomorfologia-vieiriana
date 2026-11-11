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
