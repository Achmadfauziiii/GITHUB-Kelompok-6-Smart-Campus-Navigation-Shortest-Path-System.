"""
Implementasi Graph menggunakan Adjacency List berbasis Dictionary of Linked Lists.
"""
from src.data_structures.linked_list import EdgeLinkedList

class Graph:
    def __init__(self):
        # Dictionary untuk menyimpan daftar tetangga per vertex
        self.adj_list = {}
        # Array (List Python biasa) untuk daftar semua vertex
        self.vertices = []
        
    def add_vertex(self, vertex):
        """
        Menambahkan vertex/gedung baru.
        Kompleksitas Waktu: O(1) rata-rata karena penyisipan dict.
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = EdgeLinkedList()
            self.vertices.append(vertex)
            
    def add_edge(self, src, dest, weight):
        """
        Menambahkan edge berarah dari src ke dest (dan dest ke src untuk graf tak berarah).
        Kompleksitas Waktu: O(E) untuk penyisipan ke linked list (EdgeLinkedList iterasi dari head).
        """
        if src in self.adj_list and dest in self.adj_list:
            self.adj_list[src].append(dest, weight)
            self.adj_list[dest].append(src, weight) # Asumsi jalan dua arah
            
    def get_neighbors(self, vertex):
        """
        Mengambil semua tetangga dari suatu vertex.
        Kompleksitas Waktu: O(E) di mana E adalah derajat vertex tersebut (jumlah edge).
        """
        if vertex in self.adj_list:
            # list comprehension untuk mendapatkan data dari generator iterator
            return [(d, w) for d, w in self.adj_list[vertex]]
        return []
