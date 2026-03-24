def find_item_by_name(game_state, name):
    results = []

    results.append(game_state.item_manager.templates[name.lower()])

    return results