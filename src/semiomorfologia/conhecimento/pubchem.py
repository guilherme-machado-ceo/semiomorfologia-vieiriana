import requests
from typing import Dict, Any, Optional


class PubChemClient:
    """Cliente REST para PubChem (NCBI)."""

    BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def buscar_composto(self, nome: str) -> Optional[Dict[str, Any]]:
        """Buscar dados de um composto quimico."""
        try:
            url = (
                self.BASE
                + "/compound/name/%s/property/"
                "MolecularFormula,MolecularWeight,IsomericSMILES/JSON"
                % nome
            )
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            props = r.json()["PropertyTable"]["Properties"][0]
            return {
                "fonte": "PubChem",
                "formula_molecular": props.get("MolecularFormula", ""),
                "peso_molecular": props.get("MolecularWeight", 0),
                "smiles": props.get("IsomericSMILES", "")
            }
        except Exception:
            return None

    def buscar_descritores(self, nome: str) -> Dict[str, Any]:
        """Buscar descritores QSAR de um composto."""
        try:
            url = (
                self.BASE
                + "/compound/name/%s/property/"
                "MolecularFormula,MolecularWeight,TPSA,"
                "HBondDonorCount,HBondAcceptorCount/JSON"
                % nome
            )
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            props = r.json()["PropertyTable"]["Properties"][0]
            return {
                "fonte": "PubChem",
                "formula_molecular": props.get("MolecularFormula", ""),
                "peso_molecular": props.get("MolecularWeight", 0),
                "area_superficie_polar": props.get("TPSA", 0),
                "doador_hidrogenio": props.get("HBondDonorCount", 0),
                "aceptor_hidrogenio": props.get("HBondAcceptorCount", 0)
            }
        except Exception:
            return {"fonte": "PubChem", "erro": "nao encontrado"}

    def enriquecer_morfema_mineral(self, morfema: Dict) -> Dict[str, Any]:
        """Enriquecer morfema mineral com dados PubChem."""
        nome = morfema.get("nome", morfema.get("id", ""))
        resultado = self.buscar_descritores(nome)
        if resultado and "erro" not in resultado:
            resultado["morfema_enriquecido"] = nome
            return resultado
        return {"fonte": "PubChem", "morfema": nome, "erro": "nao encontrado"}
