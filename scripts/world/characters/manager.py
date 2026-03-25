import copy

from scripts.world.characters.loader    import CharacterLoader, CharacterIdentityLoader
from scripts.world.characters.character import Character, Ancestry, Background, CharClass
from scripts.system.core.loaders_folder_path import CHARACTER_UNIQUE , CHARACTER_TEMPLATE

from scripts.system.exceptions import (
    CharacterNotFoundError,
    CharacterIdentityNotFoundError
)

class CharacterManager:
    """
    Manages the loading, storage and instantiation of character objects.

    This manager loads both unique characters and character templates from
    JSON files using CharacterLoader. Loaded characters are stored internally
    and can be instantiated later using the spawn() method.

    Templates act as blueprints and are deep-copied when a new instance
    is requested.

    Responsibilities:
    - Load character data from JSON files
    - Build Character objects with their components
    - Manage template and unique character collections
    - Spawn independent character instances
    """
    def __init__(self, identity_factory, item_factory, base_path="data/world/entities/characters/"):
        self.loader = CharacterLoader(base_path)
        self.characters          = {}
        self.characters_template = {}
        self.identity_list = identity_factory
        self.item_factory  = item_factory


    def load_all(self , character_list = None):
        """
        Loads character definitions from JSON files.

        Depending on the argument, this method loads either unique characters
        or character templates.

        Parameters
        ----------
        character_list : str | None
            - None or "unique": loads unique characters
            - "template": loads character templates
        """
        template = False
        if character_list is None or character_list ==  'unique':
            structure = CHARACTER_UNIQUE
            char_dict = self.characters
        else:
            template = True
            structure = CHARACTER_TEMPLATE
            char_dict = self.characters_template
        
        data = self.loader.load_characters(structure)

        for char_id, info  in data.items():
            char = Character()
            if template:
                char.template_id = info['id']
            char.unique_id = info['id']

            # ==============================================================
            # COMPONENTS
            # ==============================================================
            for component in info['components']:
                if char.components.get(component) != None:
                    if component == "inventory" or component == "equipment":
                        char.components[component].load_from_dict(data = info['components'][component], factory = self.item_factory )
                        continue
                    char.components[component].load_from_dict(info['components'][component])

            # ==============================================================
            # CHARACTER ANCESTRY
            # ==============================================================
            if info.get('ancestry') != None:
                ancestry        = info['ancestry'].get('name')
                extra_abilities = info['ancestry'].get('extra_abilities', [])
                identity_list   = self.identity_list
                empty_values    = info['ancestry'].get('empty_values', False)

                char.set_ancestry(ancestry, extra_abilities, identity_list, empty_values)

            # ==============================================================
            # CHARACTER CLASS
            # ==============================================================
            if info.get('class') != None:
                class_ins       = info['class'].get('name')
                main_ability    = info['class'].get('main_ability')
                identity_list   = self.identity_list
                empty_values    = info['class'].get('empty_values', False)
                char.set_class(class_ins, main_ability, identity_list, empty_values)
                
            # ==============================================================
            # CHARACTER BACKGROUND
            # ==============================================================
            if info.get('background') != None:
                background      = info['background'].get('name')
                chosen_boosts   = info['background'].get('chosen_boosts', [])
                identity_list   = self.identity_list
                empty_values    = info['background'].get('empty_values', False)
                char.set_background(background, chosen_boosts, identity_list, empty_values)

            # ==============================================================
            # CHARACTER FREE POINTS
            # ==============================================================
            if info.get('free_ability_points') != None:
                char.set_free_ability_points(info['free_ability_points'].get('ability_points'))


            char.recalculate_all()
            char.update_character_ability_points()
            char.recalculate_hit_points_max()
            char.get_component("combat").hit_points_current = char.get_component("combat").hit_points_max

            char_dict[char_id] = char


    def spawn(self, character_type = None, character_name = ''):
        """
        Creates and returns an independent instance of a character.

        The method searches for a template or unique character by name and
        returns a deep copy of the stored object.

        Parameters
        ----------
        character_type : str
            "template" or "unique"

        character_name : str
            Identifier of the character to spawn.
        """
        if character_type is None or character_type == 'template':
            template = self.characters_template.get(character_name)
        elif character_type == 'unique':
            template = self.characters.get(character_name)
        else:
            template = None

        if not template:
            raise CharacterNotFoundError(character_name)
            
        return copy.deepcopy(template) if template else None
    
    
    # /---/ locations system required
    def update_active_npcs(self, game_state):
        """
        /---/
        """
        game_state.active_npcs = {}

        for npc in game_state.npcs.values():
            if npc.location == game_state.current_location:
                npc.is_active = True
                game_state.active_npcs[npc.id] = npc
            else:
                npc.is_active = False


