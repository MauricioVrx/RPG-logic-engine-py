import pytest

from scripts.exceptions import (
    EntityAbilityNotFoundError,
    CharacterAbilityLimitExceededError,
    CharacterDuplicateAbilityError,
    CharacterInvalidDistributionError,
    AncestryNotFoundError,
    ClassNotFoundError,
    ClassMainAbilityRequiredError,
    BackgroundNotFoundError,
    BackgroundMinAbilityRequiredError
)

def test_assign_ancestry_valid(simple_char):
    """Test successful ancestry assignment."""
    simple_char.set_ancestry('Gnome', ["INT"])

def test_asign_ancestry(simple_char):
    """Test exceptions during ancestry assignment."""
    
    # 1. Non-existent ancestry
    with pytest.raises(AncestryNotFoundError):
        simple_char.set_ancestry('G-mono', ["STR"])

    # 2. Exceeding ability boost limit 
    with pytest.raises(CharacterAbilityLimitExceededError):
        simple_char.set_ancestry('Gnome', ["WIS", "INT"])

    # 3. Invalid ability name
    with pytest.raises(EntityAbilityNotFoundError):
        simple_char.set_ancestry('Gnome', ["Unknown_Ability"])

    # 4. Duplicate boost with a mandatory ancestry ability
    with pytest.raises(CharacterDuplicateAbilityError):
        simple_char.set_ancestry('Gnome', ["CON"])


def test_assign_class_valid(simple_char):
    """Test successful class assignment."""
    simple_char.set_class('Fighter', "STR")


def test_assign_class_exceptions(simple_char):
    """Test exceptions during class assignment."""

    # 1. Non-existent class
    with pytest.raises(ClassNotFoundError):
        simple_char.set_class('Frigthe', "STR")

    # 2. Invalid ability name
    with pytest.raises(EntityAbilityNotFoundError):
        simple_char.set_class('Fighter', "Invalid_Stat")

    # 3. Use an invalid key ability for the class
    with pytest.raises(ClassMainAbilityRequiredError):
        simple_char.set_class('Fighter', "WIS")


def test_assign_background_valid(simple_char):
    """Test successful class assignment."""
    simple_char.set_background('Merchant', ["CHA","WIS"])


def test_assign_background_exceptions(simple_char):
    """Test exceptions during background assignment."""

    # 1. Non-existent background
    with pytest.raises(BackgroundNotFoundError):
        simple_char.set_background('Merchantee', ["CHA", "WIS"])

    # 2. Exceeding boost limit
    with pytest.raises(CharacterAbilityLimitExceededError):
        simple_char.set_background('Merchant', ["CHA", "WIS", "INT"])
    
    # 3. Use an invalid key ability for the background
    with pytest.raises(EntityAbilityNotFoundError):
        assert simple_char.set_background('Merchant', ["Wrong_name","WIS"])

    # 4. Minimum mandatory boost not selected (Merchant requires INT or CHA)
    with pytest.raises(BackgroundMinAbilityRequiredError):
        simple_char.set_background('Merchant', ["DEX", "WIS"])

    # 5. Duplicate ability selection in background
    with pytest.raises(CharacterInvalidDistributionError):
        simple_char.set_background('Merchant', ["INT", "INT"])


def test_assign_free_ability_points_valid(simple_char):
    """Test successful ability points assignment."""
    simple_char.set_free_ability_points(["STR", "DEX", "WIS", "INT"])

def test_asign_free_ability_points(simple_char):
    """Test exceptions during final free ability points assignment."""

    # 1. Invalid ability name
    with pytest.raises(EntityAbilityNotFoundError):
        simple_char.set_free_ability_points(["Wrong_name", "DEX", "WIS", "INT"])

    # 2. Exceeding the points limit 
    with pytest.raises(CharacterAbilityLimitExceededError):
        simple_char.set_free_ability_points(["STR", "DEX", "WIS", "INT", "CHA"])

    # 3. Duplicate selection in free points
    with pytest.raises(CharacterInvalidDistributionError):
        simple_char.set_free_ability_points(["STR", "STR", "WIS", "INT"])