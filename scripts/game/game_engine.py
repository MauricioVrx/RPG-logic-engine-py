from scripts.world.characters.manager import CharacterManager, CharacterIdentityManager
from scripts.game.game_state          import GameState
from scripts.world.time.game_time     import GameTime
from scripts.world.items.manager      import ItemManager
from scripts.mechanics.time_system    import TimeSystem

class GameEngine:

    def __init__(self):
        self.state = GameState()
        

    def initialize(self):
        """
        Load all data and initialize systems
        """

        # =========================
        # TIME
        # =========================
        game_time = GameTime()
        self.state.time_system = TimeSystem(game_time)

        # =========================
        # MANAGERS
        # =========================
        item_factory = ItemManager()
        item_factory.load_all()

        identity_manager = CharacterIdentityManager()
        identity_manager.load_all_identity()

        character_manager = CharacterManager(
            identity_factory=identity_manager,
            item_factory=item_factory  
        )

        character_manager.load_all("unique")
        character_manager.load_all("template")

        self.state.character_manager = character_manager

        # =========================
        # PLAYER
        # =========================
        player = character_manager.spawn("template", "player_base")
        self.state.player = player