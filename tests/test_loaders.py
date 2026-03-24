import pytest
from scripts.system.exceptions import (
    ItemNotFoundError,
    CharacterIdentityNotFoundError,
)
from scripts.world.items.manager import ItemManager
from scripts.world.characters.manager import CharacterManager, CharacterIdentityManager


# ===============================
# ITEMS 
# ===============================
def test_item_factory():
    # 1. Create Item Factory
    item_factory = ItemManager(base_path = "tests/schemas/data/info")
    item_factory.load_all(structure = {
        "equipment": ["armor", "weapon", "shield"],
        "item": ["consumable", "adventuring_gear"]
    })
    len(item_factory.templates) > 0


    # 2. Spawn differents type of items
    item_factory.spawn("clan_dagger")
    item_factory.spawn("wooden_shield")
    item_factory.spawn("explorers_clothing")
    item_factory.spawn("candle")
    item_factory.spawn("healing_potion_minor")
    
    # 3. Try to spawn a wrong item
    with pytest.raises(ItemNotFoundError):
        item_factory.spawn("wrong_item")

def test_wrong_item_factory():
    item_factory = ItemManager(base_path = "wrong_path")
    len(item_factory.templates) == 0


# ===============================
# CHARACTER 
# ===============================
def test_identity_character_factory():
    # 1. Create Character Identity Factory
    identity_character_factory = CharacterIdentityManager()
    identity_character_factory.load_all_identity()

    # 2. Spawn differents type of identity instances
    identity_character_factory.spawn('ancestry', 'human')
    identity_character_factory.spawn('class', 'rogue')
    identity_character_factory.spawn('background', 'merchant')

    # 3. Try to spawn wrongs identity instance
    with pytest.raises(CharacterIdentityNotFoundError):
        identity_character_factory.spawn('Wrong_category', 'wrong')