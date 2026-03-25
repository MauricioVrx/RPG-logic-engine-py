from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult
from scripts.system.resolver.entity_resolver import resolve_entity, resolve_entity_have_capacity
from scripts.system.resolver.item_resolver   import resolve_item


class AddItemAction(Action):
    name = "add_item"

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # Entity 
        entity = resolve_entity(self.state, entity_name)
        if not entity:
            return False, "Entity not found."
        
        # Capacity 
        capacity_available = entity.get_component("inventory").capacity_available()
        if not capacity_available[0]:
            return False, capacity_available[1]

        # Item 
        item = resolve_item(item_name, self.state.item_manager.templates)
        if not item:
            return False, "Invalid item."

        return True, None


    def execute(self):

        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # Spawn item 
        item = self.state.item_manager.spawn(item_name.lower())

        # Get entity
        entity = resolve_entity(self.state, entity_name)

        # Add item
        item_added = entity.get_component("inventory").add_item(item)

        return ActionResult(
            message=f"'{item_name}' added to '{entity.get_component('identity').name}'.",
            data={
                "entity" : entity,
                "item" : item_added
            }
        )


class RemoveItemAction(Action):
    name = "remove_item"
    
    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # Entity validation
        entity = resolve_entity(self.state, entity_name)
        if not entity:
            return False, "Entity not found."

        item_list = [item.key_name for item in entity.get_component('inventory').items]
        # item_list = {item.key_name for item in entity.get_component('inventory').items}

        # Item validation
        if item_name is None or item_name not in item_list:
            return False, f"{item_name} not in {entity_name}'s inventory."

        return True, None


    def execute(self):

        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # Get entity
        entity = resolve_entity(self.state, entity_name)

        # Item validation
        item = resolve_item(item_name, entity.get_component('inventory').items)
        if not item:
            return False, "Invalid item."

        # Remove item
        removed_item = entity.get_component('inventory').remove_item(item)

        return ActionResult(
            message=f"{entity_name}: item '{removed_item.name}' removed.",
            data={
                "entity" : entity,
                "item"   : removed_item
            }
        )

class ListItemAction(Action):
    name = "list_items"

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)

        # Entity validation
        entity = resolve_entity(self.state, entity_name)
        if not entity:
            return False, "Entity not found."

        return True, None


    def execute(self):
        entity_name = self.params.get("entity", None)

        # Get entity
        entity = resolve_entity(self.state, entity_name)

        # ITEM CATEGORY LIST
        dict_items = {}
        for item_category in self.state.item_manager.category_list:
            dict_items[item_category] = []

        # ITEM DICTIONARY
        item_list = entity.get_component("inventory").items
        for item in item_list:
            dict_items[item.category].append(item.name)

        # MESSAGE
        item_message = ""
        for category_name, category_list in dict_items.items():
            if len(category_list) > 0:
                item_message += f"""\n  {category_name} : {', '.join(category_list)}""" 

        # RETURN
        return ActionResult(
            message=f"{entity.get_component('identity').name}'s items ({len(item_list)}/{entity.get_component('inventory').capacity}): {item_message}",
            data={
                "entity"    : entity,
                "item_list" : item_list
            }
        )

class TransferItemAction(Action):
    name = "list_items"
    def validate(self):
        pass
    def execute(self):
        pass