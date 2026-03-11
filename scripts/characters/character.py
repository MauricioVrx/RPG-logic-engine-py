from collections import Counter
from scripts.system import read_json_files
import copy

from scripts.entities.entity import Entity

from scripts.constants import ABILITY_NAMES, ABILITY_SCORE
from scripts.config import FREE_ABILITY_POINTS , BASE_HIT_POINTS

from scripts.exceptions import (
    EntityAbilityNotFoundError,
    EntityParameterNotFoundError, 
    CharacterDisabledParameterError,
    CharacterAbilityLimitExceededError,
    CharacterDuplicateAbilityError,
    CharacterInvalidDistributionError,
    CharacterChangePastError,
    AncestryNotFoundError,
    ClassNotFoundError,
    ClassMainAbilityRequiredError,
    BackgroundNotFoundError,
    BackgroundMinAbilityRequiredError,
)

from scripts.components import (
    EquipmentComponent, 
    IdentityComponent,
    NarrativeComponent, 
    SocialComponent, 
    ProgressionComponent, 
    AbilityComponent, 
    AIComponent, 
    JobComponent, 
    CombatComponent, 
    InventoryComponent
)

# class Character(Entity):
class Character(Entity):
    # def __init__(self):
    def __init__(self, template_id = None, name = None):
        super().__init__(template_id)
        self.add_component(IdentityComponent(self))
        self.add_component(NarrativeComponent(self))
        self.add_component(SocialComponent(self))
        self.add_component(ProgressionComponent(self))
        self.add_component(AbilityComponent(self))
        self.add_component(InventoryComponent(self,capacity=20))
        self.add_component(CombatComponent(self))
        self.add_component(EquipmentComponent(self))
        self.add_component(AIComponent(self))
        self.add_component(JobComponent(self))
        
        self.name = name
        
        self.ancestry        = None 
        self.character_class = None 
        self.background      = None 

        self.lore              = []
        self.magical_aptitude  = []
        self.secondary_ability = []

        # Points for the 4-step boost process
        self._ancestry_boosts   = {}
        self._class_boosts      = {}
        self._background_boosts = {}
        self._free_boosts       = {}

        self._ability_choices = {}

        self.recalculate_all()

    def recalculate_all(self):
        self.get_component("ability").update_parameters_by_ability()
        self.get_component("combat").calculate_armor_class()
        self.get_component("combat").calculate_perception()

    def recalculate_hit_points_max(self):
        base_character_hp = BASE_HIT_POINTS
        ancestry_hp_bonus = 0
        class_hp_bonus = 0

        if self.ancestry != None:
            ancestry_hp_bonus = self.ancestry.hit_points_max
        if self.character_class != None:
            class_hp_bonus = self.character_class.hit_points_max

        self.get_component("combat").hit_points_max = self.get_component("combat").entity_hit_points + base_character_hp + ancestry_hp_bonus + class_hp_bonus

    # ==============================================================
    # ANCESTRY / CLASS / BACKGROUND / FREE - POINTS FUNCTIONS
    # ==============================================================
    def set_ancestry(self, ancestry, extra_abilities = [], identity_list=None, empty_values = False):
        """
        Sets the character's ancestry and applies related boosts and stats.
        """
        ancestry_instance = ancestry
        if isinstance(ancestry_instance, str) and identity_list != None:
            ancestry_instance = identity_list.spawn("ancestry" , ancestry_instance)

        if self.ancestry != None:
            raise CharacterChangePastError(self.get_component("identity").name, 'ancestry')
 
        if not isinstance(ancestry_instance, Ancestry):
            raise AncestryNotFoundError(ancestry_instance)

        if ancestry_instance.status == 0:
            raise CharacterDisabledParameterError(ancestry_instance, 'Ancestry')
        
        if empty_values == False:
            # Validate Free Boosts limit
            # ability_boosts = json.loads(ancestry_instance.ability_boosts)
            ability_boosts = ancestry_instance.ability_boosts
            max_free = ability_boosts.get('FREE', 0)
            if len(extra_abilities) > max_free:
                raise CharacterAbilityLimitExceededError(len(extra_abilities), max_free)

            # Validate against duplicates and existence
            for ability in extra_abilities:
                if ability not in ABILITY_NAMES:
                    raise EntityAbilityNotFoundError(ability)
                if ability in ability_boosts:
                    del ability_boosts['FREE']
                    raise CharacterDuplicateAbilityError(ability, 'Ancestry', ability_boosts)
            
            # Process boosts (1 boost = 2 points)
            base_boosts = {k: v for k, v in ability_boosts.items() if k != 'FREE'}
            final_boost_map = base_boosts | {ability: 1 for ability in extra_abilities}

            # Update ability points
            self.update_character_ability_points()
            self._ancestry_boosts = {ability: val * 2 for ability, val in final_boost_map.items()}
            
            self._ability_choices['ancestry'] = extra_abilities

        # Assign core stats
        self.get_component("identity").speed   += ancestry_instance.speed
        self.get_component("identity").size     = ancestry_instance.size
        self.get_component("identity").trait   += ancestry_instance.trait
        self.get_component("social").sense     += ancestry_instance.sense   
        self.get_component("social").language  += ancestry_instance.language 

        self.ancestry         = ancestry_instance

        self.recalculate_hit_points_max()

        return True


    def set_class(self, class_ins, main_ability, identity_list=None, empty_values = False):
        """
        Sets the character's class and the key ability boost.
        """
        class_instance = class_ins
        if isinstance(class_instance, str) and identity_list != None:
            class_instance = identity_list.spawn("class" , class_instance)

        if self.character_class != None:
            raise CharacterChangePastError(self.get_component("identity").name, 'class')

        if not isinstance(class_instance, CharClass):
            raise ClassNotFoundError(class_instance)
        
        if main_ability not in ABILITY_NAMES:
            raise EntityAbilityNotFoundError(main_ability)

        if class_instance.status == 0:
            raise CharacterDisabledParameterError(class_instance, 'class')

        if main_ability not in class_instance.main_ability:
            raise ClassMainAbilityRequiredError(main_ability, class_instance)
        
        if empty_values == False:
            self._class_boosts   = {main_ability:2}
            self._ability_choices['class'] = [main_ability]

        self.character_class                   = class_instance 
        self.main_ability                      = main_ability 
        self.secondary_ability                += class_instance.secondary_ability
        self.get_component("identity").trait  += class_instance.trait
        self.magical_aptitude                  = class_instance.magical_aptitude

        self.calculate_class_cd()
        self.recalculate_hit_points_max()
        return True

    def set_background(self, background, chosen_boosts = [], identity_list = None, empty_values = False):
        """
        Sets background and applies proficiency in skills/lore.
        """
        background_instance = background
        if isinstance(background_instance, str) and identity_list != None:
            background_instance = identity_list.spawn("background" , background_instance)

        if self.background != None:
            raise CharacterChangePastError(self.get_component("identity").name, 'background')

        if not isinstance(background_instance, Background):
            raise BackgroundNotFoundError(background_instance)

        if background_instance.status == 0:
            raise CharacterDisabledParameterError(background_instance, 'Background')

        if empty_values == False:
            if len(chosen_boosts) > background_instance.boosts_count:
                raise CharacterAbilityLimitExceededError(len(chosen_boosts), background_instance.boosts_count)

            # Validate against duplicates and existence
            for ability in chosen_boosts:
                if ability not in ABILITY_NAMES:
                    raise EntityAbilityNotFoundError(ability)

            # Validate proficiency
            for skill in background_instance.trained_skills:
                if skill not in self.get_component("ability").proficiency_rank: 
                    raise EntityParameterNotFoundError(skill, "skill")
                self.get_component("ability").proficiency_promotion(skill) 

            min_ability_count = 0
            for ability in chosen_boosts: 
                if ability in background_instance.ability:
                    min_ability_count += 1
            if min_ability_count < 1:
                raise BackgroundMinAbilityRequiredError(background_instance, background_instance.ability)
            sum_ability =  {ability: 2 for ability in chosen_boosts}
            if sum(sum_ability.values()) != len(chosen_boosts) * 2:
                raise CharacterInvalidDistributionError(chosen_boosts)

            self._background_boosts = sum_ability


        self.background         = background_instance
        self.lore              += background_instance.trained_lore
        self.get_component("ability").acquired_feats += background_instance.granted_feats

        self._ability_choices['background'] = chosen_boosts
        self.recalculate_hit_points_max()

        # Update ability points
        self.update_character_ability_points()

        return True


    def set_free_ability_points(self, ability_points):
        for ability in ability_points:
            if ability not in ABILITY_NAMES:
                raise EntityAbilityNotFoundError(ability)

        if len(ability_points) > FREE_ABILITY_POINTS:
            raise CharacterAbilityLimitExceededError(len(ability_points), FREE_ABILITY_POINTS)

        sum_ability = {ability:2 for ability in ability_points}

        if sum(sum_ability.values()) != len(ability_points) * 2:
            raise CharacterInvalidDistributionError(ability_points)

        self._free_boosts = sum_ability

        # Update ability points
        self.update_character_ability_points()

        return True
    
    # ==============================================================
    # UPDATE FUNCTIONS
    # ==============================================================

    def update_character_ability_points(self):
        """
        Sum of base, ancestry, class and background and free abilities points on core ability 
        """
        self.get_component("ability").core_ability_score = dict(
            Counter(ABILITY_SCORE) + 
            Counter(self._ancestry_boosts)  + 
            Counter(self._class_boosts)  + 
            Counter(self._background_boosts) + 
            Counter(self._free_boosts)
        )

        # Update dependency values by ability points
        self.get_component("ability").update_parameters_by_ability()
        
        return True


    # ==============================================================
    # CLASS CD - FUNCTIONS
    # ==============================================================
  
    def calculate_class_cd(self): 
        class_cd =  10 + self.get_component("ability").ability_calculation(self.main_ability) + self.get_component("ability").proficiency_value('class_cd')
        self.get_component('combat').class_cd['value'] = class_cd
        return class_cd
        

