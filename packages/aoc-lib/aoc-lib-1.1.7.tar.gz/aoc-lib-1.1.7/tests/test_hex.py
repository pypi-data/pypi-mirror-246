# Tests
from aoc import Hex, HEX_DIRECTIONS, HEX_NAMED_DIRECTIONS


def test_hex_arithmetic():
    assert Hex(1, -3, 2) + Hex(3, -7, 4) == Hex(4, -10, 6)
    assert Hex(1, -3, 2) - Hex(3, -7, 4) == Hex(-2, 4, -2)


def test_hex_direction():
    assert Hex(0, -1, 1) == HEX_DIRECTIONS[2]
    assert Hex(0, 1, -1) == HEX_NAMED_DIRECTIONS['s']
    for h in HEX_DIRECTIONS:
        assert h.length() == 1

def test_hex_neighbor():
    assert Hex(1, -2, 1).neighbor(2) == Hex(1, -3, 2)


def test_hex_diagonal():
    assert Hex(1, -2, 1).diagonal_neighbor(3) == Hex(-1, -1, 2)


def test_hex_distance():
    assert Hex(3, -7, 4).distance(Hex(0, 0, 0)) == 7


def test_hex_rotate_right():
    assert Hex(1, -3, 2).rotate_right() == Hex(3, -2, -1)


def test_hex_rotate_left():
    assert Hex(1, -3, 2).rotate_left() == Hex(-2, -1, 3)


def test_hex_round():
    a = Hex(0.0, 0.0, 0.0)
    b = Hex(1.0, -1.0, 0.0)
    c = Hex(0.0, -1.0, 1.0)
    assert Hex(0.0, 0.0, 0.0).lerp(Hex(10.0, -20.0, 10.0), 0.5).round() == Hex(5, -10, 5)
