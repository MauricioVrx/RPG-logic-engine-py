from scripts.world.characters.utils import find_npc_by_name

def resolve_entity(game_state, name):

    if name == "player":
        return game_state.player

    npcs = find_npc_by_name(game_state, name)

    if len(npcs) == 1:
        return npcs[0]

    # if len(npcs) > 1:
    #     raise Exception(f"Ambiguous entity: {name}")

    return None

def resolve_entity_have_capacity(entity):
    capacity_available = entity.get_component("inventory").capacity_available()
    if capacity_available[0] == False:
        return None, f"{entity.get_component('identity').name} : insufficient inventory space."
    return True, None