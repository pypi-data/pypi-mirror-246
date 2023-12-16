from aoc.linked_list import SinglyListNode, ListNode

def check_list(node, l):
    for expected in l:
        assert node.val == expected
        node = node.next_node
    assert node is None

def test_singly():
    l = [-4, -1, 0, 3, 10]
    node = SinglyListNode.from_list(l)
    check_list(node, l)

def test_reverse_singly():
    l = [-4, -1, 0, 3, 10]
    node = SinglyListNode.from_list(reversed(l))
    new_head = node.reverse()
    check_list(new_head, l)

def test_iterator():
    l = [-4, -1, 0, 3, 10]
    node = ListNode.from_list(l)
    for i, v in enumerate(node):
        assert v == l[i]

def test_singly_iterator():
    l = [-4, -1, 0, 3, 10]
    node = SinglyListNode.from_list(l)
    for i, v in enumerate(node):
        assert v == l[i]
