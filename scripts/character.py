from collections import Counter
from scripts.entity import Entity
from scripts.constants import SIZE_NAME, ABILITY_NAMES
from scripts.config import FREE_ABILITY_POINTS
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
from data.dataframes import (
    df_ancestry  as ancestry, 
    df_char_class as character_class,
    df_background as background, 
)

from scripts.constants import ABILITY_SCORE

from scripts.mechanics import get_name_df
import json

# Data structures (To be moved to JSON/Database in future sprints)

class Character(Entity):
    def __init__(self):
        super().__init__()
        self.character_class = None 
        self.ancestry        = None 
        self.background      = None 
        self.lore              = []
        self.magical_aptitude  = []

        self.secondary_ability = []

        # Points for the 4-step boost process
        self._ancestry_boosts   = {}
        self._class_boosts      = {}
        self._background_boosts = {}
        self._free_boosts       = {}


    # ==============================================================
    # ANCESTRY / CLASS / BACKGROUND / FREE - POINTS FUNCTIONS
    # ==============================================================
    def set_ancestry(self, name, extra_abilities = []):
        """
        Sets the character's ancestry and applies related boosts and stats.
        """
        if self.ancestry != None:
            raise CharacterChangePastError(self.name, 'ancestry')

        info = get_name_df(ancestry, name)

        if len(info) == 0: 
            raise AncestryNotFoundError(name)

        if info.get("status") == 0:
            raise CharacterDisabledParameterError(name, 'Ancestry')
        
        # Validate Free Boosts limit
        ability_boosts = json.loads(info["ability_boosts"])
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
       
        # Assign core stats
        self.hit_points_max += info['hit_points_max']
        self.speed          += info['speed']
        self.size            = info['size']
        self.trait          += info['trait']
   
        if isinstance(info['sense'], list):
            self.sense      += info.get('sense', [])    
        else:
            self.sense = []
        self.language       += info.get('language', []) 

        # Process boosts (1 boost = 2 points)
        base_boosts = {k: v for k, v in ability_boosts.items() if k != 'FREE'}
        final_boost_map = base_boosts | {ability: 1 for ability in extra_abilities}

        self._ancestry_boosts = {ability: val * 2 for ability, val in final_boost_map.items()}
        self.ancestry         = name 

        return True
    

    def set_class(self, name, main_ability):
        """
        Sets the character's class and the key ability boost.
        """
        
        if self.character_class != None:
            raise CharacterChangePastError(self.name, 'class')

        info = get_name_df(character_class, name)

        if len(info) == 0: 
            raise ClassNotFoundError(name)
        
        if main_ability not in ABILITY_NAMES:
            raise EntityAbilityNotFoundError(main_ability)

        if info.get("status") == 0:
            raise CharacterDisabledParameterError(name, 'class')

        if main_ability not in info['main_ability']:
            raise ClassMainAbilityRequiredError(main_ability, info['main_ability'])

        self.character_class   = name 
        self.hit_points_max    += info['hit_points_max']
        self.main_ability       = main_ability 
        self.secondary_ability += info['secondary_ability']
        self.trait             += info['trait']
        # self.magical_aptitude  += info['magical_aptitude']
        if isinstance(info['magical_aptitude'], list):
            self.magical_aptitude  += info.get('magical_aptitude', [])
        else:
            self.magical_aptitude = []

        self._class_boosts   = {main_ability:2}
        self.character_class = name 

        self.calculate_class_cd()

        return True


    def set_background(self, name, chosen_boosts):
        """
        Sets background and applies proficiency in skills/lore.
        """

        if self.background != None:
            raise CharacterChangePastError(self.name, 'background')

        info = get_name_df(background, name)

        if len(info) == 0: 
            raise BackgroundNotFoundError(name)

        if info.get("status") == 0:
            raise CharacterDisabledParameterError(name, 'Background')

        if len(chosen_boosts) > info['boosts_count']:
            raise CharacterAbilityLimitExceededError(len(chosen_boosts), info['boosts_count'])

        # Validate against duplicates and existence
        for ability in chosen_boosts:
            if ability not in ABILITY_NAMES:
                raise EntityAbilityNotFoundError(ability)

        # Validate proficiency
        for skill in info['skills'].split(','):
            if skill not in self.proficiency_rank: 
                raise EntityParameterNotFoundError(skill, "skill")
            self.proficiency_promotion(skill) 

        min_ability_count = 0
        for ability in chosen_boosts: 
            if ability in info['ability']:
                min_ability_count += 1
        if min_ability_count < 1:
            raise BackgroundMinAbilityRequiredError(name, info['ability'])
        sum_ability =  {ability: 2 for ability in chosen_boosts}
        if sum(sum_ability.values()) != len(chosen_boosts) * 2:
            raise CharacterInvalidDistributionError(chosen_boosts)

        self._background_boosts = sum_ability
        self.background         = name
        self.lore           += info['lore']
        self.acquired_feats += info['feat']

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

        return True
    
    # ==============================================================
    # UPDATE FUNCTIONS
    # ==============================================================

    def update_character_ability_points(self):
        """
        Sum of base, ancestry, class and background and free abilities points on core ability 
        """
        self.core_ability_score = dict(
            Counter(ABILITY_SCORE) + 
            Counter(self._ancestry_boosts)  + 
            Counter(self._class_boosts)  + 
            Counter(self._background_boosts) + 
            Counter(self._free_boosts)
        )

        # Update dependency values by ability points
        self.update_parameters_by_ability()
        
        return True


    # ==============================================================
    # CLASS CD - FUNCTIONS
    # ==============================================================
  
    def calculate_class_cd(self): 
        self.class_cd =  10 + self.ability_calculation(self.main_ability) + self.proficiency_value('class_cd')
        return self.class_cd
        
