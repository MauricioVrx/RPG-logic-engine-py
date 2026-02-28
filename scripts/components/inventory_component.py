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

    def add_item(self, item_instance):
        if len(self.items) >= self.capacity:
            raise StorageLimitItemsError("Capacity reached", self.capacity)

        item = add_it(self, item_instance)
        # self.items.append(item)
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