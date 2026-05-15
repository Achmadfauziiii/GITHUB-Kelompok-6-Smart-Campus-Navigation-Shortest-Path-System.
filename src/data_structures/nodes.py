"""
Definisi Kelas Node Dasar.
"""

class LLNode:
    """Node untuk Singly Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None

class EdgeNode:
    """Node untuk representasi Edge pada Adjacency List."""
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight
        self.next = None

class BSTNode:
    """Node untuk Binary Search Tree."""
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
