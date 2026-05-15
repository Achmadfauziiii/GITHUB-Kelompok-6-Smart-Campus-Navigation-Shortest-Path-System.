import numpy as np, time
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

np.random.seed(7)

# — Data gedung UNY (30 node simulatie) —
GEDUNG_DATA = [
    ('A1', 'Gerbang Utama'), ('A2', 'Rektorat'),
    ('B1', 'FT-Gedung 1'), ('B2', 'FT-Gedung B'),
    ('B3', 'Lab Elektronika'), ('B4', 'Lab Komputer'),
    ('C1', 'FMIPA-Gedung A'), ('C2', 'Perpustakaan'),
    ('D1', 'Stadion'), ('D2', 'GOR'),
    # tambahkan 20 gedung lainnya sesuai kreativitas kelompok
]

# — Edge berbobot (u, v, bobot_meter) acak, seed=7 —
def generate_edges(nodes, seed=7):
    rng = np.random.default_rng(seed)
    n = len(nodes)
    edges = []

    # Pastikan graph terhubung: spanning tree acak dulu
    perm = rng.permutation(n)
    for i in range(1, n):
        u = nodes[perm[i-1]][0]
        v = nodes[perm[i]][0]
        w = int(rng.integers(50, 500))  # 50–500 meter
        edges.append((u, v, w))

    # Tambah edge acak untuk densitas
    extra = int(n * 0.5)
    for _ in range(extra):
        i, j = rng.choice(n, 2, replace=False)
        w = int(rng.integers(50, 500))
        edges.append((nodes[i][0], nodes[j][0], w))

    return edges

# — Node untuk Linked List adjacency list —
class EdgeNode:
    def __init__(self, dest: str, bobot: int):
        self.dest = dest
        self.bobot = bobot
        self.next: Optional['EdgeNode'] = None

# — Graph (implementasikan dari sini) —
class Graph:
    def __init__(self):
        self.adj: Dict[str, Optional[EdgeNode]] = {}   # adjacency list
        self.node_names: Dict[str, str] = {}           # id -> nama

    def add_node(self, node_id: str, nama: str) -> None:
        """Big-O: O(1)."""
        # TODO: implementasikan
        pass

    def add_edge(self, u: str, v: str, bobot: int) -> None:
        """Big-O: O(1) tambah di head linked list."""
        # TODO: implementasikan (graf tidak berarah: dua arah)
        pass

    def neighbors(self, u: str) -> List[Tuple[str, int]]:
        """Big-O: O(deg(u))"""
        # TODO: kembalikan list (dest, bobot)
        pass

# — Dijkstra (implementasikan dari sini) —
def dijkstra(graph: Graph, source: str) -> Tuple[Dict[str, int],
Dict[str, Optional[str]]]:
    """
    Mengembalikan (dist, parent).
    dist[v] = jarak minimum dari source ke v.
    parent[v] = predecessor v pada shortest path tree.
    Big-O: O(V^2 + E) dengan array sederhana (tanpa heap library).
    """
    INF = float('inf')
    dist = {v: INF for v in graph.adj}
    parent = {v: None for v in graph.adj}
    visited = set()
    dist[source] = 0

    # TODO: implementasikan loop Dijkstra
    while len(visited) < len(graph.adj):

        current = None
        current_dist = INF

        for node in graph.adj:
           
            if node not in visited and dist[node] < current_dist:

                current = node
                current_dist = dist[node]

        if current is None:
            break

        visited.add(current)

        for neighbor, weight in graph.neighbors(current):

            if neighbor not in visited:

                new_dist = dist[current] + weight

                if new_dist < dist[neighbor]:

                    dist[neighbor] = new_dist
                    parent[neighbor] = current
    return dist, parent


def reconstruct_path(parent: Dict[str, Optional[str]], source: str, target: str) -> List[str]:
    """Rekonstruksi jalur dari parent dict. Big-O: O(V)."""
    # TODO: implementasikan
    path = []

    current = target

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path
    pass

# — BFS (implementasikan dari sini) —
def bfs(graph: Graph, source: str) -> List[str]:
    """BFS berbasis Queue Linked List. Big-O: O(V + E)."""
    # TODO: gunakan Queue berbasis Linked List (BUKAN collections.deque)
    visited = set()

    traversal =[]

    queue = [source]

    visited.add(source)

    while queue:

        current = queue.pop(0)

        traversal.append(current)

        for neighbor, _ in graph.neighbors(current):

            if neighbor not in visited:

                visited.add(neighbor)

                queue.append(neighbor)

    return traversal
    pass

# — DFS (implementasikan dari sini) —
def dfs(graph: Graph, source: str) -> List[str]:
    """DFS berbasis Stack Linked List. Big-O: O(V + E)."""
    # TODO: gunakan Stack berbasis Linked List (BUKAN list Python)
    
    visited = set()

    traversal = []

    stack = [source]

    while stack:

        current = stack.pop()

        if current not in visited:

            visited.add(current)

            traversal.append(current)

            neighbors = graph.neighbors(current)

            for neighbor, _ in reversed(neighbors):

                if neighbor not in visited:

                    stack.append(neighbor)

    return traversal
    pass

# — BST Direktori Gedung (implementasikan dari sini) —
class BSTNode:
    def __init__(self, key: str, nama: str):
        self.key = key
        self.nama = nama
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BSTGedung:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: str, nama: str) -> None:
        # TODO: implementasikan

        new_node = BSTNode(key, nama)

        if self.root is None:

            self.root = new_node
            return

        current = self.root

        while True:

            if key < current.key:

                if current.left is None:

                    current.left = new_node
                    return

                current = current.left

            else:

                if current.right is None:

                    current.right = new_node
                    return

                current = current.right
        pass

    def search(self, key: str) -> Optional[str]:
        # TODO: implementasikan; kembalikan nama gedung atau None

        current = self.root

        while current:

            if key == current.key:

                return current.nama

            elif key < current.key:

                current = current.left

            else:

                current = current.right

        return None
        pass

    def inorder(self) -> List[str]:
        # TODO: kembalikan list (key, nama) terurut

        result = []

        def traverse(node):

            if node:

                traverse(node.left)

                result.append((node.key, node.nama))

                traverse(node.right)

        traverse(self.root)

        return result
        pass

# — Main CLI —
def main():
    g = Graph()
    bst = BSTGedung()

    # Inisialisasi data
    for gid, gname in GEDUNG_DATA:
        g.add_node(gid, gname)
        bst.insert(gid, gname)

    edges = generate_edges(GEDUNG_DATA, seed=7)
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print('Smart Campus Navigation System. Ketik BANTUAN untuk daftar perintah')
    # TODO: implementasikan loop CLI


if __name__ == '__main__':
    main()
```
