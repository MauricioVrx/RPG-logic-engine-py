class NarrativeComponent:
    """
    Handles Narrative parameters for system and AI use.

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

    backstory : str 
        Previous and start history.

    alignment : str 
        Alignment preferences.

    belief : str 
        If beliebe in something or someone.

    attitude : str 
        Base attitud.

    condition : list 
        Altered conditions .

    like : list 
        Preferences something or someone.

    dislike : list 
        Aversion something or someone.

    ally : list 
        Allied individuals or group.

    enemy : list 
        Enemy individuals or groups.

    Methods
    -------
    load_from_dict(data)
        Loads items from JSON data using the item factory.
    """
    component_name = "narrative"
    def __init__(self, entity):
        self.entity = entity
        self.backstory = "" # Previous and start history
        self.alignment = "" # Alignment preferences
        self.belief    = "" # If beliebe in something or someone
        self.attitude  = "" # Base attitud
        self.condition = [] # Altered conditions 
        self.like      = [] # Preferences something or someone
        self.dislike   = [] # Aversion something or someone
        self.ally      = [] # Allied individuals or group
        self.enemy     = [] # Enemy individuals or groups

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
