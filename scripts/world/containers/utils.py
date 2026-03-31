def find_container_by_name(game_state, name):
    results = []

    for container in game_state.active_containers.values():
        if name.lower() in container.unique_id.lower():
            results.append(container)

    return results