class LockComponent:
    component_name = "lock"
    def __init__(self, is_locked=False, key_id=None):
        self.is_locked = is_locked
        self.key_id = key_id

    def unlock(self, key):
        if key.id == self.key_id:
            self.is_locked = False
            return True
        return False