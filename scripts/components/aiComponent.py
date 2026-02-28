class AIComponent:
    component_name = "ai"
    def __init__(self, entity):
        self.entity = entity
        self.ia    = {} # For IA data


    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
