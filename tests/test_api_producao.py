"""Em produção (sem PANVIEIRA_API_EXPERIMENTAL) só a plataforma fica exposta."""
import importlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient


def _app(**env):
    antigo = {k: os.environ.get(k) for k in ("PANVIEIRA_API_EXPERIMENTAL", "PANVIEIRA_ORIGIN_SECRET")}
    for k in antigo:
        os.environ.pop(k, None)
    os.environ.update(env)
    try:
        import semiomorfologia.api.app as modulo
        return importlib.reload(modulo).app
    finally:
        for k, v in antigo.items():
            os.environ.pop(k, None)
            if v is not None:
                os.environ[k] = v


def test_rotas_experimentais_ficam_fora_em_producao():
    c = TestClient(_app())
    assert c.get("/").status_code == 200
    assert c.get("/api/status").status_code == 200
    assert c.get("/static/dados/concordancia.json").status_code == 200
    for rota in ("/api/extract", "/api/contract", "/api/fame", "/api/fame/batch",
                 "/api/bridges", "/api/knowledge/enrich"):
        assert c.post(rota, json={}).status_code in (404, 405), rota
    assert c.get("/docs").status_code == 404
    assert c.get("/openapi.json").status_code == 404


def test_segredo_de_origem_bloqueia_acesso_direto():
    c = TestClient(_app(PANVIEIRA_ORIGIN_SECRET="valor-de-teste"))
    assert c.get("/").status_code == 403
    assert c.get("/", headers={"x-panvieira-origin": "errado"}).status_code == 403
    assert c.get("/", headers={"x-panvieira-origin": "valor-de-teste"}).status_code == 200
