import pytest
from scripts.system.exceptions import (
    EntityParameterNotFoundError,
    WeaponNotFoundInInventoryError, 
    EquipmentError
    )

from scripts.game_config.constants import SAV_THROWS_NAMES
from scripts.components.equipment_component import EquipmentComponent

from scripts.mechanics.mechanics import (
    # Entity
    skill_checks, 
    saving_throw_checks, 
    attack_roll_checks,
    perception_check,
    armor_class_check,
    check_impact_attack,
    check_CD,
    skill_cd,
    saving_throw_cd,
    # CHARACTER
    class_cd_check,
    )

def test_parameter_checks(full_char, mocker):
    """Test successful skill and saving throw rolls."""
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=12)

    # SKILL TEST
    skill_acrobatics_result = skill_checks(full_char, "Acrobatics")
    assert skill_acrobatics_result['roll']   == 12
    assert skill_acrobatics_result["result"] == 19
    assert check_CD(skill_acrobatics_result, 15)['passed'] == True
    assert skill_cd(full_char, "Acrobatics", 15)['passed'] == True
    
    skill_intimidation_result = skill_checks(full_char, "Intimidation")
    assert skill_intimidation_result['roll']   == 12
    assert skill_intimidation_result["result"] == 12
    assert check_CD(skill_intimidation_result, 15)['passed'] == False
    assert skill_cd(full_char, "Intimidation", 15)['passed'] == False


    # SAVING THROWS TEST
    saving_throw_fortitude_result = saving_throw_checks(full_char, SAV_THROWS_NAMES[0])
    assert saving_throw_fortitude_result['roll']   == 12
    assert saving_throw_fortitude_result["result"] == 11
    assert check_CD(saving_throw_fortitude_result, 15)['passed'] == False
    assert saving_throw_cd(full_char, SAV_THROWS_NAMES[0], 15)['passed'] == False

    saving_throw_reflex_result    = saving_throw_checks(full_char, SAV_THROWS_NAMES[1])
    assert saving_throw_reflex_result['roll']   == 12
    assert saving_throw_reflex_result["result"] == 16
    assert check_CD(saving_throw_reflex_result, 15)['passed'] == True
    assert saving_throw_cd(full_char, SAV_THROWS_NAMES[1], 15)['passed'] == True

    saving_throw_will_result      = saving_throw_checks(full_char, SAV_THROWS_NAMES[2])
    assert saving_throw_will_result['roll']   == 12
    assert saving_throw_will_result["result"] == 14
    assert check_CD(saving_throw_will_result, 15)['passed'] == False
    assert saving_throw_cd(full_char, SAV_THROWS_NAMES[2], 15)['passed'] == False


def test_wrong_parameter_checks(full_char):
    """Test exceptions during skill and saving throw rolls."""
    # SKILL TEST
    with pytest.raises(EntityParameterNotFoundError):
        skill_checks(full_char, "WrongName")

    with pytest.raises(EntityParameterNotFoundError):
        skill_cd(full_char, "WrongName", 15)
   
    # SAVING THROWS TEST
    with pytest.raises(EntityParameterNotFoundError):
        saving_throw_checks(full_char, "WrongName")

    with pytest.raises(EntityParameterNotFoundError):
        saving_throw_cd(full_char, "WrongName", 15)


