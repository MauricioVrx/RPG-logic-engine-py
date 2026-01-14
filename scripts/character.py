from collections import Counter
from scripts.entity import Entity
from scripts.constants import SIZE_NAME, ABILITY_NAMES
from scripts.config import FREE_ABILITY_POINTS
from scripts.exceptions import (
    EntityAbilityNotFoundError,
    EntityParameterNotFoundError, 
    CharacterDisabledParameterError,
    CharacterAbilityLimitExceededError,
    CharacterDuplicateAbilityError,
    CharacterInvalidDistributionError,
    AncestryNotFoundError,
    ClassNotFoundError,
    ClassMainAbilityRequiredError,
    BackgroundNotFoundError,
    BackgroundMinAbilityRequiredError
)

# Data structures (To be moved to JSON/Database in future sprints)
ANCESTRIES = {
    "Gnomo" :{
        "hit_points_max" : 8,
        "speed"          : 25, 
        "size"           : 1, # Small
        "ability_boosts" : {"CON" : 1, "CHA" : 1 , "STR" : -1, "FREE" : 1},
        "trait"          : ['Gnome' , 'Humanoid'],
        "language"       : ['Common', 'Gnomish', 'Fey'],
        "sense"          : ['Low-Light Vision'],
        "status"         : 1 
    },
    "Human" :{
        "hit_points_max" : 8,
        "speed"          : 25, 
        "size"           : 2, # Medium
        "ability_boosts" : {"FREE" : 2},
        "trait"          : ['Human' , 'Humanoid'],
        "language"       : ['Common', 'FREE'],
        "status"         : 1,
    },
    "Elf" :{
        "hit_points_max" : 6,
        "speed"          : 30, 
        "size"           : 2,
        "ability_boosts" : {"DEX" : 1, "INT" : 1 , "CON" : -1, "FREE" : 1},
        "trait"          : ['Elf' , 'Humanoid'],
        "language"       : ['Common', 'Elven'],
        "sense"          : ['Low-Light Vision'],
        "status"         : 1, 
    },
}

CHARACTER_CLASSES = {
    'Fighter' : {
        "hit_points_max"    : 10,
        "main_ability"      : ["STR", "DEX"],
        "secondary_ability" : ["CON"],
        "trained_skills"    : 3, 
        "trait"             : ['Fighter'],
        "magical_aptitude"  : [],
        "status"            : 1, 
    },
    'Rogue' : {
        "hit_points_max"    : 8,
        "main_ability"      : ["DEX"],
        "secondary_ability" : ["CON", "CHA"],
        "trained_skills"    : 7, 
        "trait"             : ['Rogue'],
        "magical_aptitude"  : [],
        "status"            : 1, 
    },
    'Ranger' : {
        "hit_points_max"    : 10,
        "main_ability"      : ["STR", "DEX"],
        "secondary_ability" : ["CON", "WIS"],
        "trained_skills"    : 4,
        "trait"             : ['Ranger'],
        "magical_aptitude"  : ["WIS"],
        "status"            : 1, 
    },
}

BACKGROUND = {
    "Acrobat" : {
        "ability"      : ["STR", "DEX"], # almost 1 of list + 1 porint free = 2 points
        "boosts_count" : 2,
        "description"  : "In a circus or on the streets, you earned your pay by performing as an acrobat. You might have turned to adventuring when the money dried up, or simply decided to put your skills to better use.",
        "rarity"       : "Common",
        "skills"       : ["Acrobatics"],
        "lore"         : ["Circus"],
        "feat"         : ["Steady Balance"],
        "extra"        : {},
        "status"       : 1, 
    },
    "Hunter" : {
        "ability"      : ["DEX", "WIS"],
        "boosts_count" : 2,
        "description"  : "You stalked and took down animals and other creatures of the wild. Skinning animals, harvesting their flesh, and cooking them were also part of your training, all of which can give you useful resources while you adventure.",
        "rarity"       : "Common",
        "skills"       : ["Survival"],
        "lore"         : ["Tanning"],
        "feat"         : ["Survey Wildlife"],
        "extra"        : {},
        "status"       : 1, 
    },
    "Merchant" : {
        "ability"      : ["INT", "CHA"],
        "boosts_count" : 2,
        "description"  : "In a dusty shop, market stall, or merchant caravan, you bartered wares for coin and trade goods. The skills you picked up still apply in the adventuring life, in which a good deal on a suit of armor could prevent your death.",
        "rarity"       : "Common",
        "skills"       : ["Diplomacy"],
        "lore"         : ["Mercantile"],
        "feat"         : ["Bargain Hunter"],
        "extra"        : {},
        "status"       : 1, 
    },
}

TRAIT = {
    'Gnome'    : {'type' : 'Ancestry', 'description' : 'A creature with this trait is a member of the gnome ancestry. Gnomes are small people skilled at magic who seek out new experiences and usually have low-light vision. An ability with this trait can be used or selected only by gnomes. A weapon with this trait is created and used by gnomes.'},
    'Human'    : {'type' : 'Ancestry', 'description' : 'A creature with this trait is a member of the human ancestry. Humans are a diverse array of people known for their adaptability. An ability with this trait can be used or selected only by humans.'},
    'Elf  '    : {'type' : 'Ancestry', 'description' : 'A creature with this trait is a member of the elf ancestry. Elves are mysterious people with rich traditions of magic and scholarship who typically have low-light vision. An ability with this trait can be used or selected only by elves. A weapon with this trait is created and used by elves.'},
    'Humanoid' : {'type' : 'Creature Type', 'description' : 'Humanoid creatures reason and act much like humans. They typically stand upright and have two arms and two legs.'},

    'Fighter' : {'type' : 'Class', 'description' : 'This indicates abilities from the fighter class.'},
    'Rogue'   : {'type' : 'Class', 'description' : 'This indicates abilities from the rogue class.'},
    'Ranger'  : {'type' : 'Class', 'description' : 'This indicates abilities from the ranger class.'},
}

