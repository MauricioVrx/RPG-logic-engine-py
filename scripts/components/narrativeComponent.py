class NarrativeComponent:
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