class CharacterIdentityManager:
    """
    Loads and manages character identity data such as ancestries,
    classes and backgrounds.

    These identities represent static game definitions that are used
    during character creation.
    """
    def __init__(self, base_path="data/info"):
        self.loader = CharacterIdentityLoader(base_path)
        self.ancestry   = {}
        self.char_class = {}
        self.background = {}

    def load_all_ancestries(self, file_name= "ancestry"):
        data = self.loader.load_characters_identity("character", file_name)

        for n, info in enumerate(data.items()):
            ancestries_id = info[0]
            ancestry_data = info[1]
            
            status = ancestry_data.get("status", 0)
            if status == 1:
                self.ancestry[ancestries_id] = Ancestry(
                    ancestries_id   = ancestries_id,
                    name            = ancestry_data["name"],
                    id_value        = n,
                    hit_points_max  = ancestry_data["hit_points_max"],
                    speed           = ancestry_data["speed"],
                    size            = ancestry_data.get("size", 2),
                    ability_boosts  = ancestry_data.get("ability_boosts", {}),
                    trait           = ancestry_data.get("trait", []),
                    language        = ancestry_data.get("language", []),
                    sense           = ancestry_data.get("sense", []),
                    status          = ancestry_data.get("status", 0),
                    description     = ancestry_data.get("description", ""),
                )

    def load_all_class(self, file_name= "char_class"):
        data = self.loader.load_characters_identity("character", file_name)

        for n, info in enumerate(data.items()):
            class_id        = info[0]
            char_class_data = info[1]

            status = char_class_data.get("status", 0)
            if status == 1:
                self.char_class[class_id] = CharClass(
                    class_id          = class_id,
                    name              = char_class_data["name"],
                    id_value          = n,
                    hit_points_max    = char_class_data['base_stats']["hit_points_max"],
                    main_ability      = char_class_data["main_ability"],
                    secondary_ability = char_class_data["secondary_ability"],
                    trait             = char_class_data.get("trait", []),
                    magical_aptitude  = char_class_data['magical_progression']['spellcasting_ability'],
                    status            = char_class_data['status'],
                )

    def load_all_background(self, file_name= "background"):

        data = self.loader.load_characters_identity("character", file_name)

        for n, info in enumerate(data.items()):
            background_id   = info[0]
            background_data = info[1]
            
            status = background_data.get("status", 0)
            if status == 1:
                self.background[background_id] = Background(
                    background_id      = background_id,
                    name               = background_data["name"],
                    id_value           = n,
                    ability            = background_data['ability_boosts']["choices"],
                    boosts_count       = background_data["ability_boosts"]['boosts'],
                    trained_skills     = background_data["trained_skills"],
                    trained_lore       = background_data['trained_lore'],
                    granted_feats      = background_data['granted_feats'],
                    additional_effects = background_data['additional_effects'],
                    status             = background_data['status'],
                )

    def load_all_identity(self):
        """
        Load ancestries, classes and backgrounds
        """
        self.load_all_ancestries()
        self.load_all_class()
        self.load_all_background()

    
    def spawn(self, char_identity , name):
        """
        Creates and returns a unique, independent copy of an item.
        """
        if char_identity == "ancestry":
            template = self.ancestry.get(name)
        elif char_identity == "class":
            template = self.char_class.get(name)
        elif char_identity == "background":
            template = self.background.get(name)
        else:
            raise CharacterIdentityNotFoundError(char_identity, name)

        if template:
            # deepcopy ensures the new item doesn't share memory with the template
            return copy.deepcopy(template)