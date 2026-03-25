def find_item_by_name(repository, item_name):
    results = []
    if isinstance(repository, dict): 
        item = repository[item_name.lower()]
    elif isinstance(repository, list):
        item = next((item for item in repository if item.name.lower() == item_name.lower() ), None)
        
    results.append(item)

    return results