
class IdentityComponent:
    component_name = "identity"
    def __init__(self, entity):
        self.entity = entity
        self.id_entity   = None 
        # self.custom      = False # if has custom values 
        self.type        = ""    # Player, character
        self.name        = ""    # Name of entity
        self.alias       = ""    # Alias of entity
        self.age         = None  # Count of ages
        self.appearance  = ""    # physical appearance
        self.years_old   = ""    # Years old
        self.gender      = 0     # 0 = None, 1 = Male, 2 = Female, 3 = Other
        self.location    = ""    # id o description
        self.trait       = ['general'] # All entity tags 
        self.size        = 2     # Size rank
        self.speed       = 0     # movement in mts

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
