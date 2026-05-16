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
