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
    ('E7', 'Perpustakaan'),            ('E8', 'Ruang Sidang FISIP'),

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

# — Dijkstra (implementasikan dari sini) —
def dijkstra(graph: Graph, source: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
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
        if self.root is None:
            self.root = BSTNode(key, nama)
            return
            
        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = BSTNode(key, nama)
                    break
                current = current.left
            elif key > current.key:
                if current.right is None:
                    current.right = BSTNode(key, nama)
                    break
                current = current.right
            else:
                break

    def search(self, key: str) -> Optional[str]:
        current = self.root
        while current is not None:
            if key == current.key:
                return current.nama
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def inorder(self) -> List[str]:
        result = []
        self._inorder_rekursif(self.root, result)
        return result
        
    def _inorder_rekursif(self, node: Optional[BSTNode], result: List[str]):
        if node:
            self._inorder_rekursif(node.left, result)
            result.append(f"[{node.key}] {node.nama}")
            self._inorder_rekursif(node.right, result)

    def delete(self, key: str) -> None:
        self.root = self._delete_rekursif(self.root, key)

    def _delete_rekursif(self, root: Optional[BSTNode], key: str) -> Optional[BSTNode]:
        if root is None:
            return root
        if key < root.key:
            root.left = self._delete_rekursif(root.left, key)
        elif key > root.key:
            root.right = self._delete_rekursif(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.nama = temp.nama
            root.right = self._delete_rekursif(root.right, temp.key)
        return root

    def _min_value_node(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left is not None:
            current = current.left
        return current


# — Modul 5: Deteksi Komponen Terisolasi —
def deteksi_terisolasi(graph: Graph, gateway: str = 'A1') -> List[Tuple[str, str]]:
    semua_gedung = set(graph.adj.keys())
    gedung_terjangkau = set(bfs(graph, gateway))
    gedung_terisolasi = semua_gedung - gedung_terjangkau

    hasil = []
    for gid in gedung_terisolasi:
        nama = graph.node_names.get(gid, "Unknown")
        hasil.append((gid, nama))
    return hasil


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

    print('='*55)
    print(' SMART CAMPUS NAVIGATION SYSTEM '.center(55, '='))
    print('='*55)
    print("Ketik 'BANTUAN' untuk melihat daftar perintah.")
    
    while True:
        try:
            inp = input("\n[SmartCampus] > ").strip().split()
            if not inp: continue
                
            cmd = inp[0].upper()
            
            if cmd == "BANTUAN":
                print("1. JALUR <sumber> <tujuan> (Cari rute terpendek)")
                print("2. JELAJAH_DFS <sumber>    (Eksplorasi DFS)")
                print("3. JELAJAH_BFS <sumber>    (Eksplorasi BFS)")
                print("4. CARI_GEDUNG <kode>      (Cari nama gedung)")
                print("5. HAPUS_GEDUNG <kode>     (Hapus dari direktori)")
                print("6. DIREKTORI               (Lihat semua gedung urut abjad)")
                print("7. AUDIT_ISOLASI           (Cek jaringan terputus)")
                print("8. KELUAR")
                
            elif cmd == "JALUR":
                if len(inp) != 3:
                    print("Format salah! Gunakan: JALUR <sumber> <tujuan>")
                    continue
                src, dst = inp[1], inp[2]
                
                t_start = time.perf_counter()
                dist, parent = dijkstra(g, src)
                t_end = time.perf_counter()
                
                if dist.get(dst, float('inf')) == float('inf'):
                    print(f"Tidak ada jalur dari {src} ke {dst}")
                else:
                    path = reconstruct_path(parent, src, dst)
                    print(f"Jalur: {' -> '.join(path)}")
                    print(f"Total Jarak: {dist[dst]} meter")
                    print(f"[Big-O: O(V^2 + E) | Waktu Eksekusi: {(t_end-t_start)*1000:.4f} ms]")
                    
            elif cmd == "JELAJAH_DFS":
                if len(inp) != 2: continue
                print("Kunjungan DFS:", " -> ".join(dfs(g, inp[1])))
                print("[Big-O: O(V + E)]")
                
            elif cmd == "JELAJAH_BFS":
                if len(inp) != 2: continue
                print("Kunjungan BFS:", " -> ".join(bfs(g, inp[1])))
                print("[Big-O: O(V + E)]")
                
            elif cmd == "CARI_GEDUNG":
                if len(inp) != 2: continue
                nama = bst.search(inp[1])
                if nama:
                    print(f"Ditemukan: {nama}")
                else:
                    print("Gedung tidak ditemukan.")
                print("[Big-O: O(log V)]")
                
            elif cmd == "HAPUS_GEDUNG":
                if len(inp) != 2: continue
                kode = inp[1]
                if bst.search(kode):
                    bst.delete(kode)
                    print(f"Gedung [{kode}] berhasil dihapus dari direktori BST.")
                else:
                    print(f"Gedung [{kode}] tidak ditemukan.")
                print("[Big-O: O(log V)]")

            elif cmd == "DIREKTORI":
                print("\n".join(bst.inorder()))
                print("\n[Big-O: O(V)]")

            elif cmd == "AUDIT_ISOLASI":
                terisolasi = deteksi_terisolasi(g, 'A1')
                if not terisolasi:
                    print("Audit Selesai: Jaringan aman, tidak ada gedung terisolasi.")
                else:
                    print(f"PERINGATAN! Ditemukan {len(terisolasi)} gedung TERISOLASI:")
                    for gid, nama in terisolasi:
                        print(f"- [{gid}] {nama}")
                print("[Big-O: O(V + E)]")
                
            elif cmd == "KELUAR":
                print("Menutup Smart Campus Navigation System. Sampai jumpa!")
                break
                
            else:
                print("Perintah tidak dikenali. Ketik BANTUAN.")
                
        except KeyboardInterrupt:
            print("\nSistem dihentikan paksa. Sampai jumpa!")
            break


if __name__ == '__main__':
    main()
