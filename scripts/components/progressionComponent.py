from scripts.config import MAX_LEVEL 
from scripts.exceptions import (
    EntityLevelLimitError, 
    EntityIsIntegerError, 
    )

class ProgressionComponent:
    component_name = "progression"
    def __init__(self, entity):
        self.entity = entity
        self.level       = 1 # Current level
        self.exp         = 0 # Total current exp

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def level_up(self, force_lvl = False): 
        """
        Arise the entity's level by one
        """
        if self.level < MAX_LEVEL or force_lvl == True: 
            self.level += 1
            self.exp    = 0
        else:
            raise EntityLevelLimitError(self.entity.get_component("identity").name, self.level, MAX_LEVEL)
        return self.level


    def sum_exp(self, value):
        """
        Sum entity expecience
        """
        if not isinstance(value, int):
            raise EntityIsIntegerError("The experience points must be a integer.")
        self.exp = 0 if self.exp + value < 0 else self.exp + value
        return (self.exp)
    
