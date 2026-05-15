"""
Modul Navigasi yang berisi algoritma rute terpendek, deteksi konektivitas,
dan pencarian area terisolasi.
"""
from src.data_structures.stack import Stack
from src.data_structures.queue import Queue

class NavigationSystem:
    def __init__(self, graph):
        self.graph = graph
        
    def dijkstra(self, start, end):
        """
        Mencari jalur terpendek menggunakan algoritma Dijkstra dengan array O(V^2 + E).
        
        Kompleksitas Waktu: O(V^2 + E)
        Penjelasan: 
        - Inisialisasi array (dictionary) jarak membutuhkan O(V).
        - Loop utama berjalan V kali.
        - Dalam setiap iterasi, mencari vertex dengan jarak minimum membutuhkan iterasi O(V) 
          karena menggunakan pencarian linear pada struktur data (tanpa min-heap). 
          Ini memberikan total waktu pencarian minimum O(V^2).
        - Relaksasi edge memerlukan iterasi tetangga setiap vertex. 
          Total relaksasi di seluruh iterasi dalam graf adalah O(E).
        - Jadi, kompleksitas waktu total adalah O(V^2 + E).
        
        Kompleksitas Ruang: O(V)
        - Array `distances`, `visited`, dan `previous` membutuhkan memori sebesar O(V).
        """
        distances = {v: float('inf') for v in self.graph.vertices}
        distances[start] = 0
        visited = {v: False for v in self.graph.vertices}
        previous = {v: None for v in self.graph.vertices}
        
        for _ in range(len(self.graph.vertices)):
            # Cari vertex tak terkunjungi dengan jarak minimum O(V)
            min_dist = float('inf')
            u = None
            for v in self.graph.vertices:
                if not visited[v] and distances[v] < min_dist:
                    min_dist = distances[v]
                    u = v
                    
            if u is None or u == end:
                break
                
            visited[u] = True
            
            # Relaksasi edge O(E) secara keseluruhan
            for v, weight in self.graph.get_neighbors(u):
                if not visited[v]:
                    new_dist = distances[u] + weight
                    if new_dist < distances[v]:
                        distances[v] = new_dist
                        previous[v] = u
                        
        if distances[end] == float('inf'):
            return None, float('inf')
            
        # Rekonstruksi jalur
        path = Stack()
        curr = end
        while curr is not None:
            path.push(curr)
            curr = previous[curr]
            
        path_list = []
        while not path.is_empty():
            path_list.append(path.pop())
            
        return path_list, distances[end]

    def bfs_connectivity(self, start):
        """
        Melakukan pencarian BFS untuk mendeteksi semua gedung yang terhubung.
        
        Kompleksitas Waktu: O(V + E)
        Penjelasan:
        - Setiap vertex dimasukkan dan dikeluarkan dari queue paling banyak sekali: O(V).
        - Loop mengeksplorasi setiap edge dari vertex yang dikunjungi: O(E).
        
        Kompleksitas Ruang: O(V)
        - Queue dapat menyimpan maksimal O(V) elemen. Array visited menyimpan O(V) elemen.
        """
        visited = []
        queue = Queue()
        
        queue.enqueue(start)
        visited.append(start)
        
        while not queue.is_empty():
            current = queue.dequeue()
            
            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.enqueue(neighbor)
                    
        return visited

    def dfs_exploration(self, start):
        """
        Melakukan penjelajahan DFS dari titik awal menggunakan Stack custom.
        
        Kompleksitas Waktu: O(V + E)
        Penjelasan:
        - Mirip dengan BFS, setiap vertex dikunjungi maksimal sekali O(V), 
          dan setiap edge dieksplorasi sekali O(E).
        
        Kompleksitas Ruang: O(V)
        - Stack call untuk penjelajahan graf dapat menampung maksimal O(V) vertex.
        """
        visited = []
        stack = Stack()
        
        stack.push(start)
        
        while not stack.is_empty():
            current = stack.pop()
            
            if current not in visited:
                visited.append(current)
                # Tambahkan tetangga ke stack secara terbalik (reversed)
                neighbors = self.graph.get_neighbors(current)
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.push(neighbor)
                        
        return visited

    def get_isolated_buildings(self):
        """
        Mencari gedung-gedung yang tidak memiliki jalan ke gedung lain (Terisolasi).
        
        Kompleksitas Waktu: O(V)
        Penjelasan:
        - Iterasi melalui semua vertex (V) dan memeriksa jumlah elemen 
          pada linked list tetangganya: O(V). (Meskipun get_neighbors memakan waktu O(E) 
          untuk node tersebut, panjang list bisa diperiksa saat iterasi. 
          Secara rata-rata ini bergantung pada V).
        
        Kompleksitas Ruang: O(V)
        - Array (List) untuk menyimpan hasil gedung terisolasi membutuhkan worst-case O(V).
        """
        isolated = []
        for v in self.graph.vertices:
            if len(self.graph.get_neighbors(v)) == 0:
                isolated.append(v)
        return isolated
