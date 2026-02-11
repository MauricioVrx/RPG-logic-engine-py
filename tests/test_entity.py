import pytest

from scripts.config import MAX_LEVEL, MAX_DYING_COUNT
from scripts.constants import (
    SKILLS,
    SAV_THROWS,
    PROF_NAMES, 
    PROF_RANG_BASE, 
    SKILLS_NAMES, 
    SAV_THROWS_NAMES, 
    ABILITY_NAMES, 
    PROF_RANG_BASE,
    ABILITY_SCORE,
    PARAMETER_DEPENDENCE,
)

from scripts.exceptions import ( 
    EntityParameterNotFoundError, 
    EntityAbilityNotFoundError, 
    EntityProficiencyNotFoundError, 
    EntityProficiencyLimitError, 
    EntityLevelLimitError, 
    EntityIsIntegerError, 
)

def test_get_skill_value(simple_entity):
    """Test that skills can be retrieved by name and raise error for invalid names."""
    value = simple_entity.get_skill_value(SKILLS_NAMES[0])
    with pytest.raises(EntityParameterNotFoundError):
        assert simple_entity.get_skill_value("Wrong_name")
        assert simple_entity.get_skill_value(0)
    assert value == 0


def test_get_saving_throws_value(simple_entity):
    """Test that saving throws can be retrieved by name and raise error for invalid names."""
    value = simple_entity.get_saving_throws_value(SAV_THROWS_NAMES[0])
    with pytest.raises(EntityParameterNotFoundError):
        assert simple_entity.get_saving_throws_value("Wrong_name")
        assert simple_entity.get_saving_throws_value(0)
    assert value == 0


def test_proficiency_promotion(simple_entity):
    """Verify proficiency rank progression and limit constraints, including forced promotion."""
    first_prof_rank = next(iter(PROF_RANG_BASE))
    
    # Test normal promotion
    simple_entity.proficiency_rank[first_prof_rank] == 0
    simple_entity.proficiency_promotion(first_prof_rank)
    assert simple_entity.proficiency_rank[first_prof_rank] == 1 

    # Test error handling
    with pytest.raises(EntityProficiencyNotFoundError):
        assert simple_entity.proficiency_promotion("Wrong_name")
    
    with pytest.raises(EntityProficiencyLimitError):
        # Set to max rank and try to promote
        simple_entity.proficiency_rank[first_prof_rank] = len(PROF_NAMES)
        simple_entity.proficiency_promotion(first_prof_rank)

    # Test forced promotion beyond normal limits
    simple_entity.proficiency_promotion(first_prof_rank, force_promotion = True)
      

def test_level_up(simple_entity):
    """Test level increment logic and enforcement of MAX_LEVEL limits."""
    level = simple_entity.level_up()
    assert level == 2

    simple_entity.level = MAX_LEVEL
    with pytest.raises(EntityLevelLimitError):
        assert simple_entity.level_up()

    assert simple_entity.level_up(force_lvl = True)


def test_sum_exp(simple_entity):
    """Verify experience points summation, floor at zero, and type validation."""
    assert simple_entity.sum_exp(300)  == 300
    assert simple_entity.sum_exp(-200) == 100
    assert simple_entity.sum_exp(-600) == 0
    with pytest.raises(EntityIsIntegerError):
        assert simple_entity.sum_exp("300")


def test_sum_hit_points_values(simple_entity):
    """Test health calculation for healing and damage while remaining in Stable state."""
    simple_entity.hit_points_max     = 10
    simple_entity.hit_points_current = 5
    simple_entity.sum_hit_points(2)
    assert simple_entity.hit_points_current == 7
    simple_entity.sum_hit_points(-4)
    assert simple_entity.hit_points_current == 3
    assert simple_entity.state == "Stable"

    with pytest.raises(EntityIsIntegerError):
        assert simple_entity.sum_hit_points("3")


