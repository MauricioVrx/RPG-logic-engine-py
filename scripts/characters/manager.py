from scripts.characters.loader    import CharacterLoader
from scripts.characters.character import Character
from scripts.config import CHARACTER_UNIQUE , CHARACTER_TEMPLATE


class CharacterManager:
    def __init__(self, identity_factory, item_factory, base_path="data/world/entities/characters/"):
        self.loader = CharacterLoader(base_path)
        self.characters          = {}
        self.characters_template = {}
        self.identity_list = identity_factory
        self.item_factory  = item_factory


    def load_all(self , character_list = None):

        if character_list == None or character_list ==  'unique':
            structure = CHARACTER_UNIQUE
            char_dict = self.characters
        else:
            structure = CHARACTER_TEMPLATE
            char_dict = self.characters_template
        
        data = self.loader.load_characters(structure)

        for char_id, info  in data.items():
            char = Character()
            char.unique_id = info['id']
            for component in info['components']:
                if char.components.get(component) != None:
                    if component == "inventory" or component == "equipment":
                        char.components[component].load_from_dict(data = info['components'][component], factory = self.item_factory )
                        continue
                    char.components[component].load_from_dict(info['components'][component])

            if info.get('ancestry') != None:
                ancestry        = info['ancestry'].get('name')
                extra_abilities = info['ancestry'].get('extra_abilities', [])
                identity_list   = self.identity_list
                empty_values    = info['ancestry'].get('empty_values', False)

                char.set_ancestry(ancestry, extra_abilities, identity_list, empty_values)

            if info.get('class') != None:
                class_ins       = info['class'].get('name')
                main_ability    = info['class'].get('main_ability')
                identity_list   = self.identity_list
                empty_values    = info['class'].get('empty_values', False)
                char.set_class(class_ins, main_ability, identity_list, empty_values)
                
            if info.get('background') != None:
                background      = info['background'].get('name')
                chosen_boosts   = info['background'].get('chosen_boosts', [])
                identity_list   = self.identity_list
                empty_values    = info['background'].get('empty_values', False)
                char.set_background(background, chosen_boosts, identity_list, empty_values)

            if info.get('free_ability_points') != None:
                char.set_free_ability_points(info['free_ability_points'].get('ability_points'))
            

            char.recalculate_all()
            char.update_character_ability_points()

            char_dict[char_id] = char