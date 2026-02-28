
# from scripts.components import InventoryComponent, CombatComponent
# from scripts.components import IdentityComponent

class Entity:
    """
    Base class for all creatures
    """
    def __init__(self, template_id = None):
        self.template_id = template_id
        self.unique_id = None
        self.components = {}
 

    def add_component(self, component):
        self.components[component.component_name] = component

    def get_component(self, component_name):
        return self.components.get(component_name)

    def has_component(self, component_type):
        return component_type in self.components   

    # def __str__(self): 
    #     return f"{self.identity.name} Lv: {self.progression.level} - HP: {self.combat.hit_points_current}/{self.combat.hit_points_max}"


