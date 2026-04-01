from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult
from scripts.system.resolver.entity_resolver import instance_entity_validation
from scripts.system.resolver.inventory_resolver   import instance_item_validation

from scripts.actions.registry import register_action

@register_action("add_item")
class AddItemAction(Action):

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if entity is None:
            return None, msg

        # Item validation
        item, msg = instance_item_validation(entity, self.params, self.state.item_manager.templates)
        if item is None:
            return None, msg
        
        # Validation 
        capacity_available  = entity.get_component("inventory").capacity_available()
        if not (capacity_available[0]):
            return None, capacity_available[1]
        
        # Info
        self.context['entity'] = entity
        self.context['item']   = item if msg is not None else None

        return True, None


    def execute(self):

        entity_name = self.params.get("entity", None)
        item_name   = self.params.get("item", None)
        
        # Item
        if self.context['item'] == None:
            # Spawn item 
            item = self.state.item_manager.spawn(item_name.lower())
        else:
            item = self.context['item']

        # Get entity
        entity = self.context['entity']

        # Add item
        item_added = entity.get_component("inventory").add_item(item)

        return ActionResult(
            message=f"{entity_name}: {item_added[1]}.",
            data={
                "entity" : entity,
                "item"   : item_added[0]
            }
        )

@register_action("remove_item")
class RemoveItemAction(Action):
    
    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if entity is None:
            return False, msg

        # Item validation
        item, msg =instance_item_validation(entity, self.params, entity.get_component('inventory').items)
        if item is None:
            return None, msg
        
        # INFO
        self.context['entity'] = entity
        self.context['item']   = item

        return True, None


    def execute(self):

        entity_name = self.params.get("entity", None)

        # Get entity
        entity = self.context['entity']

        # Get Item
        item = self.context['item']  

        # Remove item
        removed_item = entity.get_component('inventory').remove_item(item)

        return ActionResult(
            message=f"{entity_name}: {removed_item[1]}.",
            data={
                "entity" : entity,
                "item"   : removed_item[0]
            }
        )

@register_action("list_items")
class ListItemAction(Action):

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if entity is None:
            return False, msg
        
        if entity.has_component('lock'):
            if entity.get_component('lock').is_locked:
                return None, f"{entity.name}'s inventory is locked."
        
        # INFO
        self.context['entity'] = entity

        return True, None


    def execute(self):
        entity_name = self.params.get("entity", None)

        # Get entity
        entity = self.context['entity']

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


        if entity.has_component('equipment'):
            item_message += f"\n\nEquipment : {str(entity.get_component('equipment').equipment)}"

        # RETURN
        return ActionResult(
            message=f"{entity_name}'s items ({len(item_list)}/{entity.get_component('inventory').capacity}): {item_message}",
            data={
                "entity"    : entity,
                "item_list" : item_list
            }
        )

@register_action("transfer_item")
class TransferItemAction(Action):

    def validate(self):
        # Empty data validaton
        transfer_from_name = self.params.get("transfer_from", None)
        transfer_to_name   = self.params.get("transfer_to", None)

        # Entity validation
        transfer_from, msg = instance_entity_validation(self.state, self.params["transfer_from"], transfer_from_name)
        if transfer_from is None:
            return None, msg
        
        transfer_to, msg = instance_entity_validation(self.state, self.params["transfer_to"], transfer_to_name)
        if transfer_to is None:
            return None, msg
        
        # Capacity 
        capacity_available = transfer_to.get_component("inventory").capacity_available()
        if not capacity_available[0]:
            return None, capacity_available[1]
        
        # Item validation
        item, msg =instance_item_validation(transfer_from, self.params, transfer_from.get_component('inventory').items)
        if item == None:
            return None, msg

        # INFO
        self.context['transfer_from'] = transfer_from
        self.context['transfer_to']   = transfer_to
        self.context['item']          = item
        
        return True, None


    def execute(self):
        transfer_from_name = self.params.get("transfer_from", None)
        transfer_to_name   = self.params.get("transfer_to", None)
        item_name          = self.params.get("item", None)

        # Remove item
        removed_item = self.context['transfer_from'].get_component('inventory').remove_item(self.context['item'])

        # Add item
        item_added = self.context['transfer_to'].get_component("inventory").add_item(removed_item[0])

        # RETURN
        return ActionResult(
            message=f"{transfer_from_name} -> {transfer_to_name}: '{item_name}' transfered.",
            data={
                "transfer_from"    : self.context['transfer_from'],
                "transfer_to_name" : self.context['transfer_to'],
                "item"             : item_added[0]
            }
        )