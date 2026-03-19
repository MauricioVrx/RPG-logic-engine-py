class IdentityComponent:
    """
    Handles Identity parameters for Entity.

    Responsibilities
    ----------------
    - Contain entity's identity values

    Dependencies
    ------------
    - None

    Attributes
    ----------
    entity : Entity
        Reference to the entity that owns this inventory.

    id_entity : int 
        Unique entity id value.

    type : str
        For identify if is a player, character or other entity.

    name : str
        Name of entity

    alias : str
        For identify if is a player, character or other entity.

    appearance : str
        Physical appearance.

    years_old : int or None
        Count of entity age.

    gender : int
        Entity gender. 0 = None, 1 = Male, 2 = Female, 3.

    location : str
        location id or description.

    trait : list
        List of all entity tags, including ancestry, class, background and others.

    size : int
        size id of size (exampl: ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']).

    speed : int
        Entity movement.

    
    Methods
    -------
    load_from_dict(data)
        Loads items from JSON data using the item factory.
    """
    component_name = "identity"
    def __init__(self, entity):
        self.entity = entity
        self.id_entity   = None 
        self.type        = ""    # Player, character
        self.name        = ""    # Name of entity
        self.alias       = ""    # Alias of entity
        self.appearance  = ""    # physical appearance
        self.years_old   = ""    # Years old
        self.gender      = 0     # 0 = None, 1 = Male, 2 = Female, 3 = Other
        self.location    = ""    # id or description
        self.trait       = ['general'] # All entity tags 
        self.size        = 2     # Size rank
        self.speed       = 0     # movement 

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
