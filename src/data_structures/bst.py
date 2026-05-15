"""
Implementasi Binary Search Tree untuk pencarian data gedung.
"""
from src.data_structures.nodes import BSTNode

class BinarySearchTree:
    def __init__(self):
        self.root = None
        
    def insert(self, key, data=None):
        """
        Menyisipkan node baru ke dalam BST.
        Kompleksitas Waktu: O(h) dengan h adalah tinggi tree (rata-rata O(log n), worst O(n)).
        """
        if not self.root:
            self.root = BSTNode(key, data)
        else:
            self._insert_recursive(self.root, key, data)
            
    def _insert_recursive(self, node, key, data):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, data)
            else:
                self._insert_recursive(node.left, key, data)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, data)
            else:
                self._insert_recursive(node.right, key, data)
                
    def search(self, key):
        """
        Mencari node dalam BST berdasarkan key.
        Kompleksitas Waktu: O(h) dengan h adalah tinggi tree (rata-rata O(log n), worst O(n)).
        """
        return self._search_recursive(self.root, key)
        
    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
