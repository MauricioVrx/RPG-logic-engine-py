from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult

class WaitAction(Action):
    name = "wait"

    def validate(self):

        hours = self.params.get("hours", 1)

        # Validate correct hour
        if hours <= 0:
            return False, "Invalid number of hours."

        return True, None


    def execute(self):
        hours = self.params.get("hours", 1)

        # Pass hours
        self.state.time_system.pass_hours(hours)

        year, month, day, hour, minute = self.state.time_system.game_time.get_date()
        phase = self.state.time_system.get_day_phase()[1]

        # RETURN
        return ActionResult(
            message=f"You wait for {hours} hour(s).",
            data={
                "time": (year, month, day, hour, minute),
                "phase": phase
            }
        )


class SleepAction(Action):
    name = "sleep"

    def execute(self):

        hours = 8 # Depende of ancestry /---/
        self.state.time_system.pass_hours(hours) 

        year, month, day, hour, minute = self.state.time_system.game_time.get_date()
        phase = self.state.time_system.get_day_phase()[1]

        # RETURNs
        return ActionResult(
            message=f"You sleept for {hours} hour.",
            data={
                "time": (year, month, day, hour, minute),
                "phase": phase
            }
        )
    

class WaitToMorningAction(Action):
    name = "wait_to_morning"

    def execute(self):

        self.state.time_system.pass_to_morning()

        year, month, day, hour, minute = self.state.time_system.game_time.get_date()
        phase = self.state.time_system.get_day_phase()[1]

        # RETURN
        return ActionResult(
            message=f"You waited until morning",
            data={
                "time": (year, month, day, hour, minute),
                "phase": phase
            }
        )