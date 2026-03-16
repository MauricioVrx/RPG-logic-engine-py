import pytest
from scripts.mechanics.dice import Dice
from scripts.system.exceptions import NonNumericResultError

def test_dice_roll_range(d6):
    """Verify that a d6 always rolls between 1 and 6 (inclusive)."""
    for _ in range(100):
        result = d6.roll()
        assert 1 <= result <= 6

def test_custom_dice_values(coin):
    """Verify that a coin flip returns valid string-based values."""
    result = coin.roll()
    assert result in ["0", "1"]

def test_multiple_rolls_numeric_sum(d6):
    """Verify that multiple_rolls correctly returns the total sum and roll list."""
    n = 3
    suma, lista = d6.multiple_rolls(n)
    assert len(lista) == n
    assert suma == sum(lista)

def test_non_numeric_dice_exception(color_dice):
    """Ensure NonNumericResultError is raised when performing arithmetic on non-numeric dice."""
    with pytest.raises(NonNumericResultError):
        assert color_dice.multiple_rolls(2)