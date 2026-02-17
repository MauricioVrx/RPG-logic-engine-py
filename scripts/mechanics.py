import math
from scripts.item import Item
from scripts.exceptions import (
    DataFrameMultipleRowsError,
    DataFrameRowNotFoundError,
    ItemNotFoundError,
    StorageLimitItemsError,
    ItemNotRemovedError,
    WeaponNotFoundInInventoryError,
    EquipmentError
    )

from scripts.dice   import Dice

def calculate_ability_modifier(score: int) -> int:
    """Fórmula estándar de Pathfinder 2e para modificadores de atributo."""
    return math.floor((score - 10) / 2)

def calculate_proficiency_bonus(level: int, rank: int) -> int:
    """Calcula el bono de competencia: Nivel + (Rango * 2) si Rango > 0."""
    if rank <= 0:
        return 0
    return level + (rank * 2)

def get_name_df(df, name, column = "name", df_name = "DataFrame"):
    """Get Dataframe row by name"""
    row = df[df[column] == name]
    if len(row) > 1:
        raise DataFrameMultipleRowsError(name, column, df_name)
    elif len(row) == 0:
        return []
    return row.iloc[0]


# ==============================================================
# INVENTORY - FUNCTIONS
# ==============================================================

def add_item(inventory, item_instance, force_add = False):
    """
    Add an object from inventory.
    """
    if not isinstance(item_instance, Item) and not isinstance(item_instance, dict):
        raise ItemNotFoundError(item_instance)

    if len(inventory.inventory) < inventory.capacity or force_add == True:
        inventory.inventory.append(item_instance)
        return True
    else:
        raise StorageLimitItemsError(inventory.name, inventory.capacity)


def remove_item(inventory, item_name):
    """
    Remove an object from inventory.
    """
    if  hasattr(item_name, 'status') and item_name.status == 'equiped' :
        raise ItemNotRemovedError(item_name)

    for i, item in enumerate(inventory.inventory):
        # if item.name == item_name:
        if item == item_name or item.name == item_name:
            return inventory.inventory.pop(i)
    raise ItemNotFoundError(item_name)


def attempt_transfer(source, target, item):
    """
    Attempts to move an object from a source to a destination.
    """
    # 1. Status validations (Example: Is the Chest closed?)
    if hasattr(source, 'is_locked') and source.is_locked:
        return False, f"The container '{source.name}' is locked."

    # 2. Locate the item at the source.
    item_instance = None

    for source_item in source.inventory:
        if isinstance(item, Item) and source_item.name  == item.name :
            item_instance = item
            break
        elif isinstance(item, str) and source_item.name.lower() == item.lower():
            item_instance = source_item
            break
            
    if not item_instance:
        raise ItemNotFoundError(item)

    # 3. Destination Validations (Example: Weight or Capacity)
    if hasattr(target, 'capacity') and len(target.inventory) >= target.capacity:
        raise StorageLimitItemsError(target.name, target.capacity)

    # 4. Execution of the movement 
    source.inventory.remove(item_instance)
    success = target.add_item(item_instance) 

    if success:
        return True, f"'{item_instance.name}' has been successfully moved."
    else:
        source.inventory.append(item_instance)
        raise StorageLimitItemsError(target.name, target.capacity)


# ==============================================================
# ENTITY THROWS - FUNCTIONS 
# ==============================================================

throw_d20 = Dice(20)

def _parameter_checks(parameter_name, parameter_list , parameter_type="parameter" ,extra = 0):
    result = 0
    d20_value = throw_d20.roll()
    result += d20_value
    result += extra

    if not parameter_name in parameter_list:
        pass # /---/ Error

    return d20_value , result


def skill_checks(entity, parameter_name, extra = 0):
    return _parameter_checks(parameter_name, entity.skill, "Skill", extra)


def saving_throw_checks(entity, parameter_name, extra = 0):
    return _parameter_checks(parameter_name, entity.saving_throws, "Saving Throws", extra)


def attack_roll_checks(entity, weapon, n_attack, distance=False, ):
    if hasattr(weapon, 'stats') and 'weapon_category' not in weapon.stats:
        print("Error") # /---/

    if weapon not in entity.inventory:
        raise WeaponNotFoundInInventoryError(entity.name, weapon)
    
    if weapon.status != "equiped":
        raise EquipmentError()

    result = 0
    result += entity.proficiency_value(weapon.stats["weapon_category"]) 

    mod = 0
    if distance:
        mod += entity.core_ability_score["DEX"]
    elif "Finesse" in weapon.stats['trait'].split(", "):
        mod += max(entity.core_ability_score["DEX"] , entity.core_ability_score["STR"])
    else: 
        mod += entity.core_ability_score["STR"]

    if "Agile" in weapon.stats['trait'].split(", "):
        penalized_value = 4
    else:
        penalized_value = 5
    penalized_value *= (n_attack - 1)

    result += (mod + throw_d20.roll()) * penalized_value

    return throw_d20 , result


def perception_check(entity):
    return throw_d20.roll(), entity.calculate_perception() + throw_d20.roll()


def armor_class_check(entity):
    return entity.calculate_armor_class()

# ==============================================================
# CHARACTER THROWS - FUNCTIONS 
# ==============================================================

def class_cd_check(character):
    return throw_d20.roll(), character.calculate_class_cd() + throw_d20.roll()