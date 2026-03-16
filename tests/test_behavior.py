import pytest
from scripts.system.exceptions import HigherRangeValueError

def test_dice_roll_out_limit_range(d6, mocker):
    """Verifica si detecta al error al haber un número superior al límite"""
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=d6.sides+1)
    
    with pytest.raises(HigherRangeValueError):
        assert d6.roll()

def test_parser_botch_registration(parser_instance, mocker):
    """
    Forzamos que el d20 siempre saque un 1 para verificar 
    que se registre como pifia (botch).
    """
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=1)

    result, critical_list = parser_instance.resolve("d20")

    assert result == 1.0
    assert 1 in critical_list  # Verificamos que se capturó la pifia


def test_parser_critical_registration(parser_instance, mocker):
    """
    Forzamos que el d20 siempre saque un 20 para verificar 
    que se registre como crítico.
    """
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=20)

    result, critical_list = parser_instance.resolve("d20")

    assert result == 20.0
    assert 20 in critical_list

def test_parser_dice_botch_registration_with_mock_multiple(parser_instance, mocker):
    """
    Forzamos que el d20 siempre saque un 20 al tirar multiples dados
    para verificar que se registre como crítico.
    """
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=1)

    result, critical_list = parser_instance.resolve("(5d20)+1")

    assert result == 6.0
    assert 1 in critical_list
    assert len(critical_list) == 5

def test_parser_multiple_different_values(parser_instance, mocker):
    """Verifica que 2d20 sume correctamente valores distintos"""
    mocker.patch('scripts.mechanics.dice.random.randint', side_effect=[10, 5])
    result, _ = parser_instance.resolve("2d20")
    
    assert result == 15.0