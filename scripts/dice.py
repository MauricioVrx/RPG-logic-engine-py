import random

class Dice:
    def __init__(self, sides=6, name="dice", desc = None):
        self.sides = sides
        self.name = name
        self.desc = desc

    def __str__(self):
        return f"Type = {self.name}, sides={self.sides}"

    
    def __repr__(self):
        if self.desc == None:
            return f"{self.name[0]}{self.sides}"
        else:
            return self.desc

    def roll(self):
        return random.randint(1, self.sides)
    
    def multiple_rolls(self, n_rolls = 1) -> list:
        return [self.roll() for x in range(1, n_rolls+1)]
    
    def advantage_rolls(self, n_rolls = 2):
        return sorted(self.multiple_rolls(n_rolls), reverse=True)
    
    def disadvantage_rolls(self, n_rolls = 2):
        return sorted(self.multiple_rolls(n_rolls), reverse=False)
    
    def get_side(self):
        return self.sides
    

class CustomDice(Dice):
    def __init__(self, values = ['1'], name="dice", desc = None):
        sides = len(values)
        super().__init__(sides, name, desc)
        self.values= values 

    def roll(self):
        value = super().roll()
        return f"{self.values[value-1]}"
    

class RangeDice(Dice):
    def __init__(self, values = ((2,"Rojo"), (3, "Amarillo"), (5, "Verde")), name="dice", desc = None):
        sides = sum([i[0] for i in values])
        super().__init__(sides, name, desc)
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
# print(d6.multiple_rolls(7))

# print()
# custom1 = CustomDice(values = ["♠","♣","♥","♦"])
# print(custom1.roll())
# print(custom1.multiple_rolls(5))

# print()
# dict_rouleta = ((3,"Éxito"), (7, "Fallo"), (1, "Premio"))
# range_dice   =  RangeDice(values = dict_rouleta)
# print(range_dice.roll())


# throw = {}
# throw['coin'] = CustomDice(name = "coin", values = ["Cara","Sello"]) 
# throw['d3']   = Dice(3)
# throw['d4']   = Dice(4)
# throw['d6']   = Dice(6)
# throw['d10']  = Dice(10)
# throw['d12']  = Dice(12)
# throw['d20']  = Dice(20)
# throw['d100'] = Dice(100)
# throw['card_logo_dice'] = CustomDice(values = ["♠","♣","♥","♦"], desc="♠♣♥♦")


# print(throw)
# print(throw['coin'].roll())