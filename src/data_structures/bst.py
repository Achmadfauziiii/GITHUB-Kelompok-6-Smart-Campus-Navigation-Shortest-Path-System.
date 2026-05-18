from typing import Optional, List

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
        """Menambahkan gedung ke BST. Big-O: O(log V) rata-rata."""
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
                break # Kunci sudah ada

    def search(self, key: str) -> Optional[str]:
        """Mencari nama gedung berdasarkan ID. Big-O: O(log V) rata-rata."""
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
        """Menghasilkan daftar gedung terurut alfabetis ID. Big-O: O(V)."""
        result = []
        self._inorder_rekursif(self.root, result)
        return result
        
    def _inorder_rekursif(self, node: Optional[BSTNode], result: List[str]):
        if node:
            self._inorder_rekursif(node.left, result)
            result.append(f"[{node.key}] {node.nama}")
            self._inorder_rekursif(node.right, result)

    def delete(self, key: str) -> None:
        """Menghapus gedung dari direktori BST. Big-O: O(log V) rata-rata."""
        self.root = self._delete_rekursif(self.root, key)

    def _delete_rekursif(self, root: Optional[BSTNode], key: str) -> Optional[BSTNode]:
        if root is None:
            return root

        # Cari node yang akan dihapus
        if key < root.key:
            root.left = self._delete_rekursif(root.left, key)
        elif key > root.key:
            root.right = self._delete_rekursif(root.right, key)
        else:
            # Kasus 1 & 2: Node memiliki 1 anak atau tidak punya anak
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Kasus 3: Node memiliki 2 anak
            # Cari nilai terkecil di cabang kanan (inorder successor)
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.nama = temp.nama
            # Hapus inorder successor tersebut
            root.right = self._delete_rekursif(root.right, temp.key)

        return root

    def _min_value_node(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left is not None:
            current = current.left
        return current
