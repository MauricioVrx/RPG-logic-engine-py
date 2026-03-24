from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult
from scripts.world.characters.utils import find_npc_by_name
from scripts.world.items.utils      import find_item_by_name

class AddItemAction(Action):

    name = "add_item"
    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # Entity validation
        if not entity_name == 'player':
            entity = find_npc_by_name(self.state, entity_name)
            if len(entity) == 0:
                return False, "Invalid entity."

        # Item validation
        if item_name is None or item_name not in self.state.item_manager.templates:
            return False, "Invalid item."

        return True, None


    def execute(self):

        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # ITEM
        item = find_item_by_name(self.state, item_name)[0]

        # ENTITY
        if entity_name == 'player':
            entity = self.state.player
        else:
            entity = find_npc_by_name(self.state, entity_name)[0]

        # Add item
        item_added = entity.get_component("inventory").add_item(item)

        return ActionResult(
            message=f"'{item_name}' added to '{entity.get_component('identity').name}'.",
            data={
                "entity" : entity,
                "item" : item_added
            }
        )


class ListItemAction(Action):

    name = "list_items"
    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)

        # Entity validation
        if not entity_name == 'player':
            entity = find_npc_by_name(self.state, entity_name)
            if len(entity) == 0:
                return False, "Invalid entity."

        return True, None


    def execute(self):
        entity_name = self.params.get("entity", None)

        # ENTITY
        if entity_name == 'player':
            entity = self.state.player
        else:
            entity = find_npc_by_name(self.state, entity_name)[0]

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


class RemoveItemAction(Action):
    name = "remove_item"
    
    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)


        # Entity validation
        if entity_name == 'player':
            entity = self.state.player
        else:
            entity = find_npc_by_name(self.state, entity_name)
            if len(entity) == 0:
                return False, "Invalid entity."
            entity = entity[0]

        item_list = [item.key_name for item in entity.get_component('inventory').items]

        # Item validation
        if item_name is None or item_name not in item_list:
            return False, f"{item_name} not in {entity_name}'s inventory."

        return True, None


    def execute(self):

        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)

        # ENTITY
        if entity_name == 'player':
            entity = self.state.player
        else:
            entity = find_npc_by_name(self.state, entity_name)[0]

        # ITEM
        item = next((item for item in entity.get_component('inventory').items if item.name.lower() == item_name.lower() ), None)

        # Remove item
        removed_item = entity.get_component('inventory').remove_item(item)

        return ActionResult(
            message=f"{entity_name}: item '{removed_item.name}' removed.",
            data={
                "entity" : entity,
                "item"   : removed_item
            }
        )