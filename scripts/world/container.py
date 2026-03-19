from scripts.world.entities.entity import Entity
from scripts.world.items.item import Item
from scripts.components.inventory_component import InventoryComponent
from scripts.components.identityComponent import IdentityComponent
from scripts.components.lockComponent import LockComponent

class Container(Entity):
    """
    Represents a world container capable of storing items.

    Containers are entities that exist in the game world and include an
    inventory component used to store items. They can optionally be locked
    using a LockComponent.

    Typical examples include:
        - Chests
        - Wardrobes
        - Ground piles
        - Storage furniture

    Components
    ----------
    IdentityComponent
        Provides basic identity information such as name and identifiers.

    InventoryComponent
        Handles the storage and management of items within the container.

    LockComponent
        Allows the container to be locked or unlocked.

    Attributes
    ----------
    template_id : str
        Identifier used when the container is created from a template.

    name : str
        Display name of the container.

    category : str
        Logical classification of the container type
        (e.g. "chest", "wardrobe", "room_pile").

    capacity : int
        Maximum number of items the container can hold.

    """
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