def test_attack_roll_checks(full_char, npc_human, simple_dagger, longspear, mocker):
    """Test successful attacks with two kind of weapons."""
    full_char.get_component("combat").calculate_armor_class()
    npc_human.get_component("combat").calculate_armor_class()
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=12)

    #Equip weapon> Dagger
    full_char.get_component("inventory").add_item(simple_dagger)
    full_char.get_component("equipment").equip_weapon_on_hand(simple_dagger)

    # 1. Dagger's attack (STR - Finesse)
    attack_1 = attack_roll_checks(full_char, simple_dagger, n_attack=1)
    assert attack_1['roll']   == 12
    assert attack_1["result"] == 14

    attack_2 = attack_roll_checks(full_char, simple_dagger, n_attack=2)
    assert attack_2['roll']   == 12
    assert attack_2["result"] == 10

    attack_3 = attack_roll_checks(full_char, simple_dagger, n_attack=3)
    assert attack_3['roll']   == 12
    assert attack_3["result"] == 6

    # 2. Longspear's attack (STR)
    full_char.get_component("equipment").unequip_weapon_on_hand(simple_dagger)
    full_char.get_component("inventory").add_item(longspear)
    full_char.get_component("equipment").equip_weapon_on_hand(longspear)

    attack_1 = attack_roll_checks(full_char, longspear, n_attack=1)
    assert attack_1['roll']   == 12
    assert attack_1["result"] == 14

    attack_2 = attack_roll_checks(full_char, longspear, n_attack=2)
    assert attack_2['roll']   == 12
    assert attack_2["result"] == 9
    
    attack_3 = attack_roll_checks(full_char, longspear, n_attack=3)
    assert attack_3['roll']   == 12
    assert attack_3["result"] == 4

    impact_1 = check_impact_attack(npc_human, attack_1)
    assert impact_1['natural_critical'] == "None"
    assert impact_1['impact_attack']    == True
    assert impact_1['result_diff']      == 3

    impact_3 = check_impact_attack(npc_human, attack_3)
    assert impact_3['natural_critical'] == "None"
    assert impact_3['impact_attack']    == False
    assert impact_3['result_diff']      == -7

    # Critical success attack
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=20)
    attack_1 = attack_roll_checks(full_char, longspear, n_attack=1)
    assert attack_1['roll']   == 20
    assert attack_1["result"] == 22

    impact = check_impact_attack(npc_human, attack_1)
    assert impact['natural_critical'] == "Critical_Success"
    assert impact['impact_attack']    == True
    assert impact['result_diff']      == 11

    # Critical fail attack
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=1)
    attack_fail = attack_roll_checks(full_char, longspear, n_attack=2)
    assert attack_fail['roll']   == 1
    assert attack_fail["result"] == -2

    impact = check_impact_attack(npc_human, attack_fail)
    assert impact['natural_critical'] == "Critical_Failure"
    assert impact['impact_attack']    == False
    assert impact['result_diff']      == -13


def test_wrong_attack_roll_checks(full_char, simple_dagger):
    """Test exceptions weapon attacks."""
    # 1. Attacking with a weapon that is not in the inventory.
    with pytest.raises(WeaponNotFoundInInventoryError):
        attack_roll_checks(full_char, simple_dagger, n_attack=1)

    full_char.get_component("inventory").add_item(simple_dagger)

    # 2. Attacking with a weapon that is not equipped.
    with pytest.raises(EquipmentError):
        attack_roll_checks(full_char, simple_dagger, n_attack=1)


def test_perception_check(full_char, mocker):
    """Test successful perception rolls."""

    mocker.patch('scripts.mechanics.dice.random.randint', return_value=10)
    perception = perception_check(full_char)
    assert perception['roll']   == 10
    assert perception["result"] == 12


def test_armor_class_check(full_char, simple_armor):
    """Test successful armor class rolls."""
    full_char.get_component("combat").calculate_armor_class()
    ac_check = armor_class_check(full_char)
    
    assert ac_check == 14
    full_char.get_component("inventory").add_item(simple_armor)
    full_char.get_component("equipment").equip_armor(simple_armor)

    full_char.get_component("combat").calculate_armor_class()
    ac_check = armor_class_check(full_char)

    assert ac_check == 14


def test_class_cd_check(full_char, npc_human, mocker):
    """
    Test class cd checks between 2 differents charactes.
    """
    mocker.patch('scripts.mechanics.dice.random.randint', return_value=13)
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[0], 0)['result']      == 13
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[0], 0)['passed']      == False
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[0], 0)['result_diff'] == -1

    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[1], 0)['result']      == 14
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[1], 0)['passed']      == True
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[1], 0)['result_diff'] == 0

    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[2], 0)['result']      == 16
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[2], 0)['passed']      == True
    assert class_cd_check(full_char, npc_human, SAV_THROWS_NAMES[2], 0)['result_diff'] == 2


def test_wrong_class_cd_check(full_char, npc_human):
    """
    Test class cd checks between 2 differents charactes with a wrong saving throw name.
    """
    with pytest.raises(EntityParameterNotFoundError):
        assert class_cd_check(full_char, npc_human, "Wrong_name", 0)['result'] == 10
