
PROF_NAMES = ["Untrained" ,"Trained" ,"Expert" ,"Master" ,"Legendary"]
PROF_SHORT = ["-" ,"Tr" ,"Ex" ,"Ma" ,"Le"]
SIZE_NAME  = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']

# ENTITY 
ABILITY_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
ABILITY_SCORE = {name: 10 for name in ABILITY_NAMES} 
ABILITY_BASE_VALUE = 10 # /---/

SKILLS       = {'Acrobatics':'DEX','Arcana':'INT','Athletics':'STR','Crafting':'INT','Deception':'CHA','Diplomacy':'CHA','Eterology':'WIS','Intimidation':'CHA','Lore':'INT','Medicine':'WIS','Nature':'WIS','Occultism':'INT','Performance':'CHA','Society':'INT','Stealth':'DEX','Survival':'WIS','Thievery':'DEX'}
SKILLS_BASE  = [(skill, ability, 0) for skill, ability in SKILLS.items()]
SKILLS_NAMES = [skill for skill in SKILLS]
SKILLS_BASE_VALUE = 0 # /---/

SAV_THROWS       = {'fortitude':'CON','reflex':'DEX','will':'WIS'}
SAV_THROWS_BASE  = [(key, value,0) for key, value in SAV_THROWS.items()]
SAV_THROWS_NAMES = [st for st in SAV_THROWS]
SAV_THROWS_BASE_VALUE = 0 # /---/

PARAMETER_DEPENDENCE = {ability:[[],[]] for ability in ABILITY_NAMES}
{PARAMETER_DEPENDENCE[value][0].append(key) for key, value in SKILLS.items()}
{PARAMETER_DEPENDENCE[value][1].append(key) for key, value in SAV_THROWS.items()}

ARMOR_CLASS  = ['armor_unarmored', 'armor_light'  , 'armor_medium'  , 'armor_heavy']
WEAPON_CLASS = ['weapon_unarmed' , 'weapon_simple', 'weapon_martial', 'weapon_advanced']

PROF_RANG_BASE = {"class_cd" : 0 , "armor_class" : 0, "perception" : 0} | {wc :0 for wc in  WEAPON_CLASS} | {ac :0 for ac in  ARMOR_CLASS} | {skill:0 for skill in SKILLS_NAMES} | {st:0 for st in SAV_THROWS_NAMES}

