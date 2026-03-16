import pytest
from scripts.mechanics.dice import Dice, CustomDice, RangeDice
from scripts.mechanics.math_parser import FormulaProcessor

from scripts.world.characters.character import Character #, CharacterIdentityManager
from scripts.world.characters.manager import CharacterManager, CharacterIdentityManager

from scripts.world.items.manager import ItemManager
from scripts.world.container import Container

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
    simple_entity = Character()
    simple_entity.get_component("combat").hit_points_max     = 10
    simple_entity.get_component("combat").hit_points_current = 5
    return simple_entity


# ===============================
# CHARACTER 
# ===============================
char_factory = CharacterIdentityManager(base_path = "tests/schemas/data/info")
char_factory.load_all_identity()

@pytest.fixture
def test_char_factory():
    return char_factory

@pytest.fixture
def simple_char():
    simple_char = Character()
    return simple_char

@pytest.fixture
def full_char():
    full_char = Character()
    full_char.set_ancestry('elf', ["STR"], identity_list= char_factory)
    full_char.set_class('ranger', "DEX", identity_list= char_factory)
    full_char.set_background('acrobat', ["DEX", "WIS"], identity_list= char_factory)
    full_char.set_free_ability_points(["STR", "DEX", "WIS", "INT"])
    full_char.update_character_ability_points()
    return full_char

@pytest.fixture
def npc_human():
    ancestry    = char_factory.spawn('ancestry', 'human')
    class_char  = char_factory.spawn('class', 'rogue')
    background  = char_factory.spawn('background', 'merchant')

    human_char = Character()
    human_char.set_ancestry(ancestry, ["STR", "WIS"])
    human_char.set_class(class_char, "DEX")
    human_char.set_background(background, ["CHA", "WIS"])
    human_char.set_free_ability_points(["STR", "CHA", "WIS", "INT"])
    human_char.update_character_ability_points()
    return human_char

# ===============================
# ITEMS AND STORAGE
# ===============================

# 1. Import items from CSV

factory = ItemManager(base_path = "tests/schemas/data/info")
factory.load_all(structure = {
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
