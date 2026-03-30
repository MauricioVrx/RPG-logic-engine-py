def find_npc_by_name(game_state, name):
    results = []

    print()

    for npc in game_state.active_npcs.values():
        if name.lower() in npc.unique_id.lower():
            results.append(npc)

    return results