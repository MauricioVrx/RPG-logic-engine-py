from scripts.system.exceptions import (
    StorageLimitItemsError,
    ItemNotFoundError
    )

from scripts.mechanics.mechanics import add_item as add_it, remove_item as rem_it

class InventoryComponent:
    """
    Handles item storage for an entity.

    This component allows an entity to store, add, remove and manage items.
    It is used by characters, containers and equipment such as backpacks.

    Responsibilities
    ----------------
    - Store items
    - Enforce capacity limits
    - Provide access to stored items
    - Interact with item factory when loading data

    Dependencies
    ------------
    - ItemFactory (required for loading items)
    - Item class

    Attributes
    ----------
    entity : Entity
        Reference to the entity that owns this inventory.

    capacity : int
        Maximum number of items allowed.

    weight_limit : int
        Maximum number of weight allowed.
    
    items : list
        Collection of stored item instances.

    Methods
    -------
    add_item(item, force_add = False)
        Adds an item to the inventory if capacity allows.

    remove_item(item)
        Removes an item from the inventory.

    get_inventory_desc()
        Return a list of stored items.

    load_from_dict(data, factory)
        Loads items from JSON data using the item factory.
    """

    component_name = "inventory"
    def __init__(self, entity, capacity, weight_limit=None):
        self.entity = entity
        self.capacity = capacity
        self.weight_limit = weight_limit
        self.items = []

    def capacity_available(self):
        if len(self.items) >= self.capacity:
            return False , 0
        return True, self.capacity-len(self.items)

    def add_item(self, item_instance, force_add = False):
        "Adds an item to the inventory if capacity allows."
        # capacty_available = self.capacty_available()
        # if capacty_available[0] == False and force_add == False:
        #     raise StorageLimitItemsError("Capacity reached", self.capacity)

        result = add_it(self, item_instance, force_add)
  
        return result


    def remove_item(self, item_instance):
        "Removes an item from the inventory."
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
        "Loads items from JSON data using the item factory."
        for key, value in data.items():
            if key == "items":
                for item in value:
                    self.add_item(factory.spawn(item), force_add = True)
                continue
            if hasattr(self, key):
                setattr(self, key, value)