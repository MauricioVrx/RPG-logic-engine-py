ACTION_REGISTRY = {}

def register_action(*names):
    def decorator(cls):
        for name in names:
            ACTION_REGISTRY[name] = cls
        return cls
    return decorator