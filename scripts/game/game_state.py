class GameState:
    """
    Holds the current state of the game.
    """

    def __init__(self):
        self.npcs        = {}  # All the NPCs in the world
        self.active_npcs = {}  # Enabled NPCs in the current scene
        self.time_system = None

        self.character_manager = None
        self.identity_manager  = None
        self.item_manager      = None

        self.world             = None
        self.player            = None

        self.is_running = True

