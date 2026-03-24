def parse_command(command: str):
    
    parts = command.lower().split()

    if not parts:
        return None, {}
    
    action = parts[0]
    # TIME
    if action == "wait":
        return "wait", {"hours": int(parts[1] if len(parts)>=1 else 1)}
    
    # INVENTORY
    if action == "add_item":
        return "add_item", {"entity": parts[1], "item" : parts[2]}
    
    if action == "list_items":
        return "list_items", {"entity": parts[1]}
    
    if action == "remove_item":
        return "remove_item", {"entity": parts[1], "item" : parts[2]}
    
    return action , {}