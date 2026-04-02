from scripts.actions.base.action_result import ActionResult
from scripts.system.exceptions import GameBaseError

class Action:
    """
    Base class for all game actions.
    """

    name = "base_action"

    def __init__(self, state, **kwargs):
        self.state   = state
        self.params  = kwargs
        self.context = {}


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
        try:
            valid, error = self.validate()

            if not valid:
                return ActionResult(message=error)

            return self.execute()
        
        except GameBaseError as e:
            return ActionResult(
                message=str(e),
                data=e.to_dict() if hasattr(e, "to_dict") else {},
                error=True
            )

        except Exception as e:
            return ActionResult(
                message=f"|| Unexpected error occurred : {e}",
                data={"detail": str(e)},
                error=True
            )