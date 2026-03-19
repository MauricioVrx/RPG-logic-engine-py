class SocialComponent:
    component_name = "social"
    def __init__(self, entity):
        self.entity = entity
        self.faction = {} 
        self.language  = [] # Language comprehension 
        self.sense     = [] # Unusual senses

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)