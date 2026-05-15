"""
Implementasi Singly Linked List dan Edge Linked List dari nol.
"""
from src.data_structures.nodes import LLNode, EdgeNode

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        
    def append(self, data):
        """
        Menambahkan elemen di akhir linked list.
        Kompleksitas Waktu: O(1) karena menggunakan pointer tail.
        """
        new_node = LLNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

class EdgeLinkedList:
    def __init__(self):
        self.head = None
        
    def append(self, destination, weight):
        """
        Menambahkan edge baru di akhir linked list.
        Mencegah duplikasi edge ke destinasi yang sama.
        Kompleksitas Waktu: O(E) di mana E adalah jumlah edge dari node ini.
        """
        new_node = EdgeNode(destination, weight)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                if current.destination == destination:
                    # Update bobot jika edge sudah ada (opsional) atau abaikan
                    return
                current = current.next
            if current.destination == destination:
                return
            current.next = new_node

    def __iter__(self):
        current = self.head
        while current:
            yield current.destination, current.weight
            current = current.next
