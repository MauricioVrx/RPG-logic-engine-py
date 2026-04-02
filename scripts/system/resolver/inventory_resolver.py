from scripts.world.items.utils import find_item_by_name

def resolve_item(item_name, repository, multiple = False):
    item_name = item_name.lower()

    if item_name is None or (isinstance(repository, dict) and item_name not in repository):
        return None 
    
    items = find_item_by_name(repository, item_name)

    if multiple == False:
        return items[0]
    elif len(items) >= 1:
        return items[0]

    return None


def instance_item_validation(entity, params, repository, equiped = False ,multiple = False):
    item_instance = params["item"]
    msg = None
    if isinstance(item_instance, str):
        list_items = resolve_item(item_instance, repository, multiple)
        item = None

        # Components validation
        if entity.has_component('inventory'):
            return None, f"{entity.name} have not an inventory."
            
        if entity.has_component('lock'):
            if entity.get_component('lock').is_locked:
                return None, f"{entity.name}'s inventory is locked."
            
        # Item Validation
        if list_items is None:
            return None, f"Item '{item_instance}' not found."
        
        if list_items is None or len(list_items) == 0:
            return None, f"{item_instance} not in {entity.get_component('identity').name}'s inventory."
        
        for itm in list_items:
            if equiped == True and hasattr(itm, 'status') and itm.status == 'equiped':
                pass
            elif hasattr(itm, 'status') and itm.status == 'equiped' :
                continue
            item = itm
            break

        if item == None and equiped == False:
            return None, f"Item '{item_instance}' is already equiped."
        elif item == None and equiped == True:
            return None, f"Item '{item_instance}' is not equiped."

    elif isinstance(repository, dict):
        msg = "dict"
        item = repository["item"]
    else:     
        msg = "item"
        item = params["item"]
    return item, msg
