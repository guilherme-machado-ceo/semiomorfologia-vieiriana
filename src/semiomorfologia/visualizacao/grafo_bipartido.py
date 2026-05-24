"""
Grafo Bipartido para EXPAND PANVIEIRA

Implementa a operação EXPAND usando um grafo bipartido Sᵢ-Cᵢ onde:
  - Nós do lado esquerdo: diferenciadores {Sᵢ}
  - Nós do lado direito: loci {Cᵢ}
  - Arestas: combinações semióticas válidas com peso de plausibilidade

Em vez de gerar o produto cartesiano completo (S × C), EXPAND percorre
apenas as arestas existentes, evitando explosão combinatória semântica.
Referência: Seção 6 (Escalabilidade) do paper PANVIEIRA.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional, Set, Any
from collections import defaultdict


class GrafoBipartidoExpand:
    """
    Grafo bipartido para escalabilidade semântica do EXPAND.
    
    Em vez de S × C (produto cartesiano), opera apenas sobre arestas
    (Sᵢ, Cᵢ) previamente validadas como semióticas via corpus ou ontologia.
    """
    
    def __init__(self):
        self.arestas: Dict[Tuple[str, str], float] = {}  # (Sᵢ, Cᵢ) -> peso
        self.nos_S: Set[str] = set()
        self.nos_C: Set[str] = set()
        self.g_invariante: str = ""
    
    def adicionar_aresta(self, s: str, c: str, peso: float = 1.0):
        """Adiciona aresta (Sᵢ, Cᵢ) com peso de plausibilidade."""
        self.arestas[(s, c)] = peso
        self.nos_S.add(s)
        self.nos_C.add(c)
    
    def adicionar_arestas_em_lote(self, pares: List[Tuple[str, str]],
                                   pesos: Optional[List[float]] = None):
        """Adiciona múltiplas arestas de uma vez."""
        for i, (s, c) in enumerate(pares):
            peso = pesos[i] if pesos and i < len(pesos) else 1.0
            self.adicionar_aresta(s, c, peso)
    
    def expand(self, g: str, compor=None) -> List[Dict[str, Any]]:
        """
        EXPAND via grafo bipartido: percorre apenas arestas válidas.
        
        Args:
            g: Termo genérico (invariante)
            compor: Função (S, G, C) -> eᵢ
            
        Returns:
            Lista de instâncias com metadados
        """
        self.g_invariante = g
        if compor is None:
            compor = lambda s, gc, c: f"{s} {gc} {c}"
        
        instancias = []
        for (s, c), peso in self.arestas.items():
            instancia = compor(s, g, c)
            instancias.append({
                'instancia': instancia,
                'S': s,
                'G': g,
                'C': c,
                'peso': peso
            })
        
        # Ordenar por peso (maior plausibilidade primeiro)
        instancias.sort(key=lambda x: x['peso'], reverse=True)
        return instancias
    
    def expand_top_k(self, g: str, k: int, compor=None) -> List[Dict[str, Any]]:
        """EXPAND retornando apenas as k melhores instâncias por peso."""
        todas = self.expand(g, compor)
        return todas[:k]
    
    def expand_com_filtro_P(self, g: str, restricoes_P: List[callable],
                             compor=None) -> List[Dict[str, Any]]:
        """
        EXPAND com filtragem pelo horizonte hermenêutico P.
        
        Cada restrição em P é aplicada como filtro sobre as arestas.
        Arestas que violam qualquer restrição são excluídas.
        """
        todas = self.expand(g, compor)
        filtradas = []
        for inst in todas:
            viola = False
            for restricao in restricoes_P:
                try:
                    if not restricao(inst['S'], g, inst['C']):
                        viola = True
                        break
                except Exception:
                    viola = True
                    break
            if not viola:
                filtradas.append(inst)
        return filtradas
    
    def estimar_arestas_ausentes(self) -> List[Tuple[str, str, float]]:
        """
        Estima arestas prováveis não observadas via caminhada aleatória.
        
        Para cada S sem conexão com C, estima peso via vizinhos compartilhados.
        """
        # Construir adjacências
        adj_S = defaultdict(set)  # S -> {C}
        adj_C = defaultdict(set)  # C -> {S}
        for (s, c) in self.arestas:
            adj_S[s].add(c)
            adj_C[c].add(s)
        
        estimadas = []
        for s in self.nos_S:
            for c in self.nos_C:
                if (s, c) not in self.arestas:
                    # Peso = |vizinhos(S) ∩ vizinhos(C)| / |vizinhos(S) ∪ vizinhos(C)|
                    inter = len(adj_S[s] & adj_C[c])
                    uniao = len(adj_S[s] | adj_C[c])
                    if uniao > 0:
                        peso = inter / uniao
                        if peso > 0.3:  # limiar mínimo
                            estimadas.append((s, c, peso))
        
        estimadas.sort(key=lambda x: x[2], reverse=True)
        return estimadas
    
    def estatisticas(self) -> Dict[str, any]:
        """Retorna estatísticas do grafo bipartido."""
        n_arestas = len(self.arestas)
        n_cartesiano = len(self.nos_S) * len(self.nos_C)
        taxa_cobertura = n_arestas / n_cartesiano if n_cartesiano > 0 else 0
        
        pesos = list(self.arestas.values()) if self.arestas else [0]
        
        return {
            'n_diferenciadores': len(self.nos_S),
            'n_loci': len(self.nos_C),
            'n_arestas': n_arestas,
            'n_cartesiano': n_cartesiano,
            'reducao_combinatoria': 1 - taxa_cobertura if taxa_cobertura <= 1 else 0,
            'peso_medio': float(np.mean(pesos)),
            'peso_min': float(min(pesos)),
            'peso_max': float(max(pesos)),
            'densidade': taxa_cobertura
        }
    
    def para_networkx(self):
        """Converte para grafo NetworkX (se disponível)."""
        try:
            import networkx as nx
            G = nx.Graph()
            for s in self.nos_S:
                G.add_node(s, bipartite=0, tipo='diferenciador')
            for c in self.nos_C:
                G.add_node(c, bipartite=1, tipo='locus')
            for (s, c), peso in self.arestas.items():
                G.add_edge(s, c, weight=peso)
            return G
        except ImportError:
            return None
    
    def gerar_html(self, g: str, titulo: str = "Grafo Bipartido PANVIEIRA",
                   output_path: Optional[str] = None) -> Optional[str]:
        """
        Gera visualização HTML interativa via pyvis.
        """
        try:
            import networkx as nx
            from pyvis.network import Network
            
            G = self.para_networkx()
            if G is None:
                return None
            
            net = Network(height='600px', width='100%', directed=False,
                         notebook=False)
            net.from_nx(G)
            
            # Cores por tipo de nó
            for node in net.nodes:
                if node in self.nos_S:
                    net.nodes[node]['color'] = '#4CAF50'  # verde
                    net.nodes[node]['title'] = f'Diferenciador: {node}'
                else:
                    net.nodes[node]['color'] = '#2196F3'  # azul
                    net.nodes[node]['title'] = f'Locus: {node}'
            
            for edge in net.edges:
                peso = self.arestas.get((edge['from'], edge['to']), 1.0)
                edge['value'] = peso
                edge['title'] = f'Peso: {peso:.2f}'
            
            net.set_options("""
            {
                "physics": {
                    "barnesHut": {"gravitationalConstant": -3000}
                },
                "nodes": {"font": {"size": 14}}
            }
            """)
            
            if output_path:
                net.show(output_path)
                return output_path
            else:
                path = f"grafo_bipartido_{g[:20].replace(' ', '_')}.html"
                net.show(path)
                return path
        except ImportError:
            return None
