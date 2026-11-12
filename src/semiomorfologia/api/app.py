import hmac
import os
import pathlib

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from semiomorfologia import __version__

# Em produção a plataforma serve só a interface, os dados e o status.
# As rotas experimentais do framework (extração, contrato, FAME, pontes,
# enriquecimento por serviços externos) não têm limites de tamanho nem de
# custo e por isso só são registradas com PANVIEIRA_API_EXPERIMENTAL=1
# (uso local e testes). A documentação interativa segue a mesma regra.
EXPERIMENTAL = os.environ.get("PANVIEIRA_API_EXPERIMENTAL") == "1"
# Se definido, toda requisição precisa trazer este valor no cabeçalho
# x-panvieira-origin (enviado pelo proxy); bloqueia o acesso direto à origem.
SEGREDO_ORIGEM = os.environ.get("PANVIEIRA_ORIGIN_SECRET") or ""

app = FastAPI(
    title="Semiomorfologia Vieiriana API",
    description="API REST para extracao de analogias semiomorfologicas",
    version=__version__,
    docs_url="/docs" if EXPERIMENTAL else None,
    redoc_url=None,
    openapi_url="/openapi.json" if EXPERIMENTAL else None,
)
experimental = APIRouter()

CABECALHOS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=31536000",
    # A página usa script e estilo embutidos; o restante fica restrito à própria origem.
    "Content-Security-Policy": ("default-src 'self'; script-src 'self' 'unsafe-inline'; "
                                "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"),
}


@app.middleware("http")
async def seguranca(request: Request, call_next):
    if SEGREDO_ORIGEM and not hmac.compare_digest(
            request.headers.get("x-panvieira-origin", ""), SEGREDO_ORIGEM):
        return JSONResponse({"detail": "acesso apenas pelo dominio publico"}, status_code=403)
    resposta = await call_next(request)
    for k, v in CABECALHOS.items():
        resposta.headers.setdefault(k, v)
    return resposta


class MorfemaInput(BaseModel):
    id: str
    dominio: str
    nivel: str = "molecular"
    descritores: Dict[str, Any] = {}
    propriedades: Dict[str, float] = {}


class ContratoInput(BaseModel):
    m1: Dict[str, Any]
    m2: Dict[str, Any]


class FAMEInput(BaseModel):
    pontuacao: float
    dimensoes: Optional[Dict[str, float]] = None


WEB = pathlib.Path(__file__).resolve().parents[1] / "web"
app.mount("/static", StaticFiles(directory=str(WEB)), name="static")


@app.get("/", include_in_schema=False)
def plataforma():
    """Interface da plataforma PANVIEIRA (verticais em abas)."""
    return FileResponse(WEB / "index.html")


@app.get("/api/status")
def status():
    return {"framework": "Semiomorfologia Vieiriana", "version": __version__, "status": "online"}


@experimental.get("/api/domains")
def list_domains():
    return {"domains": ["mineral", "vegetal", "animal", "humano"],
            "types": ["heuristica", "funcional", "homologica"]}


@experimental.post("/api/extract")
def extract_analogies(domain: str, morphemes: List[MorfemaInput]):
    try:
        from semiomorfologia.core.ontologia import (
            Morfema, DominioNatural, NivelOrganizacao
        )
        from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico

        motor = MotorSemiomorfologico()
        dominio = DominioNatural(domain.lower())
        corpus = [
            Morfema(
                m.id, dominio, NivelOrganizacao(m.nivel),
                m.descritores, m.propriedades
            )
            for m in morphemes
        ]
        resultados = motor.extrair_analogias_dominio(corpus, dominio)
        serializado = {}
        for tipo, analogias in resultados.items():
            serializado[tipo.value] = [a.serializar() for a in analogias]
        total = sum(len(v) for v in serializado.values())
        return {"domain": domain, "total": total, "analogies": serializado}
    except Exception:
        raise HTTPException(status_code=400, detail="entrada invalida")


@experimental.post("/api/contract")
def create_contract(data: ContratoInput):
    from semiomorfologia.similaridade.anti_unificacao import AntiUnificador
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    au = AntiUnificador()
    av = AvaliadorFAME()
    contrato = au.contrato(data.m1, data.m2)
    contrato["avaliacao_fame"] = av.avaliar_contrato(contrato)
    return contrato


@experimental.post("/api/fame")
def evaluate_fame(data: FAMEInput):
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    av = AvaliadorFAME()
    return av.avaliar(data.pontuacao, data.dimensoes)


@experimental.post("/api/fame/batch")
def evaluate_fame_batch(scores: List[float]):
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    av = AvaliadorFAME()
    return av.avaliar_conjunto(scores)


@experimental.post("/api/bridges")
def cross_domain_bridges(domains_data: Dict[str, List[MorfemaInput]]):
    from semiomorfologia.core.ontologia import (
        Morfema, DominioNatural, NivelOrganizacao
    )
    from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico

    motor = MotorSemiomorfologico()
    corpus = {}
    for d, morphemes in domains_data.items():
        dominio = DominioNatural(d.lower())
        corpus[dominio] = [
            Morfema(
                m.id, dominio, NivelOrganizacao(m.nivel),
                m.descritores, m.propriedades
            )
            for m in morphemes
        ]
    pontes = motor.extrair_analogias_cruzadas(corpus)
    return {"bridges": [p.serializar() for p in pontes], "total": len(pontes)}


@experimental.post("/api/knowledge/enrich")
def enrich_morpheme(data: Dict[str, Any]):
    from semiomorfologia.conhecimento.enriquecedor import EnriquecedorMorfemas

    enc = EnriquecedorMorfemas()
    return enc.enriquecer(data)


if EXPERIMENTAL:
    app.include_router(experimental)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": __version__}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
