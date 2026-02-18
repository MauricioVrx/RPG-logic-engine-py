from scripts.item import Item
from scripts.mechanics import add_item as add_it, remove_item as rem_it

class Container:
    def __init__(self, container_id, name, category="chest", capacity=20, is_locked=False):
        self.id = container_id      # IDK
        self.name = name
        self.category = category    # 'chest', 'wardrobe', 'room_pile'
        self.capacity = capacity
        self.is_locked = is_locked
        self.inventory = []
    
    def __str__(self): 
        return f"<{self.name.upper()} - Status :{self.is_locked} , Inventory :{len(self.inventory)}/{self.capacity}>"

    def add_item(self, item_instance):
        """
        Add an object to container inventory.
        """
        return add_it(self, item_instance)
    
    def remove_item(self, item_instance):
        """
        Remove an object from container inventory.
        """
        return rem_it(self, item_instance)
