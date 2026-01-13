from scripts.constants  import ABILITY_SCORE, PROF_NAMES, PROF_RANG_BASE, SKILLS_BASE, SAV_THROWS_BASE, SKILLS, SAV_THROWS, PARAMETER_DEPENDENCE
from scripts.config     import MAX_LEVEL, DEFAULTS_ACTIONS, MAX_DYING_COUNT
from scripts.mechanics  import calculate_ability_modifier, calculate_proficiency_bonus
from scripts.exceptions import EntityParameterNotFoundError, EntityAbilityNotFoundError, EntityProficiencyNotFoundError, EntityProficiencyLimitError, EntityLevelLimitError, EntityIsIntegerError, EntityDataFormatError

class Entity:
    """
    Base class for all creatures
    """

    def __init__(self):
        self.id_entity   = None 
        self.name        = ""   # Name of entity
        self.alias       = ""   # Alias of entity
        self.age         = None # Count of ages
        self.appearance  = ""   # physical appearance
        self.level       = 1 # Current level
        self.exp         = 0 # Total current exp
        self.dying       = 0 # Counts 
        self.speed       = 0 # movement in mts

        self.state = "Stable" # State if is alive, dead or another 

        self.backstory = "" # Previous and start history
        self.alignment = "" # Alignment preferences
        self.belief    = "" # If beliebe in something or someone
        self.attitude  = "" # Base attitud 

        self.language  = [] # Language comprehension 
        self.sense     = [] # Unusual senses
        
        self.like      = [] # Preferences something or someone
        self.dislike   = [] # Aversion something or someone

        self.ally      = [] # Allied individuals or group
        self.enemy     = [] # Enemy individuals or groups

        self.resistance  = [] # Types of resistance or vulnerability according to level: Vulnerability(>0), Resisitance(<0), Immunity(==0)

        self.actions = DEFAULTS_ACTIONS # Type and count 3 actions, 1 reaction, 1 free action
        self.size    = 3                # Size rank

        self.trait     = ['general'] # All entity tags 
        self.condition = []          # Altered conditions 

        self.proficiency_rank   = PROF_RANG_BASE.copy() # Proficiency rank dict  
        self.core_ability_score = ABILITY_SCORE    # Ability
        self.skill              = self.__initial_insert_parameters_points(SKILLS_BASE.copy())     # All Skills with dependences values
        self.saving_throws      = self.__initial_insert_parameters_points(SAV_THROWS_BASE.copy()) # Saving parameters with dependences values

        self.acquired_feats = [] # Feats 
        self.custom_feats   = {} # Feats created just for this entity
        
        self.hit_points_max      = self.core_ability_score["CON"] # Maximum health points of the entity 
        self.hit_points_current  = self.hit_points_max            # Current health points of the entity 
        self.perception          = 0 #  Entity's general awareness and ability to notice their surroundings

        self.armor_class = 0 # Difficult a character is to hit in combat
        self.class_cd    = 0 # Specific abilities(from class or creatures) that force other creatures to attempt a saving throw

        self.inventory = [] # temporal - Inventory of objects


    def __str__(self): 
        return f"{self.name} Lv: {self.level} - HP: {self.hit_points_current}/{self.hit_points_max}"

    def __sum_parameters_points(self, parameters):
        """
        Sum all points for a parameter
        """
        if not isinstance(parameters, dict):
            raise EntityDataFormatError(parameters, dict)
        return sum(parameters.values())


    def get_skill_value(self, name):
        """
        Obtain single skill value
        """
        if name not in self.skill:
            raise EntityParameterNotFoundError(name, "skill")
        return self.__sum_parameters_points(self.skill[name])
    
    def get_saving_throws_value(self, name): 
        """
        Obtain single saving throw value
        """
        if name not in self.saving_throws:
            raise EntityParameterNotFoundError(name, "saving_throws")
        return self.__sum_parameters_points(self.saving_throws[name])


    def proficiency_promotion(self, proficiency_name, force_promotion = False): 
        """
        Ascend one entity's proficiency rank
        """

        if proficiency_name not in self.proficiency_rank:
            raise EntityProficiencyNotFoundError(proficiency_name)
        if self.proficiency_rank[proficiency_name] < len(PROF_NAMES) or force_promotion == True:
            self.proficiency_rank[proficiency_name] += 1
            if proficiency_name in self.skill:
                self.skill[proficiency_name]['proficiency'] = calculate_proficiency_bonus(self.level, self.proficiency_rank[proficiency_name])        
            if proficiency_name in self.saving_throws:
                self.saving_throws[proficiency_name]['proficiency'] = calculate_proficiency_bonus(self.level, self.proficiency_rank[proficiency_name])        
            return self.proficiency_rank[proficiency_name]
        else:
            raise EntityProficiencyLimitError(self.name, proficiency_name, PROF_NAMES[-1])


    def level_up(self, force_lvl = False): 
        """
        Arise the entity's level by one
        """
        if self.level < MAX_LEVEL or force_lvl == True:
            self.level += 1
            self.exp    = 0
        else:
            raise EntityLevelLimitError(self.name, self.level, MAX_LEVEL)
        return self.level


    def sum_exp(self, value):
        """
        Sum entity expecience
        """
        if not isinstance(value, int):
            raise EntityIsIntegerError("The experience points must be a integer.")
        self.exp = 0 if self.exp + value < 0 else self.exp + value
        return (self.exp)


    def sum_hit_points(self, value): 
        """
        Recovers or damages the entity
        """
        if not isinstance(value, int):
            raise EntityIsIntegerError("Damage/Healt points must be a integer.")

        previous_hp = self.hit_points_current

        # Apply change
        self.hit_points_current += value

        # Apply limits
        if self.hit_points_current > self.hit_points_max:
            self.hit_points_current = self.hit_points_max

        # State logic
        if previous_hp > 0 and self.hit_points_current <= 0:
            self.dying += 1
            if self.dying > MAX_DYING_COUNT:
                self.state = "Death"
            else:
                self.state = "Dying"
        elif previous_hp <= 0 and self.hit_points_current > 0:
            self.state = "Stable"
        elif self.state == "Dying" and value < 0:
            self.dying += 1
        if self.hit_points_current < self.core_ability_score["CON"] * -1:
            self.state = "Death"

        return previous_hp, self.hit_points_current, self.state


    def ability_calculation(self, name): 
        """
        Convert ability base points into modifier value
        """
        if name not in self.core_ability_score:
            raise EntityAbilityNotFoundError(name)
        ability_value = self.core_ability_score[name]
        return calculate_ability_modifier(ability_value)


    def proficiency_value(self, name):
        """
        Get proficiency bonus value, by proficiency rank and entity level
        """
        if name not in self.proficiency_rank:
            raise EntityProficiencyNotFoundError(name)
        rank = self.proficiency_rank[name]
        sum_points = calculate_proficiency_bonus(self.level, rank)
        return sum_points
    
    
    def insert_parameter_point(self, ability, proficiency, custom): 
        """
        Insert the parameter points
        """
        parameter = {'mod': self.ability_calculation(ability),'proficiency': self.proficiency_value(proficiency), 'custom' : custom}
        return parameter


    def __initial_insert_parameters_points(self, parameters):  
        """
        insert the parameter points when it's created
        """
        parameters_dict = {}
        for parameter in parameters:
            parameters_dict[parameter[0]] =  self.insert_parameter_point(parameter[1], parameter[0], parameter[2])
        return parameters_dict


    def _update_sub_parameter(self, param_dict, name, custom=None, source_label="parameter"):
        """
        Internal helper to update proficiency and custom bonuses for any parameter dictionary.
        """
        if name not in param_dict:
            raise EntityParameterNotFoundError(name, source_label)
        if name not in self.proficiency_rank:
            raise EntityProficiencyNotFoundError(name)
        
        # Validation
        if custom is not None and not isinstance(custom, int):
            raise EntityIsIntegerError("Custom bonus value must be an integer.")
        
        param_dict[name]['proficiency'] = calculate_proficiency_bonus(self.level, self.proficiency_rank[name])

        # Update values if provided
        if custom is not None:
            param_dict[name]['custom'] = custom


    def update_skill(self, name, custom=None):
        """
        Updates a specific skill's bonuses and recalculates its ability modifier dependency.
        """
        self._update_sub_parameter(self.skill, name, custom, "skill")
        related_ability = SKILLS[name]
        self.skill[name]['mod'] = self.ability_calculation(related_ability)  


    def update_saving_throw(self, name, custom=None):
        """
        Updates a specific saving throw's bonuses and recalculates its modifier.
        """
        self._update_sub_parameter(self.saving_throws, name, custom, "saving_throw")
        related_ability = SAV_THROWS[name]
        self.saving_throws[name]['mod'] = self.ability_calculation(related_ability)


    def set_ability_score(self, name, value):
        """
        Sets a new core ability score and triggers a cascading update for all dependent parameters.
        """
        if name not in self.core_ability_score:
            raise EntityAbilityNotFoundError(name)
        if not isinstance(value, int):
            raise EntityIsIntegerError(f"Ability score for {name} must be an integer.")
        
        self.core_ability_score[name] = value

        # Cascading update using the dependency map
        # idx 0: Skills, idx 1: Saving Throws
        dependencies = PARAMETER_DEPENDENCE.get(name, [[], []])

        for skill_name in dependencies[0]:
            self.update_skill(skill_name)
            
        for save_name in dependencies[1]:
            self.update_saving_throw(save_name)
            
        return self.core_ability_score[name]

