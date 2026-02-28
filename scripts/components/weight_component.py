class WeightComponent:
    component_name = "weight"
    def __init__(self, max_weight):
        self.max_weight = max_weight
        self.current_weight = 0

    def can_add(self, item_weight):
        return self.current_weight + item_weight <= self.max_weight