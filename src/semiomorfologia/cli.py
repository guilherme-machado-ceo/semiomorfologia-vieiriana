import json
import typer
from typing import Optional

app = typer.Typer(
    help="Semiomorfologia Vieiriana - CLI v2.0",
    no_args_is_help=True
)


@app.command()
def extract(
    domain: str = typer.Argument(..., help="Dominio: mineral, vegetal, animal, humano"),
    input_file: str = typer.Argument(..., help="Arquivo JSON com lista de morfemas"),
    output: str = typer.Option("output.json", help="Arquivo de saida JSON")
):
    """Extrair analogias de um corpus por dominio."""
    from semiomorfologia.core.ontologia import (
        Morfema, DominioNatural, NivelOrganizacao
    )
    from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico

    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    motor = MotorSemiomorfologico()
    dominio = DominioNatural(domain.lower())
    corpus = [
        Morfema(
            m["id"], dominio, NivelOrganizacao(m.get("nivel", "molecular")),
            m.get("descritores", {}), m.get("propriedades", {})
        )
        for m in data
    ]
    resultados = motor.extrair_analogias_dominio(corpus, dominio)
    out = {}
    for tipo, analogias in resultados.items():
        out[tipo.value] = [a.serializar() for a in analogias]

    with open(output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    total = sum(len(v) for v in out.values())
    typer.echo(f"Extraidas {total} analogias de {domain} -> {output}")


@app.command()
def contract(
    m1_file: str = typer.Argument(..., help="JSON do morfema 1"),
    m2_file: str = typer.Argument(..., help="JSON do morfema 2"),
    output: str = typer.Option("contract.json", help="Arquivo de saida")
):
    """Anti-unificar dois morfemas (CONTRACT do PANVIEIRA)."""
    from semiomorfologia.similaridade.anti_unificacao import AntiUnificador
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    with open(m1_file, encoding="utf-8") as f:
        m1 = json.load(f)
    with open(m2_file, encoding="utf-8") as f:
        m2 = json.load(f)

    au = AntiUnificador()
    av = AvaliadorFAME()
    c = au.contrato(m1, m2)
    c["avaliacao_fame"] = av.avaliar_contrato(c)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    typer.echo(f"Contrato salvo em {output} (grau={c.get('grau_similaridade', 0)})")


@app.command()
def evaluate(
    score: float = typer.Argument(..., help="Pontuacao entre 0 e 1"),
    output: str = typer.Option("fame.json", help="Arquivo de saida")
):
    """Avaliar pontuacao com o framework FAME (6 dimensoes)."""
    from semiomorfologia.avaliacao.fame import AvaliadorFAME

    av = AvaliadorFAME()
    r = av.avaliar(score)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(r, f, indent=2, ensure_ascii=False)
    typer.echo(f"FAME={r['fame']:.4f} | Media Harmonica={r['media_harmonica']:.4f}")


@app.command()
def bridges(
    input_file: str = typer.Argument(..., help="JSON multi-dominio"),
    output: str = typer.Option("bridges.json", help="Arquivo de saida")
):
    """Buscar pontes cruzadas entre dominios."""
    from semiomorfologia.core.ontologia import (
        Morfema, DominioNatural, NivelOrganizacao
    )
    from semiomorfologia.motor.semiomorfologico import MotorSemiomorfologico

    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    motor = MotorSemiomorfologico()
    corpus = {}
    for d, morphemes in data.items():
        dominio = DominioNatural(d.lower())
        corpus[dominio] = [
            Morfema(
                m["id"], dominio, NivelOrganizacao(m.get("nivel", "molecular")),
                m.get("descritores", {}), m.get("propriedades", {})
            )
            for m in morphemes
        ]
    pontes = motor.extrair_analogias_cruzadas(corpus)
    out = [p.serializar() for p in pontes]

    with open(output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    typer.echo(f"{len(out)} pontes cruzadas -> {output}")


@app.command()
def enrich(
    input_file: str = typer.Argument(..., help="JSON do morfema"),
    output: str = typer.Option("enriched.json", help="Arquivo de saida")
):
    """Enriquecer morfema com dados de Knowledge Graphs."""
    from semiomorfologia.conhecimento.enriquecedor import EnriquecedorMorfemas

    with open(input_file, encoding="utf-8") as f:
        morfema = json.load(f)

    enc = EnriquecedorMorfemas()
    resultado = enc.enriquecer(morfema)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    fontes = list(resultado.get("enriquecimento", {}).keys())
    typer.echo(f"Enriquecido com: {fontes} -> {output}")


@app.command()
def visualize(
    input_file: str = typer.Argument(..., help="JSON com analogias ou pontes"),
    output: str = typer.Option("graph.html", help="Arquivo HTML interativo"),
    title: str = typer.Option("Analogias Semiomorfologicas", help="Titulo")
):
    """Gerar grafo interativo de analogias."""
    from semiomorfologia.visualizacao.grafo import VisualizadorAnalogias

    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = data.get("bridges", data.get("analogies", []))

    viz = VisualizadorAnalogias()
    viz.gerar_html(data, output, title)
    typer.echo(f"Grafo salvo em {output} (abrir no navegador)")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host"),
    port: int = typer.Option(8000, help="Porta")
):
    """Iniciar servidor API REST."""
    import uvicorn
    typer.echo("Servidor em http://%s:%d" % (host, port))
    typer.echo("Docs: http://%s:%d/docs" % (host, port))
    uvicorn.run("semiomorfologia.api.app:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    app()
