from scripts.world.items.utils import find_item_by_name

def resolve_item(item_name, repository, multiple = False):
    item_name = item_name.lower()

    if item_name is None or (isinstance(repository, dict) and item_name not in repository):
        return None 
    
    items = find_item_by_name(repository, item_name)

    if multiple == False:
        return items[0]
    elif len(items) > 1:
        return items

    return None


def instance_item_validation(entity, params, repository):
    item_instance = params["item"]
    if isinstance(item_instance, str):
        list_items = resolve_item(item_instance, repository)

        item = None
        if len(list_items) == 0:
            return None, f"{item_instance} not in {entity.get_component('identity').name}'s inventory."
        for itm in list_items:
            if hasattr(item, 'status') and item.status == 'equiped' :
                continue
            item = itm
            break
        if item == None:
            return None, f"Item '{item}' is equiped."
    
    else:     
        item = params["item"]

    return item, ""

        

# multiple: equip_weapon, remove_item, tranfer items