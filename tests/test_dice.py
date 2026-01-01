import pytest
from scripts.dice import Dice
from scripts.exceptions import NonNumericResultError

def test_dice_roll_range(d6):
    """Verifica que el d6 siempre lance entre 1 y 6"""
    for _ in range(100):
        result = d6.roll()
        assert 1 <= result <= 6

def test_custom_dice_values(coin):
    """Verifica que el dado de moneda devuelva los valores correctos"""
    result = coin.roll()
    assert result in ["0", "1"]

def test_multiple_rolls_numeric_sum(d6):
    """Verifica que multiple_rolls devuelva la suma y la lista"""
    n = 3
    suma, lista = d6.multiple_rolls(n)
    assert len(lista) == n
    assert suma == sum(lista)

def test_non_numeric_dice_exception(color_dice):
    """Verifica que un dado no numérico lance error al intentar operarlo en múltiples"""
    # Si color_dice tiene is_numeric=True debería fallar
    with pytest.raises(NonNumericResultError):
        assert color_dice.multiple_rolls(2)