import pytest
from scripts.dice import Dice, CustomDice, RangeDice
from scripts.parser import FormulaProcessor

from scripts.entity import Entity
from scripts.character import Character

from scripts.item import ItemManager
from scripts.storage import Container

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

@pytest.fixture
def full_char():
    full_char = Character()
    full_char.set_ancestry('Elf', ["STR"])
    full_char.set_class('Ranger', "DEX")
    full_char.set_background('Acrobat', ["DEX", "WIS"])
    full_char.set_free_ability_points(["STR", "DEX", "WIS", "INT"])
    full_char.update_character_ability_points()
    return full_char

@pytest.fixture
def npc_human():
    human_char = Character()
    human_char.set_ancestry('Human', ["STR", "WIS"])
    human_char.set_class('Rogue', "DEX")
    human_char.set_background('Merchant', ["CHA", "WIS"])
    human_char.set_free_ability_points(["STR", "CHA", "WIS", "INT"])
    human_char.update_character_ability_points()
    return human_char

# ===============================
# ITEMS AND STORAGE
# ===============================

# 1. Import items from CSV

factory = ItemManager(base_path = "tests/schemas/data/info_csv")
factory.load_all_items(structure = {
    "equipment": ["armor", "weapon", "shield"],
    "item": ["consumables"]
})

@pytest.fixture
def test_item_factory():
    return factory

# 2. Create items
@pytest.fixture
def simple_dagger():
    simple_dagger = factory.spawn("clan_dagger")
    return simple_dagger

@pytest.fixture
def longspear():
    longspear = factory.spawn("longspear")
    return longspear

@pytest.fixture
def imposible_weapon():
    imposible_weapon = factory.spawn("impossible_weapon")
    return imposible_weapon

@pytest.fixture
def simple_shield():
    simple_shield = factory.spawn("wooden_shield")
    return simple_shield

@pytest.fixture
def simple_armor():
    simple_armor  = factory.spawn("padded_armor")
    return simple_armor

@pytest.fixture
def explorer_armor():
    explorer_armor  = factory.spawn("explorers_clothing")
    return explorer_armor

@pytest.fixture
def heavy_armor():
    heavy_armor  = factory.spawn("full_plate")
    return heavy_armor

# 3. Create containers
@pytest.fixture
def simple_chest():
    simple_chest = Container("chest_01", "Simple Chest", capacity=2)
    return simple_chest

@pytest.fixture
def normal_chest():
    normal_chest = Container("chest_02", "Normal Chest", capacity=3)
    return normal_chest
