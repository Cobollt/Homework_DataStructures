class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)

        return node

    def find_min(self):
        if self.root is None:
            raise ValueError("Дерево порожнє")

        current = self.root

        while current.left is not None:
            current = current.left

        return current.key


tree = BinarySearchTree()

values = [50, 17, 72, 12, 23, 54, 76, 9, 14, 19, 67]

for value in values:
    tree.insert(value)

print("Найменше значення:", tree.find_min())