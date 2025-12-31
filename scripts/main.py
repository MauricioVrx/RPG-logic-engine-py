# main.py
from dice import Dice, CustomDice
from parser import FormulaProcessor

# 1. Dices 
MAIN_DICE = Dice(20, name ="main")
throw = {
    'd20': MAIN_DICE,
    'd12': Dice(12),
    'd6': Dice(6),
    'coin': CustomDice(values=["0", "1"], name="coin") 
}

formula_procesos = FormulaProcessor(throw, MAIN_DICE)

formula = "(d20 - d12) + 4"
try:
    resultado = formula_procesos.resolve(formula)
    print(f"Formula: {formula}")
    print(f"Result: {resultado[0]}")
    print(f"Critis/fails: {resultado[1]}")
except Exception as e:
    print(f"Error executing formula: {e}")