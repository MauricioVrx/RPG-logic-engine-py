from scripts.exceptions import (
    StorageLimitItemsError,
    ItemNotFoundError
    )

from scripts.mechanics import add_item as add_it, remove_item as rem_it


class InventoryComponent:
    component_name = "inventory"
    def __init__(self, entity, capacity, weight_limit=None):
        self.entity = entity
        self.capacity = capacity
        self.weight_limit = weight_limit
        self.items = []

    def add_item(self, item_instance, force_add = False):
        
        if len(self.items) >= self.capacity and force_add == False:
            raise StorageLimitItemsError("Capacity reached", self.capacity)

        item = add_it(self, item_instance, force_add)
  
        return item

    def remove_item(self, item_instance):
        for i, stored in enumerate(self.items):
            if stored == item_instance or stored.name == item_instance:
                return rem_it(self, item_instance)

        raise ItemNotFoundError(item_instance)
    
    def get_inventory_desc(self):
        """
        Return a inventory object list from entity  
        """
        return ", ".join([item.name for item in self.items]) or "Empty"
    

    def load_from_dict(self, data, factory):
        for key, value in data.items():
            if key == "items":
                for item in value:
                    self.add_item(factory.spawn(item), force_add = True)
                continue
            if hasattr(self, key):
                setattr(self, key, value)