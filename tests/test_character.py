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
    BackgroundMinAbilityRequiredError,
    CharacterChangePastError
)

def test_assign_ancestry_valid(simple_char, test_char_factory):
    """Test successful ancestry assignment."""
    simple_char.set_ancestry('gnome', ["INT"], identity_list= test_char_factory)

def test_asign_ancestry(simple_char, test_char_factory):
    """Test exceptions during ancestry assignment."""
    
    # 1. Non-existent ancestry
    with pytest.raises(AncestryNotFoundError):
        simple_char.set_ancestry('G-mono', ["STR"], identity_list= test_char_factory)

    # 2. Exceeding ability boost limit 
    with pytest.raises(CharacterAbilityLimitExceededError):
        simple_char.set_ancestry('gnome', ["WIS", "INT"], identity_list= test_char_factory)

    # 3. Invalid ability name
    with pytest.raises(EntityAbilityNotFoundError):
        simple_char.set_ancestry('gnome', ["Unknown_Ability"], identity_list= test_char_factory)

    # 4. Duplicate boost with a mandatory ancestry ability
    with pytest.raises(CharacterDuplicateAbilityError):
        simple_char.set_ancestry('gnome', ["CON"], identity_list= test_char_factory)

    # 5. Duplicate ancestry instance
    with pytest.raises(CharacterChangePastError):
        simple_char.set_ancestry('human', ["INT", "DEX"], identity_list= test_char_factory)
        simple_char.set_ancestry('gnome', ["INT"], identity_list= test_char_factory)


def test_assign_class_valid(simple_char, test_char_factory):
    """Test successful class assignment."""
    simple_char.set_class('fighter', "STR", identity_list= test_char_factory)


def test_assign_class_exceptions(simple_char, test_char_factory):
    """Test exceptions during class assignment."""

    # 1. Non-existent class
    with pytest.raises(ClassNotFoundError):
        simple_char.set_class('Frigthe', "STR", identity_list= test_char_factory)

    # 2. Invalid ability name
    with pytest.raises(EntityAbilityNotFoundError):
        simple_char.set_class('fighter', "Invalid_Stat", identity_list= test_char_factory)

    # 3. Use an invalid key ability for the class
    with pytest.raises(ClassMainAbilityRequiredError):
        simple_char.set_class('fighter', "WIS", identity_list= test_char_factory)

    # 4. Duplicate class instance
    with pytest.raises(CharacterChangePastError):
        simple_char.set_class('fighter', "STR", identity_list= test_char_factory)
        simple_char.set_class('ranger', "DEX", identity_list= test_char_factory)


def test_assign_background_valid(simple_char, test_char_factory):
    """Test successful class assignment."""
    simple_char.set_background('merchant', ["CHA","WIS"], identity_list= test_char_factory)


def test_assign_background_exceptions(simple_char, test_char_factory):
    """Test exceptions during background assignment."""

    # 1. Non-existent background
    with pytest.raises(BackgroundNotFoundError):
        simple_char.set_background('Merchantee', ["CHA", "WIS"], identity_list= test_char_factory)

    # 2. Exceeding boost limit
    with pytest.raises(CharacterAbilityLimitExceededError):
        simple_char.set_background('merchant', ["CHA", "WIS", "INT"], identity_list= test_char_factory)
    
    # 3. Use an invalid key ability for the background
    with pytest.raises(EntityAbilityNotFoundError):
        assert simple_char.set_background('merchant', ["Wrong_name","WIS"], identity_list= test_char_factory)

    # 4. Minimum mandatory boost not selected (Merchant requires INT or CHA)
    with pytest.raises(BackgroundMinAbilityRequiredError):
        simple_char.set_background('merchant', ["DEX", "WIS"], identity_list= test_char_factory)

    # 5. Duplicate ability selection in background
    with pytest.raises(CharacterInvalidDistributionError):
        simple_char.set_background('merchant', ["INT", "INT"], identity_list= test_char_factory)

    # 6. Duplicate background instance
    with pytest.raises(CharacterChangePastError):
        simple_char.set_background('merchant', ["CHA","WIS"], identity_list= test_char_factory)
        simple_char.set_background('acrobat', ["STR", "WIS"], identity_list= test_char_factory)


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