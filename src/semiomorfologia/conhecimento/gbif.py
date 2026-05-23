import requests
from typing import Dict, Any, List, Optional


class GBIFClient:
    """Cliente API para GBIF."""

    BASE = "https://api.gbif.org/v1"

    def buscar_especie(self, nome: str) -> Optional[Dict[str, Any]]:
        """Buscar dados taxonomicos de uma especie."""
        try:
            url = self.BASE + "/species/match?name=" + nome
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            if data.get("matchType") == "NONE":
                return None
            return {
                "fonte": "GBIF",
                "nome_cientifico": data.get("scientificName", ""),
                "reino": data.get("kingdom", ""),
                "filo": data.get("phylum", ""),
                "classe": data.get("class_", ""),
                "ordem": data.get("order", ""),
                "familia": data.get("family", ""),
                "genero": data.get("genus", ""),
                "status": data.get("status", "")
            }
        except Exception:
            return None

    def buscar_ocorrencias(self, nome: str, limite: int = 5) -> List[Dict]:
        """Buscar ocorrencias geograficas de uma especie."""
        try:
            url = (
                self.BASE
                + "/occurrence/search?scientificName=%s&limit=%d"
                % (nome, limite)
            )
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            results = r.json().get("results", [])
            return [
                {"pais": o.get("country", ""), "estado": o.get("stateProvince", ""),
                 "lat": o.get("decimalLatitude", 0), "lon": o.get("decimalLongitude", 0)}
                for o in results
            ]
        except Exception:
            return []
