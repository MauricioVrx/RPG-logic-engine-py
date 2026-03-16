# Items and Characters Identity library
from scripts.world.items.manager import ItemManager
from scripts.world.characters.manager import CharacterManager, CharacterIdentityManager
# from scripts.characters.character import CharacterIdentityManager

#
item_factory = ItemManager()
item_factory.load_all()
identity_character_factory = CharacterIdentityManager()
identity_character_factory.load_all_identity()

character_loaded = CharacterManager(identity_character_factory, item_factory)
character_loaded.load_all("unique")
character_loaded.load_all("template")

print()
print(character_loaded.characters)
print()
print(character_loaded.characters_template)
# print()
# print(identity_character_factory.ancestry)
# print()
# print(identity_character_factory.char_class)
# print()
# print(identity_character_factory.background)
# print()
# print(item_factory.templates)
# print()

print("******"*4)
char1 =  character_loaded.spawn("template", "city_civile")
# print(char1.__dict__)
# print("******"*4)

dorian = character_loaded.spawn("unique", "dorian_ashford")
print(dorian.get_component('inventory').__dict__)


# print(character_loaded.characters)

# from scripts.dice import Dice, CustomDice
# from scripts.parser import FormulaProcessor

# # 1. Dices 
# MAIN_DICE = Dice(20, name ="main")
# throw = {
#     'd100' : Dice(100),
#     'd20'  : MAIN_DICE,
#     'd12'  : Dice(12),
#     'd6'   : Dice(6),
#     'coin' : CustomDice(values=["0", "1"], name="coin"),
#     'card_logo_dice' : CustomDice(values = ["♠","♣","♥","♦"], desc="♠♣♥♦", is_numeric= False) 
# }

# formula_procesos = FormulaProcessor(throw, MAIN_DICE)

# # formula = "(d20 - d12) + 4"
# formula = ""

# try:
#     resultado = formula_procesos.resolve(formula)
#     print(f"Formula: {formula}")
#     print(f"Result: {resultado[0]}")
#     print(f"Critis/fails: {resultado[1]}")
# except Exception as e:
#     print(f"Error executing formula: {e}")