from typing import List, Tuple

from data_structures.modul1_graph import Graph
from data_structures.modul3_bfs_dfs import bfs 

def deteksi_terisolasi(graph: Graph, gateway: str = 'A1') -> List[Tuple[str, str]]:
    """
    Mengidentifikasi gedung yang terputus dari jaringan utama kampus.
    Menggunakan BFS/DFS dengan Big-O: O(V + E).
    """
    # 1. Dapatkan semua ID gedung yang ada di dalam graf
    semua_gedung = set(graph.adj.keys())

    # 2. Lakukan eksplorasi dari pintu gerbang utama (Gateway)
    # BFS akan mengembalikan daftar semua node yang bisa diakses
    gedung_terjangkau = set(bfs(graph, gateway))

    # 3. Cari selisihnya (Gedung yang ada, tapi tidak terjangkau oleh BFS)
    gedung_terisolasi = semua_gedung - gedung_terjangkau

    # 4. Susun hasilnya beserta nama gedungnya
    hasil = []
    for gid in gedung_terisolasi:
        nama = graph.node_names.get(gid, "Unknown")
        hasil.append((gid, nama))

    return hasil
