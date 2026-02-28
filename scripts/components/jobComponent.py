class JobComponent:
    component_name = "job"
    def __init__(self, entity):
        self.entity = entity
        self.extra  = {} # For NPC data
        self.job    = {} # For NPC data


    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)