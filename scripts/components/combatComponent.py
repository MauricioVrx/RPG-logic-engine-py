from scripts.config  import DEFAULTS_ACTIONS, MAX_DYING_COUNT
from scripts.exceptions import (
    EntityIsIntegerError, 
    )

class CombatComponent:
    component_name = "combat"
    def __init__(self, entity):
        self.entity = entity
        self.entity_hit_points  = 0
        self.hit_points_max     = 0 # Maximum health points of the entity 
        self.hit_points_current = 0 # Current health points of the entity 
        self.dying              = 0 # Counts 
        self.state              = "Stable" # State if is alive, dead or another 
        self.armor_class        = 0 # Difficult a character is to hit in combat
        self.class_cd           = 0 # Specific abilities(from class or creatures) that force other creatures to attempt a saving throw
        self.perception         = 0 # Entity's general awareness and ability to notice their surroundings
        self.actions            = DEFAULTS_ACTIONS.copy()  # Type and count 3 actions, 1 reaction, 1 free action
        self.resistance         = [] # Types of resistance or vulnerability according to level: Vulnerability(>0), Resisitance(<0), Immunity(==0)
        

    def load_from_dict(self, data: dict):
        for key, value in data.items():
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
        Get armor class result
        """

        ac        = self.entity.get_component("ability").ability_calculation('DEX') 
        equipment = self.entity.get_component("equipment").equipment

        if equipment['armor'] in [None, "armor_unarmored"]:
            if type(equipment['armor']) != type(None):
                if ac > equipment['armor']['DEX_cap']:
                    ac = equipment['armor']['DEX_cap']
                
                # Bonus CA 
                ac += equipment['armor']['AC_bonus']
                
                # Armor actegory proficiency
                ac += self.entity.get_component("ability").proficiency_value(equipment['armor']['armor_category'])
            else:
                ac += self.entity.get_component("ability").proficiency_value('armor_unarmored')

        ac += 10  
        self.armor_class = ac
        return ac
