import random
import numbers

from scripts.exceptions import HigherRangeValueError, LowerRangeValueDiceThrowError, NonNumericResultError, MultipleDiceQuantityError

class Dice:
    def __init__(self, sides=6, name="dice", desc = None, is_numeric = True):
        self.sides = sides
        self.name = name
        self.desc = desc
        self.is_numeric = is_numeric

    def __str__(self):
        return f"Type = {self.name}, sides={self.sides}"
    
    def __repr__(self):
        if self.desc == None:
            return f"{self.name[0]}{self.sides}"
        else:
            return self.desc

    def roll(self):
        result = random.randint(1, self.sides)
        if result > self.sides:
            raise HigherRangeValueError(result, self.sides)
        if result <= 0:
            raise LowerRangeValueDiceThrowError(result, self.sides)
        return result
    
    def multiple_rolls(self, n_rolls = 1) -> list:
        multiple_rolls = [self.roll() for _ in range(1, n_rolls+1)]
        if n_rolls !=  len(multiple_rolls):
            raise MultipleDiceQuantityError(n_rolls, len(multiple_rolls))
        if self.is_numeric == True:
            if isinstance(multiple_rolls[0], numbers.Number):
                return sum(multiple_rolls), multiple_rolls
            else: 
                raise NonNumericResultError(multiple_rolls)
        return None, multiple_rolls
    
    def advantage_rolls(self, n_rolls = 2):
        return sorted(self.multiple_rolls(n_rolls), reverse=True)
    
    def disadvantage_rolls(self, n_rolls = 2):
        return sorted(self.multiple_rolls(n_rolls), reverse=False)
    
    def get_side(self):
        return self.sides
    

class CustomDice(Dice):
    def __init__(self, values = ['1'], name="dice", desc = None, is_numeric = True):
        sides = len(values)
        super().__init__(sides, name, desc, is_numeric)
        self.values= values 

    def roll(self):
        value = super().roll()
        return self.values[value-1]
    

class RangeDice(Dice):
    def __init__(self, values = ((2,"Rojo"), (3, "Amarillo"), (5, "Verde")), name="dice", desc = None, is_numeric = True):
        sides = sum([i[0] for i in values])
        super().__init__(sides, name, desc, is_numeric)
        self.values = values

    def roll(self):
        value = super().roll()
        current_sum = 0
        for limit in self.values:
            current_sum += limit[0]
            if value <= current_sum:
                return f"{limit[1]}"

## Probar código
# print()
# d6 = Dice()
# print(d6.roll())
# print(d6.multiple_rolls(2))
# print(d6.multiple_rolls(10))

# print()
# custom1 = CustomDice(values = ["♠","♣","♥","♦"], is_numeric=False)
# print(custom1.roll())
# print(custom1.multiple_rolls(10))

# custom2 = CustomDice(values = [1,1.5,2,2.5,3,3.5])
# print(custom2.multiple_rolls(10))

# print()
# dict_rouleta = ((3,"Éxito"), (7, "Fallo"), (1, "Premio"))
# range_dice   =  RangeDice(values = dict_rouleta)
# print(range_dice.roll())


# throw = {}
# throw['coin'] = CustomDice(name = "coin", values = ["Cara","Sello"], is_numeric= False) 
# throw['d3']   = Dice(3)
# throw['d4']   = Dice(4)
# throw['d6']   = Dice(6)
# throw['d10']  = Dice(10)
# throw['d12']  = Dice(12)
# throw['d20']  = Dice(20)
# throw['d100'] = Dice(100)
# throw['card_logo_dice'] = CustomDice(values = ["♠","♣","♥","♦"], desc="♠♣♥♦", is_numeric= False)


# print(throw)
# print(throw['coin'].roll())