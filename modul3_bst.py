# — BST Direktori Gedung (implementasikan dari sini) —
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
        # TODO: implementasikan

        new_node = BSTNode(key, nama)

        if self.root is None:

            self.root = new_node
            return

        current = self.root

        while True:

            if key < current.key:

                if current.left is None:

                    current.left = new_node
                    return

                current = current.left

            else:

                if current.right is None:

                    current.right = new_node
                    return

                current = current.right
        pass

    def search(self, key: str) -> Optional[str]:
        # TODO: implementasikan; kembalikan nama gedung atau None

        current = self.root

        while current:

            if key == current.key:

                return current.nama

            elif key < current.key:

                current = current.left

            else:

                current = current.right

        return None
        pass

    def inorder(self) -> List[str]:
        # TODO: kembalikan list (key, nama) terurut

        result = []

        def traverse(node):

            if node:

                traverse(node.left)

                result.append((node.key, node.nama))

                traverse(node.right)

        traverse(self.root)

        return result
        pass