def test_dying_by_sum_hit_points(simple_entity):
    """
    Test complex health states: transition to Dying, recovery to Stable, 
    death by Dying count, and instant death by massive damage.
    """
    # 1. Transition to Dying
    simple_entity.dying = 0
    simple_entity.sum_hit_points(-6)
    assert simple_entity.hit_points_current == -1
    assert simple_entity.state == "Dying"
    assert simple_entity.dying == 1

    # 2. Recovery
    simple_entity.sum_hit_points(6)
    assert simple_entity.state == "Stable"

    # 3. Death by Dying counter
    simple_entity.dying = MAX_DYING_COUNT
    simple_entity.sum_hit_points(-9)
    assert simple_entity.state == "Death"

    # 4. Instant Death (Massive Damage Rule)
    simple_entity.dying = 0
    simple_entity.state = "Stable"
    simple_entity.hit_points_current = 1

    # 5. Damage exceeding CON score
    simple_entity.sum_hit_points((simple_entity.get_ability_value("CON") * -1) -100)
    assert simple_entity.state == "Death"
    

def test_ability_calculation(simple_entity):
    """Verify conversion of ability scores to modifiers and handling of missing abilities."""
    assert simple_entity.ability_calculation(ABILITY_NAMES[0]) == 0
    with pytest.raises(EntityAbilityNotFoundError):
        assert simple_entity.ability_calculation("NON_EXISTENT_ABILITY") == 0


def test_proficiency_value(simple_entity):
    """Check proficiency bonus calculation based on rank and level."""
    first_prof_rank = next(iter(PROF_RANG_BASE))
    assert simple_entity.proficiency_value(first_prof_rank) == 0
    with pytest.raises(EntityProficiencyNotFoundError):
        assert simple_entity.proficiency_value("Wrong_name")


def test_set_ability_score(simple_entity):
    """Verify proficiency rank progression and limit constraints, including forced promotion."""
    ability = next(iter(ABILITY_SCORE))

    assert simple_entity.update_extra_ability_score(ability, 4)

    dependencies = PARAMETER_DEPENDENCE.get(ability, [[], []])
    for skill_name in dependencies[0]:
        assert simple_entity.skill[skill_name]['mod'] == 2
    for save_name in dependencies[1]:
        assert simple_entity.saving_throws[save_name]['mod'] == 2

    with pytest.raises(EntityAbilityNotFoundError):
        assert simple_entity.update_extra_ability_score("Wrong_name", 2)


def test_update_and_sum_skill(simple_entity):
    first_prof_rank = next(iter(SKILLS))

    simple_entity.level = 1
    simple_entity.proficiency_rank[first_prof_rank] = 2
    simple_entity.update_skill(first_prof_rank, custom=3)
    assert simple_entity.skill[first_prof_rank]['custom']  == 3

    with pytest.raises(EntityIsIntegerError):
        assert simple_entity.update_skill(first_prof_rank, custom = "3") == 3

    assert simple_entity.get_skill_value(first_prof_rank) == 8


def test_update_and_sum_saving_throws(simple_entity):
    first_prof_rank = next(iter(SAV_THROWS))

    simple_entity.level = 2
    simple_entity.proficiency_rank[first_prof_rank] = 3
    simple_entity.update_saving_throw(first_prof_rank, custom=1)
    assert simple_entity.saving_throws[first_prof_rank]['custom']  == 1

    with pytest.raises(EntityIsIntegerError):
        assert simple_entity.update_saving_throw(first_prof_rank, custom = "3") == 3

    assert simple_entity.get_saving_throws_value(first_prof_rank) == 9


def test_calculate_saving_throws_proficiency_bonus(simple_entity):
    """Verify proficiency rank progression and proficiency value in saving throws."""
    first_prof_rank = list(PROF_RANG_BASE.items())[-1][0]
    
    simple_entity.level = 1
    simple_entity.proficiency_rank[first_prof_rank] == 0
    simple_entity.proficiency_promotion(first_prof_rank)
    assert simple_entity.proficiency_rank[first_prof_rank] == 1

    simple_entity.saving_throws[first_prof_rank]['proficiency'] == 2


def test_simple_calculate_armor_class(simple_entity):
    """Verify a simple calculation of the armor class."""
    simple_entity.calculate_armor_class() == 10