"""
Implementasi Queue berbasis Linked List.
"""
from src.data_structures.nodes import LLNode

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        
    def enqueue(self, data):
        """
        Menambahkan elemen di bagian belakang (tail) antrean.
        Kompleksitas Waktu: O(1)
        """
        new_node = LLNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            
    def dequeue(self):
        """
        Menghapus dan mengembalikan elemen dari bagian depan (head) antrean.
        Kompleksitas Waktu: O(1)
        """
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data
        
    def is_empty(self):
        """
        Mengecek apakah queue kosong.
        Kompleksitas Waktu: O(1)
        """
        return self.head is None
