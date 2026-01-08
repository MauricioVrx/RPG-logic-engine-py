
PROF_NAMES = ["Untrained" ,"Trained" ,"Expert" ,"Master" ,"Legendary"]
PROF_SHORT = ["-" ,"Tr" ,"Ex" ,"Ma" ,"Le"]
SIZE_NAME  = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']

ABILITY_NANES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
ABILITY_SCORE = {name: 10 for name in ABILITY_NANES} # ABILITY_SCORE = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}

SKILLS           = [("Acrobatics", 'DEX', 0 ),("Arcana", 'INT', 0 ),("Athletics", 'STR', 0 ),("Crafting", 'INT', 0 ),("Deception", 'CHA', 0 ),("Diplomacy", 'CHA', 0 ),("Eterology", 'WIS', 0 ),("Intimidation", 'CHA', 0 ),("Lore", 'INT', 0 ),("Medicine", 'WIS', 0 ),("Nature", 'WIS', 0 ),("Occultism", 'INT', 0 ),("Performance", 'CHA', 0 ),("Society", 'INT', 0 ),("Stealth", 'DEX', 0 ),("Survival", 'WIS', 0 ),("Thievery", 'DEX', 0 )]
SKILLS_NAMES     = [skill[0] for skill in SKILLS]
SAV_THROWS       = [("fortitude", 'CON', 0), ("reflex", 'DEX', 0), ("will", 'WIS', 0)]
SAV_THROWS_NAMES = [st[0] for st in SAV_THROWS]
PROF_RANG        = {"class_cd" : 0 , "armor_class" : 0, "perception" : 0} | {'weapon_simple' : 0, 'weapon_martial' : 0, 'weapon_advanced' : 0} | {'armor_unarmored': 0, 'armor_light' : 0, 'armor_medium' : 0 , 'armor_heavy' : 0} | {skill:0 for skill in SKILLS_NAMES} | {st:0 for st in SAV_THROWS_NAMES}

