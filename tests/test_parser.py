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


def test_formula_sanitization(parser_instance):
    """Check if the parser handles spaces, caps and illegal chars"""
    formula_with_spaces = " ( d20 + 5 ) "
    formula_with_caps = "D20 + 5"
    
    assert parser_instance.resolve(formula_with_spaces)
    assert parser_instance.resolve(formula_with_caps)


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
    "Check if invalid syntax generates an error." 
    formula = "d20 ++ 4" 
    with pytest.raises(ParserInvalidFormulaError):
        parser_instance.resolve(formula)


def test_unbalanced_parentheses(parser_instance):
    """Check if missing parenthesis raises an error"""
    with pytest.raises(ParserInvalidFormulaError):
        parser_instance.resolve("(d20 + 5")


def test_illegal_characters_raise_error(parser_instance):
    """Check if symbols like $ or @ raise an error"""
    formula = "d20 + 5 $"
    with pytest.raises(ParserInvalidFormulaError):
        parser_instance.resolve(formula)

