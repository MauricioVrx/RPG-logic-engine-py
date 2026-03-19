from scripts.game.game_engine import GameEngine

class GameLoop:

    def __init__(self, state):
        self.state = state


    def run(self):
        while self.state.is_running:
            print()
            self.process_input()
            self.update()
            self.render()


    def process_input(self):
        command = input("> ")

        if command == "exit":
            self.state.is_running = False

        elif command == "wait":
            self.state.time_system.pass_hours(1)

        elif command == "sunset":
            self.state.time_system.pass_to_sunset()

        elif command == "sleep":
            self.state.time_system.pass_to_morning()


    def update(self):
        # future:
        # scheduler.update()
        # npc_manager.update()
        # item_manager.update()
        # world_events.update()
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