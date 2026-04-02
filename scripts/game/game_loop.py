from scripts.game.game_engine import GameEngine
from scripts.actions.dispatcher import execute_action
from scripts.actions.parser import parse_command

class GameLoop:

    def __init__(self, state):
        self.state = state


    def run(self):
        while self.state.is_running:
            print()
            self.process_input()
            self.update()
            print()
            self.render()


    def process_input(self):

        command = input("> ")

        action_name, params = parse_command(command)

        if action_name == "exit":
            self.state.is_running = False
            
        result = execute_action(action_name, self.state, **params)

        print(result["message"])


    def update(self):
        # future:
        #    scheduler.update()
        #    npc_manager.update()
        #    item_manager.update()
        #    world_events.update()
        pass


    def render(self):
        year, month, day, hour, minute = self.state.time_system.game_time.get_date()
        phase = self.state.time_system.get_day_phase()[1]

        print(f"Date: {day}/{month}/{year} - {hour:02}:{minute:02}")
        print(f"Phase: {phase}")


if __name__ == "__main__":
    engine = GameEngine()
    engine.initialize()

    loop = GameLoop(engine.state)
    loop.run()