class TreeNode:
    """
    A class representing a single node in the Binary Search Tree.
    """
    def __init__(self, key):
        self.key = key  # The key of the node
        self.left = None  # Pointer to the left child
        self.right = None  # Pointer to the right child

    def __str__(self):
        return str(self.key)


class BinarySearchTree:
    """
    A class for implementing a Binary Search Tree (BST).
    """
    def __init__(self):
        self.root = None  # The root node of the BST

    # Insertion of a key into the BST
    def _insert(self, node, key):
        """
        A recursive helper function to insert a key into the subtree
        rooted at 'node'.
        """
        if node is None:
            return TreeNode(key)  # Create a new node if the subtree is empty

        if key < node.key:
            node.left = self._insert(node.left, key)  # Insert into left subtree
        elif key > node.key:
            node.right = self._insert(node.right, key)  # Insert into right subtree

        return node

    def insert(self, key):
        """
        Public method to insert a key into the BST.
        """
        self.root = self._insert(self.root, key)

    # Searching for a key in the BST
    def _search(self, node, key):
        """
        A recursive helper function to search for a key in the subtree
        rooted at 'node'.
        """
        if node is None or node.key == key:
            return node  # Return the node if found, or None if not found

        if key < node.key:
            return self._search(node.left, key)  # Search in the left subtree
        return self._search(node.right, key)  # Search in the right subtree

    def search(self, key):
        """
        Public method to search for a key in the BST.
        """
        return self._search(self.root, key)

    # Deleting a node in the BST
    def _delete(self, node, key):
        """
        A recursive helper function to delete a key from the subtree
        rooted at 'node'.
        """
        if node is None:
            return node  # Key not found, return None

        if key < node.key:
            node.left = self._delete(node.left, key)  # Delete from left subtree
        elif key > node.key:
            node.right = self._delete(node.right, key)  # Delete from right subtree
        else:
            # Node with one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get the in-order successor
            node.key = self._min_value(node.right)
            # Delete the in-order successor
            node.right = self._delete(node.right, node.key)

        return node

    def delete(self, key):
        """
        Public method to delete a key from the BST.
        """
        self.root = self._delete(self.root, key)

    # Helper function to find the minimum value in a subtree
    def _min_value(self, node):
        """
        Find the node with the smallest key in the subtree rooted at 'node'.
        """
        while node.left is not None:
            node = node.left
        return node.key

    # In-order traversal
    def _inorder_traversal(self, node, result):
        """
        A recursive helper function to perform in-order traversal
        and append keys to the 'result' list in sorted order.
        """
        if node:
            self._inorder_traversal(node.left, result)  # Traverse left subtree
            result.append(node.key)  # Visit root node
            self._inorder_traversal(node.right, result)  # Traverse right subtree

    def inorder_traversal(self):
        """
        Public method to perform in-order traversal of the BST.
        """
        result = []
        self._inorder_traversal(self.root, result)
        return result

    # Visualization of the BST structure
    def _visualize(self, node, level=0, prefix="Root: "):
        """
        A recursive helper function to visualize the tree structure.
        """
        if node is not None:
            print(" " * (level * 4) + prefix + str(node.key))
            self._visualize(node.left, level + 1, "L--- ")
            self._visualize(node.right, level + 1, "R--- ")

    def visualize(self):
        """
        Public method to visualize the BST structure.
        """
        if self.root is None:
            print("The tree is empty. Like my soul.")
        else:
            self._visualize(self.root)


# Example Usage and Testing
if __name__ == "__main__":
    bst = BinarySearchTree()
    nodes = [50, 30, 20, 40, 70, 60, 80]

    # Insert nodes
    for node in nodes:
        bst.insert(node)

    print("Initial tree structure:")
    bst.visualize()

    print("\nIn-order Traversal:", bst.inorder_traversal())  # [20, 30, 40, 50, 60, 70, 80]

    print("\nSearching for 40:", bst.search(40))  # Should return the node
    print("Searching for 100:", bst.search(100))  # Should return None

    # Deleting a node
    print("\nDeleting node 40...")
    bst.delete(40)
    print("In-order Traversal after deletion:", bst.inorder_traversal())  # [20, 30, 50, 60, 70, 80]

    print("\nUpdated tree structure:")
    bst.visualize()

    # Edge-case testing
    print("\nDeleting the root (50)...")
    bst.delete(50)
    print("In-order Traversal after deleting root:", bst.inorder_traversal())  # [20, 30, 60, 70, 80]
    bst.visualize()
