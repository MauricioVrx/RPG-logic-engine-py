from scripts.world.characters.utils import find_npc_by_name
from scripts.world.containers.utils import find_container_by_name

def resolve_entity(name, game_state, multiple = False):

    if name == "player":
        return game_state.player

    entities = find_npc_by_name(game_state, name)

    if len(entities) == 0:
        entities = find_container_by_name(game_state, name)

    if len(entities) == 0:
        pass
    elif multiple == False:
        return entities[0] 
    elif len(entities) >= 1:
        return entities

    # if len(npcs) > 1:
    #     raise Exception(f"Ambiguous entity: {name}")
    return None


def instance_entity_validation(state, entity, name):
    entity_instance = entity
    if isinstance(entity_instance, str):
        entity_instance = resolve_entity(entity, state )
        if entity_instance is None:
            return None, f"Entity '{name}' not found."
        instance = entity_instance
    else:
        instance = entity
    return instance, ""
    

def resolve_entity_have_capacity(entity):
    capacity_available = entity.get_component("inventory").capacity_available()
    if capacity_available[0] == False:
        return None, f"{entity.get_component('identity').name} : insufficient inventory space."
    return True, None