SENSE = {
    'Low-Light Vision' : {'type' : 'eyes', 'description' : 'A creature with low-light vision can see in dim light as though it were bright light, so it ignores the concealed condition due to dim light.'},
}

class Character(Entity):
    def __init__(self):
        super().__init__()
        self.character_class = None 
        self.ancestry        = None 
        self.background      = None 
        self.lore              = []
        self.magical_aptitude  = []

        self.secondary_ability = []

        # Points for the 4-step boost process
        self.ancestry_boosts   = {}
        self.class_boosts      = {}
        self.background_boosts = {}
        self.free_boosts       = {}


    def set_ancestry(self, name, extra_abilities = []):
        """Sets the character's ancestry and applies related boosts and stats."""
        if name not in ANCESTRIES:
            raise AncestryNotFoundError(name)
        
        info = ANCESTRIES[name].copy() 

        if info.get("status") == 0:
            raise CharacterDisabledParameterError(name, 'Ancestry')

        # Validate Free Boosts limit
        max_free = info["ability_boosts"].get('FREE', 0)
        if len(extra_abilities) > max_free:
            raise CharacterAbilityLimitExceededError(len(extra_abilities), max_free)

        # Validate against duplicates and existence
        for ability in extra_abilities:
            if ability not in ABILITY_NAMES:
                raise EntityAbilityNotFoundError(ability)
            if ability in info["ability_boosts"]:
                del info["ability_boosts"]['FREE']
                raise CharacterDuplicateAbilityError(ability, 'Ancestry', info["ability_boosts"])
       
        # Assign core stats
        self.ancestry = name
        self.hit_points_max += info['hit_points_max']
        self.speed          += info['speed']
        self.size            = info['size']
        self.trait          += info['trait']
        self.sense          += info.get('sense', [])    
        self.language       += info.get('language', []) 

        # Process boosts (1 boost = 2 points)
        base_boosts = {k: v for k, v in info["ability_boosts"].items() if k != 'FREE'}
        final_boost_map = base_boosts | {ability: 1 for ability in extra_abilities}

        self.ancestry_boosts = {ability: val * 2 for ability, val in final_boost_map.items()}

        return True
    

    def set_class(self, name, main_ability):
        """Sets the character class and the key ability boost."""
        if name not in CHARACTER_CLASSES:
            raise ClassNotFoundError(name)

        if main_ability not in ABILITY_NAMES:
            raise EntityAbilityNotFoundError(main_ability)
        
        info = CHARACTER_CLASSES[name].copy() 

        if info.get("status") == 0:
            raise CharacterDisabledParameterError(name, 'Class')

        if main_ability not in info['main_ability']:
            raise ClassMainAbilityRequiredError(main_ability, info['main_ability'])

        self.character_class   = name 
        self.hit_points_max    += info['hit_points_max']
        self.main_ability       = main_ability 
        self.secondary_ability += info['secondary_ability']
        self.trait             += info['trait']
        self.magical_aptitude  += info['magical_aptitude']

        self.class_boosts = {main_ability:2}
        return True


    def set_background(self, name, chosen_boosts):
        """Sets background and applies proficiency in skills/lore."""
        if name not in BACKGROUND:
            raise BackgroundNotFoundError(name)

        info = BACKGROUND[name].copy() 

        if info.get("status") == 0:
            raise CharacterDisabledParameterError(name, 'Background')

        if len(chosen_boosts) > info['boosts_count']:
            raise CharacterAbilityLimitExceededError(len(chosen_boosts), info['boosts_count'])

        # Validate against duplicates and existence
        for ability in chosen_boosts:
            if ability not in ABILITY_NAMES:
                raise EntityAbilityNotFoundError(ability)

        # Validate proficiency
        for skill in info['skills']:
            if skill not in self.proficiency_rank: 
                raise EntityParameterNotFoundError(skill, "skill")
            self.proficiency_promotion(skill) 

        min_ability_count = 0
        for ability in chosen_boosts: 
            if ability in info['ability']:
                min_ability_count += 1
        if min_ability_count < 1:
            raise BackgroundMinAbilityRequiredError(name, info['ability'])
        sum_ability =  {ability: 2 for ability in chosen_boosts}
        if sum(sum_ability.values()) != len(chosen_boosts) * 2:
            raise CharacterInvalidDistributionError(chosen_boosts)


        self.background_boosts = sum_ability
        self.background = name
        self.lore           += info['lore']
        self.acquired_feats += info['feat']

        return True
    

    def set_free_ability_points(self, ability_points):
        for ability in ability_points:
            if ability not in ABILITY_NAMES:
                raise EntityAbilityNotFoundError(ability)

        if len(ability_points) > FREE_ABILITY_POINTS:
            raise CharacterAbilityLimitExceededError(len(ability_points), FREE_ABILITY_POINTS)

        sum_ability = {ability:2 for ability in ability_points}

        if sum(sum_ability.values()) != len(ability_points) * 2:
            raise CharacterInvalidDistributionError(ability_points)

        self.free_boosts = sum_ability

        return True
    

    def set_character_points(self, ancestry, character_class, free_ability_points ,free_points):
        pass
