
PROF_NAMES = ["Untrained" ,"Trained" ,"Expert" ,"Master" ,"Legendary"]
PROF_SHORT = ["-" ,"Tr" ,"Ex" ,"Ma" ,"Le"]
SIZE_NAME  = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']


# ENTITY 
ABILITY_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
ABILITY_SCORE = {name: 10 for name in ABILITY_NAMES} 

SKILLS       = {'Acrobatics':'DEX','Arcana':'INT','Athletics':'STR','Crafting':'INT','Deception':'CHA','Diplomacy':'CHA','Eterology':'WIS','Intimidation':'CHA','Lore':'INT','Medicine':'WIS','Nature':'WIS','Occultism':'INT','Performance':'CHA','Society':'INT','Stealth':'DEX','Survival':'WIS','Thievery':'DEX'}
SKILLS_BASE  = [(key, value, 0) for key, value in SKILLS.items()]
SKILLS_NAMES = [skill for skill in SKILLS]

SAV_THROWS       = {'fortitude':'CON','reflex':'DEX','will':'WIS'}
SAV_THROWS_BASE  = [(key, value,0) for key, value in SAV_THROWS.items()]
SAV_THROWS_NAMES = [st for st in SAV_THROWS]

PARAMETER_DEPENDENCE = {ability:[[],[]] for ability in ABILITY_NAMES}
{PARAMETER_DEPENDENCE[value][0].append(key) for key, value in SKILLS.items()}
{PARAMETER_DEPENDENCE[value][1].append(key) for key, value in SAV_THROWS.items()}

ARMOR_CLASS = ['armor_unarmored', 'armor_light', 'armor_medium', 'armor_heavy']

PROF_RANG_BASE = {"class_cd" : 0 , "armor_class" : 0, "perception" : 0} | {'weapon_simple' : 0, 'weapon_martial' : 0, 'weapon_advanced' : 0} | {ac :0 for ac in  ARMOR_CLASS} | {skill:0 for skill in SKILLS_NAMES} | {st:0 for st in SAV_THROWS_NAMES}

