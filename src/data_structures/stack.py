"""
Implementasi Stack berbasis Linked List.
"""
from src.data_structures.nodes import LLNode

class Stack:
    def __init__(self):
        self.head = None
        self._size = 0
    
    def push(self, data):
        """
        Menambahkan elemen ke puncak stack.
        Kompleksitas Waktu: O(1)
        """
        new_node = LLNode(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
        
    def pop(self):
        """
        Mengambil dan menghapus elemen dari puncak stack.
        Kompleksitas Waktu: O(1)
        """
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data
        
    def is_empty(self):
        """
        Mengecek apakah stack kosong.
        Kompleksitas Waktu: O(1)
        """
        return self.head is None
        
    def size(self):
        return self._size
