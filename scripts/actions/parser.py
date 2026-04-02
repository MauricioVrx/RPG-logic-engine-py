def parse_command(command: str):
    
    parts = command.lower().split()

    if not parts:
        return None, {}
    
    action = parts[0]
    
    # TIME
    if action == "wait":
        hours = 1
        if len(parts)>1:
            hours = int(parts[1]) if parts[1].isdigit() else None
        return   "wait", {"hours": hours if len(parts)>1 else 1}
    
    if action == "sleep":
        hours = -1
        if  len(parts)>1:
            hours = int(parts[1]) if parts[1].isdigit() else None
        return   "sleep", {"hours": hours}
    
    # INVENTORY
    if action == "add_item":
        return   "add_item", {"entity": parts[1], "item" : parts[2]}
    
    if action == "list_items":
        return   "list_items", {"entity": parts[1]}
    
    if action == "remove_item":
        return   "remove_item", {"entity": parts[1], "item" : parts[2]}
    
    if action == "transfer_item":
        return   "transfer_item", {"transfer_from": parts[1], "transfer_to": parts[2], "item" : parts[3]}
    
    # EQUIPMENT
    if action == "equip_weapon":
        return   "equip_weapon", {"entity": parts[1], "item" : parts[2]}
    
    if action == "unequip_weapon":
        return   "unequip_weapon", {"entity": parts[1], "item" : parts[2]}
    
    # THROWS CHECK
    if action == "skill" or action == "saving_throw":
        if len(parts) == 4:
            cd_value = int(parts[3]) if parts[3].isdigit() else 0
        else:
            cd_value = 0
        return   action, {"type": parts[0], "parameter_name": parts[1], "entity": parts[2], "cd_value": cd_value}
    
    return action , {}