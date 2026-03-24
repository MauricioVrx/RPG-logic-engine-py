from scripts.actions.base.action_result import ActionResult

class Action:
    """
    Base class for all game actions.
    """

    name = "base_action"

    def __init__(self, state, **kwargs):
        self.state  = state
        self.params = kwargs


    def validate(self):
        """
        Validate if action can be executed.
        """
        return True, None


    def execute(self):
        """
        Execute the action logic.
        """
        raise NotImplementedError


    def run(self):
        """
        Full execution pipeline.
        """
        valid, error = self.validate()

        if not valid:
            return ActionResult(message=error)

        return self.execute()