import copy
import pytest
from scripts.world.items.item    import Item
from scripts.world.items.manager import ItemManager
from scripts.mechanics.mechanics import attempt_transfer
from scripts.components.equipment_component import EquipmentComponent
from scripts.system.exceptions import (
    ItemNotFoundError,
    StorageLimitItemsError,
    FileNotFoundError,
    ArmorNonEquippableItemError,
    ArmorNotFoundInInventoryError,
    ArmorInsufficientParameterError,
    WeaponNonEquippableItemError, 
    WeaponNotFoundInInventoryError,
    WeaponNotAvailableHandsError,
    WeaponNotEquipedError,
    EquipmentError
) 

# ===============================
# ITEMS AND STORAGE
# ===============================

def test_generate_item():
    """
    Gererate a simple item
    """
    Item(item_id = "next_city_ticket" ,name = "Next City ticket", category = "obligatory" , lore =  { "common_use" : "required to enter city X"} )


def test_read_csv_files():
    """
    Make the item library
    """
    item_factory = ItemManager()
    item_factory.load_all()


def test_format_read_csv_files():
    """
    Make the item library
    """
    factory = ItemManager(base_path = "tests/schemas/data/info")
    factory.load_all(structure = {
        "equipment": ["armor", "weapon"],
        "item": ["consumable"]
    })


def test_read_wrong_csv_files():
    """
    Try to make item library with wrongs values
    """
    item_factory = ItemManager()
    with pytest.raises(FileNotFoundError):
       item_factory.load_all(structure = {"Wrong_csv": ["WrongFile1", "WrongFile2"]})


def test_spawn_item(test_item_factory):
    """
    Spawn a correct item
    """
    test_item_factory.spawn("clan_dagger")


def test_spawn_wrong_item(test_item_factory):
    """
    error when exporting a non-existent item
    """
    with pytest.raises(ItemNotFoundError):
        test_item_factory.spawn("wrong_item")


def test_storage_items(test_item_factory, simple_dagger, normal_chest):
    """
    Add and remove items in a storage
    """
    armor = normal_chest.get_component("inventory").add_item(test_item_factory.spawn("padded_armor"))[0]
    normal_chest.get_component("inventory").add_item(simple_dagger)

    normal_chest.get_component("inventory").remove_item(simple_dagger)
    normal_chest.get_component("inventory").remove_item(armor)


def test_bad_storage(simple_dagger, simple_chest):
    """
    Test add and remove wrong items, more items than storage limit.
    """
    # 1. Add wrong item
    assert simple_chest.get_component("inventory").add_item("WrongItem")[0] == None 
    # with pytest.raises(ItemNotFoundError): /---/
    #     simple_chest.get_component("inventory").add_item("WrongItem")

    # 2. Remove non-existent item
    with pytest.raises(ItemNotFoundError):
        simple_chest.get_component("inventory").remove_item("WrongItem")

    # 3. Exceed storage limit
    simple_chest.get_component("inventory").add_item(simple_dagger)
    simple_chest.get_component("inventory").add_item(simple_dagger)

    assert simple_chest.get_component("inventory").add_item(simple_dagger)[0] == None 
    # with pytest.raises(StorageLimitItemsError): /---/
    #     simple_chest.get_component("inventory").add_item(simple_dagger)

    
def test_transfer_items(simple_entity, simple_char, simple_dagger, simple_chest, normal_chest):
    """
    Transfer objects between two storages and two entities
    """
    simple_entity.get_component("inventory").add_item(simple_dagger)

    attempt_transfer(simple_entity , simple_char   , simple_dagger.name)
    attempt_transfer(simple_char   , simple_chest  , simple_dagger)
    attempt_transfer(simple_chest  , normal_chest  , simple_dagger)
    attempt_transfer(normal_chest  , simple_entity , simple_dagger.name)

    assert len(simple_entity.get_component("inventory").items) == 1
    assert len(simple_char.get_component("inventory").items)   == 0
    assert len(simple_chest.get_component("inventory").items)  == 0
    assert len(normal_chest.get_component("inventory").items)  == 0


def test_bad_transfer_items(simple_entity, simple_dagger, simple_chest):
    """
    Transfer objects between two storages and two entities
    """
    with pytest.raises(StorageLimitItemsError):
        for _ in range(simple_chest.get_component("inventory").capacity+1):
            simple_entity.get_component("inventory").add_item(simple_dagger)
            attempt_transfer(simple_entity , simple_chest, simple_dagger)

    with pytest.raises(ItemNotFoundError):
        attempt_transfer(simple_entity , simple_chest, "Wrong Item")

    # The last item return
    assert len(simple_entity.get_component("inventory").items) == 1


# ===============================
# EQUIPMENT
# ===============================
def test_equip_armor(simple_entity, simple_armor, explorer_armor):
    """
    Add and equip armors to a entity.
    """
    # Check armor and entity status
    assert simple_entity.get_component("equipment").equipment['armor'] == None
    assert simple_armor.status   == None
    assert explorer_armor.status == None

    # Add and equip armor to entity
    simple_entity.get_component("inventory").add_item(simple_armor)
    simple_entity.get_component("inventory").add_item(explorer_armor)
    simple_entity.get_component("equipment").equip_armor(explorer_armor)
    simple_entity.get_component("equipment").equip_armor(simple_armor)

    # Check armor and entity status
    assert simple_entity.get_component("equipment").equipment['armor'] == simple_armor
    assert explorer_armor.status == None
    assert simple_armor.status   == "equiped"


