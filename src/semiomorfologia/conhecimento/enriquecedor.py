from typing import Dict, Any
from .wikidata import WikidataClient
from .pubchem import PubChemClient
from .gbif import GBIFClient


class EnriquecedorMorfemas:
    """Orquestra enriquecimento de morfemas com Knowledge Graphs."""

    def __init__(self):
        self.wikidata = WikidataClient()
        self.pubchem = PubChemClient()
        self.gbif = GBIFClient()

    def enriquecer(self, morfema: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquecer um morfema com dados de fontes externas."""
        dominio = str(morfema.get("dominio", "")).lower()
        nome = morfema.get("nome", morfema.get("id", ""))

        resultado = {"morfema_original": morfema, "enriquecimento": {}}

        if "mineral" in dominio:
            pub = self.pubchem.enriquecer_morfema_mineral(morfema)
            if pub and "erro" not in pub:
                resultado["enriquecimento"]["pubchem"] = pub

        if "vegetal" in dominio or "animal" in dominio:
            gbif = self.gbif.buscar_especie(nome)
            if gbif:
                resultado["enriquecimento"]["gbif"] = gbif

        wiki = self.wikidata.buscar_propriedades(nome)
        if wiki and "erro" not in wiki:
            resultado["enriquecimento"]["wikidata"] = wiki

        return resultado

    def enriquecer_lote(self, morfemas: list, verbose: bool = False) -> list:
        """Enriquecer varios morfemas de uma vez."""
        resultados = []
        for m in morfemas:
            r = self.enriquecer(m)
            resultados.append(r)
            if verbose:
                nome = m.get("nome", m.get("id", "?"))
                fontes = list(r.get("enriquecimento", {}).keys())
                print("  %s: %s" % (nome, fontes if fontes else "sem dados"))
        return resultados
