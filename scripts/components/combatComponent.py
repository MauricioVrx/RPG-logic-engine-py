
from scripts.game_config.constants  import DEFAULTS_ACTIONS, MAX_DYING_COUNT
from scripts.system.exceptions import (
    EntityIsIntegerError, 
    )

class CombatComponent:
    """
    Handles Combat parameters for Entity.

    This component allows get and calculate an entity combat stats and parameters.

    Responsibilities
    ----------------
    - Contain health, entity state and combat parameters 
    - Calculate and get armor class and perception

    Dependencies
    ------------
    - Ability component (required for Ability entity value)
    - Equipment component (required for calculate armor class)


    Attributes
    ----------
    entity : Entity
        Reference to the entity that owns this inventory.

    entity_hit_points : int 
        health points different to class, ancestry and background values.

    hit_points_max : int
        Maximum health points of the entity.

    hit_points_current : int
        Current health points of the entity.

    dying : int
        Counts of times or turn without hit points.

    state : str
        State if entity is alive, dead or another condition.

    armor_class: dict
        Difficult a character is to hit in combat {"value" : 0, "custom" :0}. 
 
    class_cd: dict
       Specific abilities(from class or creatures) that force other creatures to attempt a saving throw {"value" : 0, "custom" :0}. 

    perception: dict
        Entity's general awareness and ability to notice their surroundings.

    actions : dict
        Actions per turn for character.

    resistance: list
        Types of resistance or vulnerability according to level: Vulnerability(>0), Resisitance(<0), Immunity(==0).

    
    Methods
    -------
    sum_hit_points(value)
        Recovers or damages the entity.

    calculate_armor_class()
        Calculate armor class result.

    get_armor_class()
        Get armor class result.

    calculate_perception()
        Calculate perception result.

    get_perception()
        Get perception result.

    load_from_dict(data)
        Loads items from JSON data using the item factory.
    """
    component_name = "combat"
    def __init__(self, entity):
        self.entity = entity
        self.entity_hit_points  = 0
        self.hit_points_max     = 0 # Maximum health points of the entity 
        self.hit_points_current = 0 # Current health points of the entity 
        self.dying              = 0 # Counts 
        self.state              = "Stable" # State if is alive, dead or another 
        self.armor_class        = {"value" : 0, "custom" :0} # Difficult a character is to hit in combat
        self.class_cd           = {"value" : 0, "custom" :0} # Specific abilities(from class or creatures) that force other creatures to attempt a saving throw
        self.perception         = {"value" : 0, "custom" :0} # Entity's general awareness and ability to notice their surroundings
        self.actions            = DEFAULTS_ACTIONS.copy()  # Type and count 3 actions, 1 reaction, 1 free action
        self.resistance         = [] # Types of resistance or vulnerability according to level: Vulnerability(>0), Resisitance(<0), Immunity(==0)


    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if key == "custom_hit_points":
                self.entity_hit_points  = value
                self.hit_points_max     = value
                self.hit_points_current = value
                continue
            if key == "custom_armor_class":
                self.armor_class['custom'] = value
                continue
            if key == "custom_perception":
                self.perception['custom'] = value
                continue
            if key == "custom_class_cd":
                self.class_cd['custom'] = value
                continue
            if hasattr(self, key):
                setattr(self, key, value)


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
        if self.hit_points_current < self.entity.get_component("ability").get_ability_value("CON") * -1:
            self.state = "Death"

        return previous_hp, self.hit_points_current, self.state


    def calculate_armor_class(self): 
        """
        Calculate armor class result
        """
        ac = self.entity.get_component("ability").ability_calculation('DEX') + 10
        equipment = self.entity.get_component("equipment").equipment
      
        if equipment['armor'] not in [None, "armor_unarmored"]: 
        # if equipment['armor'] not in [None]: 
            if type(equipment['armor']) != type(None): 
                if ac > equipment['armor'].mechanics['dex_cap']:
                    ac = equipment['armor'].mechanics['dex_cap'] + 10

                if self.armor_class['custom'] != 0:
                    ac = self.armor_class['custom']
                
                # Bonus CA 
                ac += equipment['armor'].mechanics['ac_bonus']
                
                # Armor actegory proficiency
                ac += self.entity.get_component("ability").proficiency_value(equipment['armor'].mechanics['armor_category'])
            else:
                ac += self.entity.get_component("ability").proficiency_value('armor_unarmored')
        else:
            if self.armor_class['custom'] != 0: 
                ac = self.armor_class['custom']

        self.armor_class['value'] = ac
        return ac
    

    def get_armor_class(self):
        """
        Get armor class result
        """
        return self.armor_class['value']


    def calculate_perception(self): 
        """
        Calculate perception result
        """
        perception = self.entity.get_component("ability").ability_calculation('WIS')
        if 'perception' in self.entity.get_component("ability").proficiency_rank :
            perception += self.entity.get_component("ability").proficiency_value('perception')
        self.perception['value'] = perception
        return perception
    

    def get_perception(self):
        """
        Get perception result
        """
        if self.armor_class['custom'] != 0:
            return self.perception['custom']
        else:
            return self.perception['value']
        
    
