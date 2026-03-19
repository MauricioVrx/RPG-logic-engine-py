class GameState:
    """
    Holds the current state of the game.
    """

    def __init__(self):
        self.time_system       = None
        self.character_manager = None
        self.world             = None
        self.player            = None

        self.is_running = True