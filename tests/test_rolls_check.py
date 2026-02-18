import pytest
from scripts.exceptions import (
    EntityParameterNotFoundError,
    WeaponNotFoundInInventoryError, 
    EquipmentError
    )

from scripts.mechanics import (
    # Entity
    skill_checks, 
    saving_throw_checks, 
    attack_roll_checks,
    perception_check,
    armor_class_check,
    # CHARACTER
    class_cd_check,
    )

def test_parameter_checks(full_char, mocker):
    """Test successful skill and saving throw rolls."""
    mocker.patch('scripts.dice.random.randint', return_value=12)

    # SKILL TEST
    skill_acrobatics_result = skill_checks(full_char, "Acrobatics")
    assert skill_acrobatics_result[0] == 12
    assert skill_acrobatics_result[1] == 19
    
    skill_intimidation_result = skill_checks(full_char, "Intimidation")
    assert skill_intimidation_result[0] == 12
    assert skill_intimidation_result[1] == 12

    # SAVING THROWS TEST
    saving_throw_fortitude_result = saving_throw_checks(full_char, "fortitude")
    assert saving_throw_fortitude_result[0] == 12
    assert saving_throw_fortitude_result[1] == 11

    saving_throw_reflex_result    = saving_throw_checks(full_char, "reflex")
    assert saving_throw_reflex_result[0] == 12
    assert saving_throw_reflex_result[1] == 16

    saving_throw_will_result      = saving_throw_checks(full_char, "will")
    assert saving_throw_will_result[0] == 12
    assert saving_throw_will_result[1] == 14


def test_wrong_parameter_checks(full_char):
    """Test exceptions during skill and saving throw rolls."""
    # SKILL TEST
    with pytest.raises(EntityParameterNotFoundError):
        skill_checks(full_char, "WrongName")

    # SAVING THROWS TEST
    with pytest.raises(EntityParameterNotFoundError):
        saving_throw_checks(full_char, "WrongName")


def test_attack_roll_checks(full_char, simple_dagger, longspear, mocker):
    """Test successful attacks with two kind of weapons."""
    mocker.patch('scripts.dice.random.randint', return_value=12)

    full_char.add_item(simple_dagger)
    full_char.equip_weapon_on_hand(simple_dagger)

    # 1. Dagger's attack (STR - Finesse)
    attack_1 = attack_roll_checks(full_char, simple_dagger, n_attack=1)
    assert attack_1[0] == 12
    assert attack_1[1] == 14

    attack_2 = attack_roll_checks(full_char, simple_dagger, n_attack=2)
    assert attack_2[0] == 12
    assert attack_2[1] == 10

    attack_3 = attack_roll_checks(full_char, simple_dagger, n_attack=3)
    assert attack_3[0] == 12
    assert attack_3[1] == 6

    # 2. Longspear's attack (STR)
    full_char.unequip_weapon_on_hand(simple_dagger)
    full_char.add_item(longspear)
    full_char.equip_weapon_on_hand(longspear)

    attack_1 = attack_roll_checks(full_char, longspear, n_attack=1)
    assert attack_1[0] == 12
    assert attack_1[1] == 14

    attack_2 = attack_roll_checks(full_char, longspear, n_attack=2)
    assert attack_2[0] == 12
    assert attack_2[1] == 9
    
    attack_3 = attack_roll_checks(full_char, longspear, n_attack=3)
    assert attack_3[0] == 12
    assert attack_3[1] == 4


def test_wrong_attack_roll_checks(full_char, simple_dagger):
    """Test exceptions weapon attacks."""
    # 1. Attacking with a weapon that is not in the inventory.
    with pytest.raises(WeaponNotFoundInInventoryError):
        attack_roll_checks(full_char, simple_dagger, n_attack=1)

    full_char.add_item(simple_dagger)

    # 2. Attacking with a weapon that is not equipped.
    with pytest.raises(EquipmentError):
        attack_roll_checks(full_char, simple_dagger, n_attack=1)


def test_perception_check(full_char, mocker):
    """Test successful perception rolls."""

    mocker.patch('scripts.dice.random.randint', return_value=10)
    perception = perception_check(full_char)
    assert perception[0] == 10
    assert perception[1] == 12


def test_armor_class_check(full_char, simple_armor):
    """Test successful armor class rolls."""
    ac_check = armor_class_check(full_char)
    
    assert ac_check == 14

    full_char.add_item(simple_armor)
    full_char.equip_armor(simple_armor)

    ac_check = armor_class_check(full_char)

    assert ac_check == 14