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
        self.item_factory      = None

        self.world             = None
        self.player            = None

        self.is_running = True


    # /---/ locations system required
    def update_active_npcs(self):
        self.active_npcs = {}

        for npc in self.npcs.values():
            if npc.location == self.current_location:
                npc.is_active = True
                self.active_npcs[npc.id] = npc
            else:
                npc.is_active = False