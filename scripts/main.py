# Items and Characters Identity library
from scripts.item import ItemManager
from scripts.character import CharacterIdentityManager

item_factory = ItemManager()
item_factory.load_all_items()
character_factory = CharacterIdentityManager()
character_factory.load_all_identity()



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