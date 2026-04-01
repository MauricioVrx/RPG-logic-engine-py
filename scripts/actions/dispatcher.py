from scripts.actions.registry import ACTION_REGISTRY

def execute_action(action_name, state, **kwargs):

    action_class = ACTION_REGISTRY.get(action_name)
    
    if not action_class:
        return {
            "message": f"Unknown action: {action_name}",
            "data": {},
            "events": []
        }

    action = action_class(state, **kwargs)
    result = action.run()

    return result.to_dict()