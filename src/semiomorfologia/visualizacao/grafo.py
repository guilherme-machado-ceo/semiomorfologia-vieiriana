import networkx as nx
from typing import Dict, Any, List


class VisualizadorAnalogias:
    """Gerador de grafos interativos de analogias e pontes cruzadas."""

    CORES = {
        "mineral": "#8B4513",
        "vegetal": "#228B22",
        "animal": "#4169E1",
        "humano": "#FF4500"
    }

    def criar_grafo(self, dados: List[Dict], titulo: str = "Analogias") -> nx.Graph:
        G = nx.Graph()
        G.graph["title"] = titulo
        for item in dados:
            fonte_id = item.get("fonte_id", item.get("id", "n1"))
            alvo_id = item.get("alvo_id", "n2")
            fonte_dom = item.get("dominio_fonte", "")
            alvo_dom = item.get("dominio_alvo", "")
            forca = float(item.get("forca", 0.5))
            tipo = item.get("tipo", "")
            cor_f = self.CORES.get(fonte_dom, "#888888")
            cor_a = self.CORES.get(alvo_dom, "#888888")
            G.add_node(fonte_id, grupo=fonte_dom, cor=cor_f)
            G.add_node(alvo_id, grupo=alvo_dom, cor=cor_a)
            G.add_edge(fonte_id, alvo_id, weight=forca, tipo=tipo,
                       title="%s: %.2f" % (tipo, forca))
        return G

    def gerar_html(self, dados: List[Dict], output: str = "graph.html",
                   titulo: str = "Analogias Semiomorfologicas") -> bool:
        try:
            from pyvis.network import Network
            G = self.criar_grafo(dados, titulo)
            net = Network(height="700px", width="100%", notebook=False, directed=False)
            for node, attrs in G.nodes(data=True):
                net.add_node(node, label=node, color=attrs.get("cor", "#888888"),
                             group=attrs.get("grupo", ""), title=attrs.get("grupo", ""))
            for u, v, attrs in G.edges(data=True):
                w = attrs.get("weight", 0.5)
                net.add_edge(u, v, value=w, title=attrs.get("title", ""), width=max(1, w * 5))
            net.set_options("""
            var options = {
              "physics": {"hierarchicalRepulsion": {"centralGravity": 0.0, "springLength": 200}},
              "edges": {"smooth": {"type": "continuous"}},
              "groups": {
                "mineral":  {"color": {"background": "#8B4513"}},
                "vegetal":  {"color": {"background": "#228B22"}},
                "animal":   {"color": {"background": "#4169E1"}},
                "humano":   {"color": {"background": "#FF4500"}}
              }
            }
            """)
            net.save_graph(output)
            return True
        except ImportError:
            self._gerar_html_simples(dados, output, titulo)
            return True

    def _gerar_html_simples(self, dados, output, titulo):
        html = "<!DOCTYPE html><html><head><title>%s</title>\n" % titulo
        html += "<style>body{font-family:sans-serif;padding:20px}"
        html += ".a{display:inline-block;margin:8px;padding:12px 18px;"
        html += "border-radius:8px;color:white;font-weight:bold}</style></head><body>\n"
        html += "<h1>%s</h1>\n" % titulo
        html += "<p>Instale <b>pyvis</b> para visualizacao interativa: pip install pyvis</p>\n"
        html += "<h2>%d analogias encontradas</h2>\n" % len(dados)
        for d in dados:
            f = d.get("fonte_id", "?")
            a = d.get("alvo_id", "?")
            t = d.get("tipo", "?")
            fo = d.get("forca", 0)
            fd = d.get("dominio_fonte", "")
            ad = d.get("dominio_alvo", "")
            cf2 = self.CORES.get(fd, "#888")
            ca = self.CORES.get(ad, "#888")
            html += "<p><span class=\"a\" style=\"background:%s\">%s</span>" % (cf2, f)
            html += " [%s: %.2f] " % (t, fo)
            html += "<span class=\"a\" style=\"background:%s\">%s</span></p>\n" % (ca, a)
        html += "</body></html>"
        with open(output, "w", encoding="utf-8") as f:
            f.write(html)

    def estatisticas(self, dados: List[Dict]) -> Dict[str, Any]:
        G = self.criar_grafo(dados)
        stats = {
            "nos": G.number_of_nodes(),
            "arestas": G.number_of_edges(),
            "grau_medio": round(
                sum(dict(G.degree()).values()) / max(G.number_of_nodes(), 1), 2),
            "componentes": nx.number_connected_components(G),
        }
        if G.number_of_edges() > 0:
            stats["densidade"] = round(nx.density(G), 4)
        return stats
