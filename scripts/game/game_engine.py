from scripts.world.characters.manager import CharacterManager, CharacterIdentityManager
from scripts.game.game_state          import GameState
from scripts.world.time.game_time     import GameTime
from scripts.world.items.manager      import ItemManager
from scripts.mechanics.time_system    import TimeSystem

# teporal imports
from scripts.world.containers.container import Container


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
        self.state.identity_manager  = identity_manager
        self.state.item_manager      = item_factory

        # =========================
        # PLAYER
        # =========================
        player = character_manager.spawn("template", "player_base")
        self.state.player = player


        # Temporal - add instances
        print(self.state.character_manager.characters_template)
        usu1= self.state.character_manager.spawn('template', 'city_civile')
        self.state.active_npcs[usu1.template_id] = usu1
        
        usu2= self.state.character_manager.spawn('template', 'city_civile')
        self.state.active_npcs[usu2.template_id] = usu2

        # Temporal containers
        normal_chest = Container("chest1", "Normal Chest 1", capacity=3)
        second_chest = Container("chest2", "Normal Chest 2", capacity=5, locked=True)
        containers = {"template" : {}, "uniques" : {"chest1" : normal_chest, "chest2" : second_chest}}
        self.state.containers  = containers
        self.state.active_containers['chest1'] = normal_chest
        self.state.active_containers['chest2'] = second_chest

        print()
        print(self.state.active_npcs)
        print(self.state.active_containers)
        # print(usu1.template_id)

def find_npc_by_name(game_state, name):
    results = []

    for npc in game_state.active_npcs.values():
        if name.lower() in npc.name.lower():
            results.append(npc)

    return results