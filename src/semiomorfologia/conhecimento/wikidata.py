import requests
from typing import Dict, Any, List, Optional


class WikidataClient:
    """Cliente SPARQL para Wikidata."""

    ENDPOINT = "https://query.wikidata.org/sparql"

    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "Semiomorfologia/2.0 (research)"
        }

    def buscar_propriedades(self, termo: str, lang: str = "pt") -> Dict[str, Any]:
        """Buscar propriedades de um termo no Wikidata."""
        query = """
        SELECT ?propLabel ?valueLabel WHERE {
            ?item rdfs:label "%s"@%s.
            ?item ?p ?statement.
            ?statement ?ps ?value.
            ?property wikibase:claim ?p.
            ?property rdfs:label ?propLabel.
            FILTER(LANG(?propLabel) = "%s")
            ?value rdfs:label ?valueLabel.
            FILTER(LANG(?valueLabel) = "%s")
        }
        LIMIT 15
        """ % (termo, lang, lang, lang)
        try:
            r = requests.get(
                self.ENDPOINT,
                params={"query": query, "format": "json"},
                headers=self.headers,
                timeout=10
            )
            r.raise_for_status()
            bindings = r.json().get("results", {}).get("bindings", [])
            props = {}
            for b in bindings:
                key = b.get("propLabel", {}).get("value", "")
                val = b.get("valueLabel", {}).get("value", "")
                if key and val:
                    props[key] = val
            return {"fonte": "Wikidata", "termo": termo, "propriedades": props}
        except Exception as e:
            return {"fonte": "Wikidata", "erro": str(e)}

    def buscar_relacionados(self, termo: str, lang: str = "pt") -> List[str]:
        """Buscar termos relacionados."""
        query = """
        SELECT ?relatedLabel WHERE {
            ?item rdfs:label "%s"@%s.
            ?item ?p ?related.
            ?related rdfs:label ?relatedLabel.
            FILTER(LANG(?relatedLabel) = "%s")
            FILTER(!isLiteral(?related))
        }
        LIMIT 10
        """ % (termo, lang, lang)
        try:
            r = requests.get(
                self.ENDPOINT,
                params={"query": query, "format": "json"},
                headers=self.headers,
                timeout=10
            )
            r.raise_for_status()
            bindings = r.json().get("results", {}).get("bindings", [])
            return [b["relatedLabel"]["value"] for b in bindings
                    if "relatedLabel" in b]
        except Exception:
            return []
