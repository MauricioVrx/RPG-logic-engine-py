import json

class Container:
    def __init__(self, container_id, name, category="chest", capacity=20, is_locked=False):
        self.id = container_id      # IDK
        self.name = name
        self.category = category    # 'chest', 'wardrobe', 'room_pile'
        self.capacity = capacity
        self.is_locked = is_locked
        self.inventory = []


    def add_item(self, item_instance):
        if len(self.inventory) < self.capacity:
            self.inventory.append(item_instance)
            return True
        return False # /---/ not space 
    

    def remove_item(self, item_name):
        for i, item in enumerate(self.inventory):
            if item.name == item_name:
                return self.inventory.pop(i)
        return None # /---/ ITEM NOT FOUND
    