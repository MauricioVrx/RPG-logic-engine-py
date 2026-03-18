class JobComponent:
    """
    Handles entity job o activity.

    Responsibilities
    ----------------
    - Recopilate jobs category for entirty or character services

    Dependencies
    ------------
    - None

    Attributes
    ----------
    entity : Entity
        Reference to the entity that owns this inventory.

    job : dict
        dict of job activities, example:
        * "vendor": {
            "stock": {
            "torch": {"qty": 10, "price": 1},
            "ration_basic": {"qty": 20, "price": 5},
            "healing_potion_minor": {"qty": 3, "price": 40},
            "dagger": {"qty": 2, "price": 200}
            },
            "bargain_skill": "diplomacy"
        }

    extra : dict
        Dict for custom jobs 
    
    Methods
    -------
    load_from_dict(data)
        Loads items from JSON data using the item factory.
    """
    component_name = "job"
    def __init__(self, entity):
        self.entity = entity
        self.job    = {} # For NPC data
        self.extra  = {} # For NPC data


    def load_from_dict(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)