def test_equip_wrong_armor(simple_entity, simple_armor, heavy_armor,simple_dagger):
    """
    Trying to equip armor and weapons incorrectly .
    """
    with pytest.raises(ArmorNotFoundInInventoryError):
        simple_entity.get_component("equipment").equip_armor(simple_armor)

    with pytest.raises(ArmorNotFoundInInventoryError):
        simple_entity.get_component("equipment").equip_armor("some armor name")
    
    # Add items to entity
    simple_entity.get_component("inventory").add_item(heavy_armor)
    simple_entity.get_component("inventory").add_item(simple_dagger)

    with pytest.raises(ArmorNonEquippableItemError):
        simple_entity.get_component("equipment").equip_armor(simple_dagger)
    
    with pytest.raises(ArmorInsufficientParameterError):
        simple_entity.get_component("equipment").equip_armor(heavy_armor)


def test_equip_weapon(simple_entity, simple_dagger, longspear, simple_shield):
    """
    Add and equip weapon to a entity.
    """
    simple_dagger_copy = copy.deepcopy(simple_dagger)

    # Check armor and entity status
    assert simple_dagger.status      == None
    assert simple_dagger_copy.status == None
    assert longspear.status          == None

    # Add, equip, check weapons to entity
    simple_entity.get_component("inventory").add_item(simple_dagger)
    simple_entity.get_component("inventory").add_item(simple_dagger_copy)
    simple_entity.get_component("inventory").add_item(longspear)
    simple_entity.get_component("inventory").add_item(simple_shield)
    simple_entity.get_component("equipment").equip_weapon_on_hand(simple_dagger)

    assert simple_entity.get_component("equipment").equipment['hands'] == [simple_dagger, None]
    assert simple_dagger.status   == "equiped"

    simple_entity.get_component("equipment").equip_weapon_on_hand(simple_dagger_copy)
    assert simple_entity.get_component("equipment").equipment['hands'] == [simple_dagger, simple_dagger_copy]
    assert simple_dagger_copy.status        == "equiped"

    simple_entity.get_component("equipment").unequip_weapon_on_hand(simple_dagger)
    assert simple_entity.get_component("equipment").equipment['hands'] == ["weapon_unarmed" or None, simple_dagger_copy]
    assert simple_dagger.status             == None

    simple_entity.get_component("equipment").unequip_weapon_on_hand(simple_dagger_copy)
    assert simple_entity.get_component("equipment").equipment['hands'] == ["weapon_unarmed" or None, "weapon_unarmed" or None]
    assert simple_dagger_copy.status        == None

    simple_entity.get_component("equipment").equip_weapon_on_hand(longspear)
    assert simple_entity.get_component("equipment").equipment['hands'] == [longspear, "holding_weapon"]
    assert longspear.status                 == "equiped"

    simple_entity.get_component("equipment").unequip_weapon_on_hand(longspear)

     # Check armor and entity status
    assert simple_entity.get_component("equipment").equipment['hands'] == ["weapon_unarmed" or None, "weapon_unarmed" or None]
    assert simple_dagger.status      == None
    assert simple_dagger_copy.status == None
    assert longspear.status          == None

    # Equip shield
    simple_entity.get_component("equipment").equip_weapon_on_hand(simple_shield)
    assert simple_entity.get_component("equipment").equipment['hands'] == [simple_shield, "weapon_unarmed" or None]
    assert simple_shield.status             == "equiped"


def test_equip_wrong_weapon(simple_entity, simple_dagger, longspear, imposible_weapon, simple_armor):
    """
    Trying to equip armor and weapons incorrectly .
    """
    simple_dagger_copy = copy.deepcopy(simple_dagger)
    equiped_dagger = copy.deepcopy(simple_dagger)
    equiped_dagger.status = "equiped"
    
    with pytest.raises(WeaponNotFoundInInventoryError):
        simple_entity.get_component("equipment").equip_weapon_on_hand(simple_dagger)

    # Add and equip weapons to entity
    simple_entity.get_component("inventory").add_item(simple_dagger)
    simple_entity.get_component("inventory").add_item(longspear)
    simple_entity.get_component("inventory").add_item(imposible_weapon)
    simple_entity.get_component("inventory").add_item(equiped_dagger)
    simple_entity.get_component("inventory").add_item(simple_armor)
    simple_entity.get_component("equipment").equip_weapon_on_hand(simple_dagger)

    # Equip Errors
    with pytest.raises(WeaponNonEquippableItemError):
        simple_entity.get_component("equipment").equip_weapon_on_hand(simple_armor)

    with pytest.raises(EquipmentError):
        simple_entity.get_component("equipment").equip_weapon_on_hand(equiped_dagger)

    with pytest.raises(WeaponNotAvailableHandsError):
        simple_entity.get_component("equipment").equip_weapon_on_hand(imposible_weapon)

    # Unequip errrors
    with pytest.raises(WeaponNotFoundInInventoryError):
        simple_entity.get_component("equipment").unequip_weapon_on_hand(simple_dagger_copy)
    
    with pytest.raises(WeaponNotEquipedError):
        simple_entity.get_component("equipment").unequip_weapon_on_hand(longspear)
