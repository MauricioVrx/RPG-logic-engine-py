import pytest
from scripts.system.exceptions import (
    DiceNotFoundError, 
    ParserZeroDivisionError, 
    ParserInvalidFormulaError
)

def test_empty_formula_raise_error(parser_instance):
    """Verify that an empty formula is rejected"""
    formula = ""
    with pytest.raises(ParserInvalidFormulaError):
        assert parser_instance.resolve(formula)


def test_correct_simple_formula(parser_instance):
    """Verify that resolve returns the correct tuple structure (value, list) and range"""
    result, rolls = parser_instance.resolve("(d20 - d12) + 4")
    assert -7 <= result <= 23
    assert isinstance(result, float)
    assert isinstance(rolls, list)


def test_throw_one_dice(parser_instance):
    """Verify that parser handles one dice"""
    assert parser_instance.resolve("d6")


def test_throw_multiple_dice(parser_instance):
    """Verify that parser handles dice quantity"""
    assert parser_instance.resolve("3d20")


def test_decimal_dice_quantity_raises_error(parser_instance):
    """Verify that decimal quantities such as 2.5d6 are rejected."""
    with pytest.raises(ParserInvalidFormulaError):
        assert parser_instance.resolve("2.5d6")


def test_invalid_character_in_quantity_raises_error(parser_instance):
    """Verifica que caracteres no numéricos en la cantidad fallen"""
    with pytest.raises(ParserInvalidFormulaError, match="Invalid dice quantity"):
        parser_instance.resolve("Ad6")


def test_throw_wrong_quantity_multiple_dice(parser_instance):
    """Verify that parser handles dice quantity with a wrong quantity value"""
    with pytest.raises(ParserInvalidFormulaError):
        assert parser_instance.resolve("vwd20")


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

