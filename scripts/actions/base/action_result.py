class ActionResult:
    """
    Standard response for all actions.
    """

    def __init__(self, message="", data=None, error=None, events=None):
        self.message = message
        self.data    = data or {}
        self.error   = error
        self.events  = events or []

    def to_dict(self):
        return {
            "message" : self.message,
            "data"    : self.data,
            "error"   : self.error,
            "events"  : self.events
        }