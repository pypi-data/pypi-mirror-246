from aoc.tree import TreeNode


def test_tree_setup():
    tree = TreeNode.from_list([1, 2, 3, 4, 5])
    assert tree.val == 1
    assert tree.left.val == 2
    assert tree.right.val == 3
    assert tree.left.left.val == 4
    assert tree.left.right.val == 5
    assert tree.right.left is None
    assert tree.right.right is None


def test_complex_tree_setup():
    tree = TreeNode.from_list([1, 2, 3, 4, 5, None, 7, 8, None, None, 9])
    assert tree.val == 1
    assert tree.left.val == 2
    assert tree.right.val == 3
    assert tree.left.left.val == 4
    assert tree.left.right.val == 5
    assert tree.right.left is None
    assert tree.right.right.val == 7
    assert tree.left.left.left.val == 8
    assert tree.left.left.right is None
    assert tree.left.right.left is None
    assert tree.left.right.right.val == 9
    assert tree.right.right.left is None
    assert tree.right.right.right is None


def test_inorder():
    tree = TreeNode.from_list([1, 2, 3, 4, 5])
    in_order = [4, 2, 5, 1, 3]
    assert list(tree) == in_order
    assert list(tree.nodes()) == in_order
    assert list(tree.nodes(TreeNode.INORDER)) == in_order
    assert list(tree.nodes(TreeNode.PREORDER)) == [1, 2, 4, 5, 3]
    assert list(tree.nodes(TreeNode.POSTORDER)) == [4, 5, 2, 3, 1]

    for i, node in enumerate(tree):
        assert node == in_order[i]
