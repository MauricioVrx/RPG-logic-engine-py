def find_item_by_name(repository, item_name):
    results = []
    if isinstance(repository, dict): 
        results.append([repository[item_name.lower()]])
    elif isinstance(repository, list):
        item_list = [item for item in repository if item is not None]
        results.append( [item for item in item_list if item.name.lower() == item_name.lower()])
    return results