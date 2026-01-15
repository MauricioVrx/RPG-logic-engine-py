import pytest
from scripts.dice import Dice, CustomDice, RangeDice
from scripts.parser import FormulaProcessor

from scripts.entity import Entity
from scripts.character import Character

# ===============================
# DICE 
# ===============================

@pytest.fixture
def d6():
    return Dice(6, name="standard_d6")

@pytest.fixture
def d20():
    return Dice(20, name="standard_d20")

@pytest.fixture
def coin():
    return CustomDice(values=["0", "1"], name="coin", is_numeric=True)

@pytest.fixture
def color_dice():
    return RangeDice(values=((2, "Rojo"), (3, "Verde")), is_numeric=True) 

# ===============================
# PARSER 
# ===============================

@pytest.fixture
def parser_instance():
    throw = {
        'd100' : Dice(100),
        'd20'  : Dice(20),
        'd12'  : Dice(12),
        'd6'   : Dice(6)
    }
    return FormulaProcessor(throw, Dice(20))

# ===============================
# ENTITY 
# ===============================

@pytest.fixture
def simple_entity():
    simple_entity = Entity()
    simple_entity.hit_points_max     = 10
    simple_entity.hit_points_current = 5
    return simple_entity


# ===============================
# CHARACTER 
# ===============================

@pytest.fixture
def simple_char():
    simple_char = Character()
    return simple_char