# ==============================================================
# Character Identity Library :  Ancestry, Class, Background
# ==============================================================
class Ancestry:
    def __init__(self, ancestries_id, name, category = "Ancestry", id_value = None, hit_points_max = None, size = None, speed = None, 
                 ability_boosts = None, trait= None, language= None, sense= None, status= None, 
                 description= None):
        self.id = ancestries_id
        self.name = name
        self.category = category
        self.id_value = id_value
        self.hit_points_max = hit_points_max
        self.speed = speed
        self.size = size
        self.ability_boosts = ability_boosts or {}
        self.trait = trait or []
        self.language = language or []
        self.sense = sense or []
        self.status = status
        self.description = description
    
    def __repr__(self):
        return f"<{self.category.upper()}: {self.name}>"


    def get_stat(self, key, default=None):
        """Safely retrieves a stat from the ancestry."""
        return self.stats.get(key, default)
    
class CharClass:
    def __init__(self, class_id, name, category = "Class", id_value = None, hit_points_max = None, size = None, main_ability = None, 
                 secondary_ability = None, trait= None, magical_aptitude= None, status= None, 
                 ):
        self.id = class_id
        self.name = name
        self.category = category
        self.id_value = id_value
        self.hit_points_max = hit_points_max
        self.main_ability = main_ability
        self.size = size
        self.secondary_ability = secondary_ability or {}
        self.trait = trait or []
        self.magical_aptitude = magical_aptitude or []
        self.status = status 
        
    
    def __repr__(self):
        return f"<{self.category.upper()}: {self.name}>"


    def get_stat(self, key, default=None):
        """Safely retrieves a stat from the class."""
        return self.stats.get(key, default)  

class Background:
    def __init__(self, background_id, name, category = "Background", id_value = None, ability = None, boosts_count = None, trained_skills = None, 
                 trained_lore = None, granted_feats= None, additional_effects= None, status= None, 
                 ):
        self.background_id = background_id
        self.name = name
        self.category = category
        self.id_value = id_value
        self.ability  = ability
        self.boosts_count = boosts_count
        self.trained_skills     = trained_skills or [] 
        self.trained_lore       = trained_lore or []
        self.granted_feats      = granted_feats or []
        self.additional_effects = additional_effects or {}
        self.status = status 
        
    
    def __repr__(self):
        return f"<{self.category.upper()}: {self.name}>"


    def get_stat(self, key, default=None):
        """Safely retrieves a stat from the background."""
        return self.stats.get(key, default)