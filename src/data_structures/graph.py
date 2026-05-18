from typing import Optional, Dict, List, Tuple

class EdgeNode:
    def __init__(self, dest: str, bobot: int):
        self.dest = dest
        self.bobot = bobot
        self.next: Optional['EdgeNode'] = None

class Graph:
    def __init__(self):
        self.adj: Dict[str, Optional[EdgeNode]] = {}   # adjacency list
        self.node_names: Dict[str, str] = {}           # id -> nama

    def add_node(self, node_id: str, nama: str) -> None:
        """Big-O: O(1)."""
        if node_id not in self.adj:
            self.adj[node_id] = None
            self.node_names[node_id] = nama

    def add_edge(self, u: str, v: str, bobot: int) -> None:
        """Big-O: O(1) tambah di head linked list."""
        # tambah edge u -> v
        new_node_v = EdgeNode(v, bobot)
        new_node_v.next = self.adj[u]
        self.adj[u] = new_node_v

        # tambah edge v -> u (graph tidak berarah)
        new_node_u = EdgeNode(u, bobot)
        new_node_u.next = self.adj[v]
        self.adj[v] = new_node_u

    def neighbors(self, u: str) -> List[Tuple[str, int]]:
        """Big-O: O(deg(u))"""
        
        result = []
        current = self.adj[u]

        while current is not None:
            result.append((current.dest, current.bobot))
            current = current.next

        return result

    def is_connected(self, u: str, v: str) -> bool:
        """Cek apakah ada edge langsung antara u dan v."""
        
        current = self.adj[u]

        while current is not None:
            if current.dest == v:
                return True
            current = current.next

        return False
