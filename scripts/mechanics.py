import math
from scripts.item import Item
from scripts.exceptions import (
    DataFrameMultipleRowsError,
    DataFrameRowNotFoundError,
    ItemNotFoundError,
    StorageLimitItemsError
    )

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
    for i, item in enumerate(inventory.inventory):
        if item.name == item_name:
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
