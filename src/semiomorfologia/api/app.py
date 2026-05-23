from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(
    title="Semiomorfologia Vieiriana API",
    description="API REST para extracao de analogias semiomorfologicas",
    version="2.0.0"
)


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


@app.get("/")
def root():
    return {"framework": "Semiomorfologia Vieiriana", "version": "2.0.0", "status": "online"}


@app.get("/api/domains")
def list_domains():
    return {"domains": ["mineral", "vegetal", "animal", "humano"],
            "types": ["heuristica", "funcional", "homologica"]}


@app.post("/api/extract")
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/contract")
def create_contract(data: ContratoInput):
    from semiomorfologia.similaridade.anti_unificacao import AntiUnificador
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    au = AntiUnificador()
    av = AvaliadorFAME()
    contrato = au.contrato(data.m1, data.m2)
    contrato["avaliacao_fame"] = av.avaliar_contrato(contrato)
    return contrato


@app.post("/api/fame")
def evaluate_fame(data: FAMEInput):
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    av = AvaliadorFAME()
    return av.avaliar(data.pontuacao, data.dimensoes)


@app.post("/api/fame/batch")
def evaluate_fame_batch(scores: List[float]):
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    av = AvaliadorFAME()
    return av.avaliar_conjunto(scores)


@app.post("/api/bridges")
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


@app.post("/api/knowledge/enrich")
def enrich_morpheme(data: Dict[str, Any]):
    from semiomorfologia.conhecimento.enriquecedor import EnriquecedorMorfemas

    enc = EnriquecedorMorfemas()
    return enc.enriquecer(data)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
