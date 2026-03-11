
from scripts.world.entities.entity import Entity
from scripts.world.items.item import Item
from scripts.components.inventory_component import InventoryComponent
from scripts.components.identityComponent import IdentityComponent
from scripts.components.lockComponent import LockComponent

class Container(Entity):
    def __init__(self, template_id = None, name = None, category="chest", capacity=20):
        super().__init__(template_id)
        self.add_component(IdentityComponent(self))
        self.add_component(InventoryComponent(self,capacity=capacity))
        self.add_component(LockComponent(self))
        self.name = name
        self.id = template_id      # IDK

        self.category = category    # 'chest', 'wardrobe', 'room_pile'
    
    def __str__(self): 
        return f"<{self.name.upper()} - Status :{self.is_locked} , Inventory :{len(self.inventory)}/{self.capacity}>"


class Backpack(Item):
    def __init__(self, template_id, name):
        super().__init__(template_id, name= None, category="equipment")
        self.name = name
        self.add_component(InventoryComponent(capacity=15))
