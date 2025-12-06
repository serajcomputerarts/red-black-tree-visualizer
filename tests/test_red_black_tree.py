"""Unit tests for Red-Black Tree"""
import unittest
from red_black_tree import RedBlackTree, Node, parse_parenthetic


class TestRedBlackTree(unittest.TestCase):
    def setUp(self):
        self.tree = RedBlackTree()
ECHO is off.
    def test_empty_tree(self):
        self.assertEqual(self.tree.root, self.tree.NIL)
ECHO is off.
    def test_single_insertion(self):
        self.tree.insert(5)
        self.assertEqual(self.tree.root.key, 5)
        self.assertEqual(self.tree.root.color, 'BLACK')
ECHO is off.
    def test_multiple_insertions(self):
        values = [5, 3, 8, 1, 4, 7, 9]
        for val in values:
            self.tree.insert(val)
        traversal = self.tree.inorder_traversal()
        keys = [key for key, _ in traversal]
        self.assertEqual(keys, [1, 3, 4, 5, 7, 8, 9])
ECHO is off.
    def test_parse_parenthetic(self):
        result = parse_parenthetic("^(5^(3^(1^)^(4^)^)^(8^(7^)^(9^)^)^)")
        self.assertEqual(result, [5, 3, 1, 4, 8, 7, 9])


if __name__ == '__main__':
    unittest.main()
