from scripts.world.items.utils import find_item_by_name

def resolve_item(item_name, repository):
    item_name = item_name.lower()

    if item_name is None or (isinstance(repository, dict) and item_name not in repository):
        return None 
    

    items = find_item_by_name(repository, item_name)

    if len(items) == 1:
        return items[0]

    # if len(items) > 1:
    #     raise Exception(f"Ambiguous item: {name}")

    return None