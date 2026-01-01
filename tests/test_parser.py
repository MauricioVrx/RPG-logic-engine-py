import pytest
from scripts.exceptions import (
    DiceNotFoundError, 
    ParserZeroDivisionError, 
    ParserInvalidFormulaError
)

def test_correct_simple_formula(parser_instance):
    """Verify that resolve returns the correct tuple structure (value, list) and range"""
    result, rolls = parser_instance.resolve("(d20 - d12) + 4")
    assert -7 <= result <= 23
    assert isinstance(result, float)
    assert isinstance(rolls, list)

def test_unrecognized_dice_raises_error(parser_instance):
    """Verify that an undefined dice name triggers DiceNotFoundError"""
    formula = "(d36 +4)"
    with pytest.raises(DiceNotFoundError) as excinfo:
        parser_instance.resolve(formula)
    assert "d36" in str(excinfo.value)

def test_parser_zero_division(parser_instance):
    """Verify that division by zero is handled by our custom exception"""
    formula = "10 / (5 - 5)"
    with pytest.raises(ParserZeroDivisionError):
        assert parser_instance.resolve(formula)

def test_invalid_formula_syntax(parser_instance):
    """Verify that unbalanced parentheses or invalid syntax raises an error"""
    formula = "(d20 + 4" 
    with pytest.raises(ParserInvalidFormulaError):
        parser_instance.resolve(formula)

# def test_test_error(parser_instance):
#     """Verify that unbalanced parentheses or invalid syntax raises an error"""
#     formula = "d20 % 4" 
#     with pytest.raises(ParserInvalidFormulaError):
#         parser_instance.resolve(formula)