import math
from scripts.items.item import Item


from scripts.exceptions import (
    DataFrameMultipleRowsError,
    ItemNotFoundError,
    StorageLimitItemsError,
    ItemNotRemovedError,
    WeaponNotFoundInInventoryError,
    EquipmentError,
    EntityParameterNotFoundError
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
    Add an object to inventory.
    """
    if not isinstance(item_instance, Item) and not isinstance(item_instance, dict):
        raise ItemNotFoundError(item_instance)

    if len(inventory.items) < inventory.capacity or force_add == True:
        inventory.items.append(item_instance)
        return item_instance
    else:
        raise StorageLimitItemsError(inventory.name, inventory.capacity)


def remove_item(inventory, item_name):
    """
    Remove an object from inventory.
    """
    if  hasattr(item_name, 'status') and item_name.status == 'equiped' :
        raise ItemNotRemovedError(item_name)

    for i, item in enumerate(inventory.items):
        # if item.name == item_name:
        if item == item_name or item.name == item_name:
            return inventory.items.pop(i)
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

    for source_item in source.get_component("inventory").items:
        if isinstance(item, Item) and source_item.name  == item.name :
            item_instance = item
            break
        elif isinstance(item, str) and source_item.name.lower() == item.lower():
            item_instance = source_item
            break
            
    if not item_instance:
        raise ItemNotFoundError(item)

    # 3. Destination Validations (Example: Weight or Capacity)
    if hasattr(target.get_component("inventory"), 'capacity') and len(target.get_component("inventory").items) >= target.get_component("inventory").capacity:
        raise StorageLimitItemsError(target.get_component("identity").name, target.get_component("inventory").capacity)

    # 4. Execution of the movement 
    source.get_component("inventory").remove_item(item_instance)
    success = target.get_component("inventory").add_item(item_instance) 

    if success:
        return True, f"'{item_instance.name}' has been successfully moved."
    else:
        source.get_component("inventory").append(item_instance)
        raise StorageLimitItemsError(target.get_component("identity").name, target.get_component("inventory").capacity)


# ==============================================================
# ENTITY ROLLS | CHECK - FUNCTIONS 
# ==============================================================

throw_d20 = Dice(20)

def critical_roll(dice_result):
    """
    Check whether the dice roll corresponds to a critical success or a critical failure. 
    """
    status = "None"
    if dice_result == throw_d20.sides:
        status = "Critical_Success"
    elif dice_result == 1:
        status = "Critical_Failure"
    return status

def critical_diff(result, cd):
    """Calculate the difference in value between the entity information with roll and the difficulty class."""
    value = result - cd
    return {"result_diff" : value} 


def check_CD(rolled_value, cd, cleared = "passed"):
    """
    Calculate if the roll's result pass the difficulty class.
    """
    result_info =  rolled_value
    result_info[cleared] = False
    if rolled_value['result'] >= cd:
        result_info[cleared] = True

    return result_info | critical_diff(rolled_value['result'], cd)


def format_return_check(dice_result, sum_params):
    """
    Make a dictionary format from throw result . 
    """
    return {"roll" : dice_result, "result" : sum_params , "natural_critical" : critical_roll(dice_result)}


def _parameter_checks(entity, parameter_name, parameter_list , parameter_type="parameter" ,extra = 0):
    """
    Main function for rolls according to parameter type ("Skill", "Saving Throws"). Calculated according to the corresponding formula, without considering Item Bonus and Other Bonuses/Penalties.

    result = 1d20 + Ability Modifier + Proficiency Bonus + extra(plus custom)
    """
    result = 0
    d20_value = throw_d20.roll()
    result += d20_value
    result += extra

    if not parameter_name in parameter_list:
        raise EntityParameterNotFoundError(parameter_name, parameter_type)


    val = 0
    if parameter_type == "Skill":
        val = entity.get_component("ability").get_skill_value(parameter_name)
        result += val
    elif parameter_type == "Saving Throws":
        val =  entity.get_component("ability").get_saving_throws_value(parameter_name)
        result += val

    return  {"type" : parameter_type , "parameter": parameter_name}| format_return_check(d20_value , result)


def skill_checks(entity, parameter_name, extra = 0):
    """
    Calculate the entity's Skill values and roll a 1d20. 

    result = 1d20 + Ability Modifier + Proficiency Bonus + extra(plus custom)
    """
    return _parameter_checks(entity, parameter_name, entity.get_component("ability").skill, "Skill", extra)


def saving_throw_checks(entity, parameter_name, extra = 0):
    """
    Calculate the entity's Saving Throws values and roll a 1d20. 

    result = 1d20 + Ability Modifier + Proficiency Bonus + extra(plus custom)
    """
    return _parameter_checks(entity, parameter_name, entity.get_component("ability").saving_throws, "Saving Throws", extra)


def skill_cd(entity, parameter_name, cd_value, extra = 0):
    """Calculate the skill roll's result, then check if it's higher than difficulty class."""
    result = skill_checks(entity, parameter_name, extra)
    result = check_CD(result, cd_value)
    return result


def saving_throw_cd(entity, parameter_name, cd_value, extra = 0):
    """Calculate the saving throw roll's result, then check if it's higher than difficulty class."""
    result = saving_throw_checks(entity, parameter_name, extra)
    result = check_CD(result, cd_value)
    return result


def attack_roll_checks(entity, weapon, n_attack= 1, distance=False, force = False):
    """
    An entity attempts to attack with its weapon. A penalty will be applied if more attacks have 
    been made in the same turn.
 
    The result of the rolls will determine whether the attack hits or meets the difficulty value.

    Result = 1d20 + Ability Modifier + Weapon proficiency - MAP (Multipe attacks Penalty) 
    """
    if force == False:
        if weapon not in entity.get_component("inventory").items:
        # if weapon not in entity.inventory:
            raise WeaponNotFoundInInventoryError(entity.get_component("identity").name, weapon)
        
        if weapon.status != "equiped":
            raise EquipmentError()

    result = 0


    # Weapon proficiency
    if hasattr(weapon.mechanics, 'weapon_category'): # Weapon
        proficiency_name = weapon.mechanics["weapon_category"]
    else: # Shield
        proficiency_name = "armor_unarmored"

    result += entity.get_component("ability").proficiency_value(proficiency_name) 

    # Ability mod value, Ability modification value, depends on weapon type and distance.
    mod = 0
    if distance: # If is a distance weapon o throw weapon
        mod += entity.get_component("ability").ability_calculation("DEX")
    elif "Finesse" in weapon.traits: # Weapon "Finesse" trait
        mod += max(entity.get_component("ability").ability_calculation("DEX") , entity.get_component("ability").ability_calculation("STR"))
    else: 
        mod += entity.get_component("ability").ability_calculation("STR")

    # MAP (Multipe attacks Penalty) depned of "Agile" trait.
    if "Agile" in weapon.traits:
        penalized_value = 4
    else:
        penalized_value = 5
 
    penalized_value *= (n_attack - 1)

    # Roll 1d20
    roll = throw_d20.roll()

    result += (mod + roll) - penalized_value

    return {"type" : "attack" , "parameter": "weapon"} | format_return_check(roll , result)


def perception_check(entity):
    """
    Calculate the entity's perception values and roll a 1d20. 
    """
    roll = throw_d20.roll()
    entity.get_component("combat").calculate_perception()
    return format_return_check(roll, (entity.get_component("combat").get_perception() + roll))


def armor_class_check(entity):
    """
    returns the entity's armor class
    """
    return entity.get_component("combat").get_armor_class()


def check_impact_attack(attacked_entity , rolled_value):
    """
    Calculate whether the result of the attack equals or exceeds the target's armor class.
    """
    return check_CD(rolled_value, armor_class_check(attacked_entity), cleared="impact_attack")


# ==============================================================
# CHARACTER - FUNCTIONS 
# ==============================================================

def class_cd_check(entity_attack, entity_deffend, param_name, extra = 0):
    """
    Value that enemies must beat with a saving throw to avoid the effects of a 
    entity's special ability.
    """

    class_cd = entity_attack.calculate_class_cd()
    saving_throw = saving_throw_cd(entity_deffend, param_name, class_cd, extra)
    return saving_throw
