import numpy as np, time
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

np.random.seed(7)

# — Data gedung UNY (30 node simulatie) —
GEDUNG_DATA = [
    ('A1', 'Gerbang Utama'),           ('A2', 'Rektorat'),
    ('B1', 'FT-Gedung A'),             ('B2', 'FT-Gedung B'),
    ('B3', 'Lab Elektronika'),         ('B4', 'Lab Komputer'),
    ('C1', 'FMIPA-Gedung A'),          ('C2', 'Lab Fisika'),
    ('D1', 'Stadion'),                 ('D2', 'GOR'),
    ('E1', 'PKM FT UNY'),              ('E2', 'LPTK FT UNY'),
    
    ('E3', 'FISIP-Gedung A'),          ('E4', 'FISIP-Gedung B'),
    ('E5', 'Ruang Seminar FISIP'),     ('E6', 'Pusat Kajian Sosial'),
    ('E7', 'Perpustakaan'),              ('E8', 'Ruang Sidang FISIP'),

    ('F1', 'FEB-Gedung A'),            ('F2', 'FEB-Gedung B'),
    ('F3', 'Lab Akuntansi'),           ('F4', 'Lab Manajemen'),
    ('F5', 'Pojok Bursa Efek'),        ('F6', 'Ruang Sidang FEB'),

    ('G1', 'FIKK-Gedung A'),           ('G2', 'FIKK-Gedung B'),
    ('G3', 'Laboratorium Olahraga'),   ('G4', 'Lapangan Atletik'),
    ('G5', 'Kolam Renang FIKK'),       ('G6', 'Lapangan Sepak Bola'),
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
        if current == source:
            break
        current = parent[current]
    else:
        return []

    path.reverse()

    if not path or path[0] != source:
        return []

    return path
    pass

# — Node Linked List internal —
class _LLNode:
    def __init__(self, data):
        self.data = data
        self.next: Optional['_LLNode'] = None


# — Queue berbasis Linked List (FIFO) —
class Queue:
    def __init__(self):
        self._head: Optional[_LLNode] = None
        self._tail: Optional[_LLNode] = None

    def enqueue(self, data) -> None:
        node = _LLNode(data)
        if self._tail:
            self._tail.next = node
        self._tail = node
        if self._head is None:
            self._head = node

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue dari Queue kosong")
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        return data

    def is_empty(self) -> bool:
        return self._head is None


# — Stack berbasis Linked List (LIFO) —
class Stack:
    def __init__(self):
        self._top: Optional[_LLNode] = None

    def push(self, data) -> None:
        node = _LLNode(data)
        node.next = self._top
        self._top = node

    def pop(self):
        if self._top is None:
            raise IndexError("pop dari Stack kosong")
        data = self._top.data
        self._top = self._top.next
        return data

    def is_empty(self) -> bool:
        return self._top is None

# — BFS (implementasikan dari sini) —
def bfs(graph: Graph, source: str) -> List[str]:
    """BFS berbasis Queue Linked List. Big-O: O(V + E)."""
    # TODO: gunakan Queue berbasis Linked List (BUKAN collections.deque)
    visited = set()
    traversal =[]
    queue = Queue()

    queue.enqueue(source)
    visited.add(source)

    while not queue.is_empty():
        current = queue.dequeue()
        traversal.append(current)

        for neighbor, _ in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

    return traversal
    pass

# — DFS (implementasikan dari sini) —
def dfs(graph: Graph, source: str) -> List[str]:
    """DFS berbasis Stack Linked List. Big-O: O(V + E)."""
    # TODO: gunakan Stack berbasis Linked List (BUKAN list Python)
    visited = set()
    traversal = []
    stack = Stack()

    stack.push(source)

    while not stack.is_empty():
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        traversal.append(current)
        
        neighbors = graph.neighbors(current)
        for neighbor, _ in reversed(neighbors):
                if neighbor not in visited:
                    stack.push(neighbor)

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
        pass

    def search(self, key: str) -> Optional[str]:
        # TODO: implementasikan; kembalikan nama gedung atau None
        pass

    def inorder(self) -> List[str]:
        # TODO: kembalikan list (key, nama) terurut
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
