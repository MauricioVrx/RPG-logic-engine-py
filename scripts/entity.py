from scripts.constants import ABILITY_SCORE, PROF_NAMES, PROF_RANG, SKILLS, SAV_THROWS
from scripts.config    import MAX_LEVEL, DEFAULTS_ACTIONS, MAX_DYING_COUNT
from scripts.mechanics import calculate_ability_modifier, calculate_proficiency_bonus

class Entity:
    """
    Base class for all creatures
    """

    def __init__(self, ability = ABILITY_SCORE):
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

        self.traits    = ['general'] # All entity tags 
        self.condition = []          # Altered conditions 

        self.proficiency_rank   = PROF_RANG.copy() # Proficiency rank dict  
        self.core_ability_score = ability          # Ability
        self.skill              = self.calculate_parameters_points(SKILLS.copy())     # All Skills with dependences values
        self.saving_throws      = self.calculate_parameters_points(SAV_THROWS.copy()) # Saving parameters with dependences values

        self.existed_feats = {} # Existed feats 
        self.custom_feats  = {} # Feats created just for this entity
        
        self.hit_points_max      = self.core_ability_score["CON"] # Maximum health points of the entity 
        self.hit_points_current  = self.hit_points_max            # Current health points of the entity 
        self.perception          = 0 #  Entity's general awareness and ability to notice their surroundings

        self.armor_class = 0 # Difficult a character is to hit in combat
        self.class_cd    = 0 # Specific abilities(from class or creatures) that force other creatures to attempt a saving throw

        self.inventory = [] # temporal - Inventory of objects


    def __str__(self):
        return f"{self.name} Lv: {self.level} - HP: {self.hit_points_current}/{self.hit_points_max}"

    def __sum_parameters_points(self, parameters):
        return sum(parameters.values())
    
    def get_skill_value(self, name):
        return self.__sum_parameters_points(self.skill[name])
    
    def get_saving_throws_value(self, name):
        return self.__sum_parameters_points(self.saving_throws[name])

    def proficiency_promotion(self, proficiency_name, force_promotion = False): # /---/ make validation if exist self.proficiency_rank[proficiency_name]
        """Ascend one entity's proficiency rank"""
        if self.proficiency_rank[proficiency_name] < len(PROF_NAMES) or force_promotion == True:
            self.proficiency_rank[proficiency_name] += 1
        else:
            print(f"***ERROR*** {proficiency_name} can't be more than {PROF_NAMES[-1]}")


    def level_up(self, force_lvl = False): # /---/ make validations ans exceptions
        """Arise the entity's level by one"""
        if self.level < MAX_LEVEL or force_lvl == True:
            self.level += 1
            self.exp    = 0
        else:
            print(f"***ERROR*** can't be more than {MAX_LEVEL} lvl")


    def sum_exp(self, value): # /---/ make validations - check isdigit
        """Sum entity expecience"""
        self.exp = 0 if self.exp + value < 0 else self.exp + value
        # /---/ create if exp >= limit, its level_up()
        return (self.exp)


    def sum_hit_points(self, value): # /---/ make validations - check isdigit
        """Recovers or damages the entity"""
        previous_hp = self.hit_points_current

        # Apply change
        self.hit_points_current += value

        # Apply limits
        if self.hit_points_current > self.hit_points_max:
            self.hit_points_current = self.hit_points_max

        # State logic
        # /---/ if self.hit_points_current <= self.core_ability_score["CON"] entity is dead
        if previous_hp > 0 and self.hit_points_current <= 0:
            self.dying += 1
            if self.state > MAX_DYING_COUNT:
                self.state = "Death"
            else:
                self.state = "Dying"
        elif previous_hp <= 0 and self.hit_points_current > 0:
            self.state = "Stable"

        return previous_hp, self.hit_points_current, self.state


    def calculate_parameters_points(self, parameters): # /---/ make validations - 
        """Calculate the parameter points; this is necessary when updating certain proficiency or ability values."""
        parameters_dict = {}
        for parameter in parameters:
            parameters_dict[parameter[0]] =  {'mod': self.ability_calculation(parameter[1]),'proficiency': self.proficiency_value(parameter[0]), 'custom' : parameter[2]}
        return parameters_dict


    def ability_calculation(self, name): # /---/ make validate if exist
        """Convert ability base points into modifier value"""
        ability_value = self.core_ability_score[name]
        return calculate_ability_modifier(ability_value)


    def proficiency_value(self, name): # /---/ make validate if exist
        """Get proficiency bonus value, by proficiency rank and entity level"""
        rank = self.proficiency_rank[name]
        sum_points = calculate_proficiency_bonus(self.level, rank)
        return sum_points


    def update_parameters_points(self): # /---/ make validations - course and return
        """Update entity's main parameters"""
        self.skill          = self.calculate_parameters_points(SKILLS.copy())
        self.saving_throws  = self.calculate_parameters_points(SAV_THROWS.copy())

        # /---/ make validations - exist proficiency 
        self.armor_class    = 10 + self.ability_calculation('DEX') + self.proficiency_value('armor_class') 
        self.class_cd       = 10 + self.level + self.proficiency_value('class_cd') 
        self.perception     = self.level + self.ability_calculation('WIS') + self.proficiency_value('perception')