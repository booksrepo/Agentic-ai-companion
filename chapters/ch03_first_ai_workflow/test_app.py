# test_app.py
from app import add, apply_discount


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_apply_discount():
    assert apply_discount(100, 0.2) == 80.0


def test_apply_discount_with_whole_number_percent():
    # A caller might reasonably think "20" means 20%, not 2000%
    result = apply_discount(100, 20)
    assert 0 <= result <= 100
