"""
Modul untuk generasi data kampus (gedung dan rute) menggunakan numpy.random.
"""
# pyrefly: ignore [missing-import]
import numpy as np 
from src.data_structures.graph import Graph
from src.data_structures.bst import BinarySearchTree

def generate_campus_data():
    """
    Menghasilkan data gedung dan edge untuk kampus UNY.
    Menggunakan np.random.seed(7) untuk mereproduksi:
    - 30 gedung (Vertices)
    - 55 edge berbobot antara 50-500 meter.
    
    Kompleksitas Waktu Pembentukan Graf: O(V + E * E_v)
    di mana E_v adalah derajat rata-rata vertex untuk pengecekan edge yang sudah ada.
    """
    np.random.seed(7)
    
    buildings = [
        "Rektorat", "FIP", "FBS", "FMIPA", "FIS", "FT", "FIK", "FE",
        "Perpustakaan", "Masjid Mujahidin", "Kopma", "GOR", "Kolam Renang",
        "Auditorium", "Plaza UNY", "Museum Pendidikan", "Lab Terpadu",
        "Gedung Pascasarjana", "Student Center", "Asrama Putra", "Asrama Putri",
        "Fakultas Kedokteran", "Klinik Kampus", "Pusat Komputer",
        "Fakultas Vokasi", "Laboratorium Bahasa", "Gedung IKA",
        "UPT Bahasa", "Fakultas Hukum", "Gedung LPPMP"
    ]
    
    graph = Graph()
    bst = BinarySearchTree()
    
    for b in buildings:
        graph.add_vertex(b)
        bst.insert(b)
        
    edges_added = 0
    while edges_added < 55:
        src_idx = np.random.randint(0, 30)
        dest_idx = np.random.randint(0, 30)
        
        if src_idx != dest_idx:
            src = buildings[src_idx]
            dest = buildings[dest_idx]
            weight = np.random.randint(50, 501)
            
            # Cek apakah sudah ada edge
            exists = False
            for neighbor, _ in graph.get_neighbors(src):
                if neighbor == dest:
                    exists = True
                    break
                    
            if not exists:
                graph.add_edge(src, dest, weight)
                edges_added += 1
                
    return graph, bst
