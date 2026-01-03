import random
import numbers

from scripts.exceptions import HigherRangeValueError, LowerRangeValueDiceThrowError, NonNumericResultError, MultipleDiceQuantityError

class Dice:
    """
    Base class representing a standard polyhedral dice.
    """
    def __init__(self, sides=6, name="dice", desc = None, is_numeric = True):
        self.sides = sides
        self.name = name
        self.desc = desc
        self.is_numeric = is_numeric

    def __str__(self):
        return f"Type = {self.name}, sides={self.sides}"
    
    def __repr__(self):
        # Returns a compact string representation like 'd20' or custom description
        if self.desc == None:
            return f"{self.name[0]}{self.sides}"
        else:
            return self.desc

    def roll(self):
        """
        Generates a random integer between 1 and the number of sides.
        Raises Range errors if the random generator fails safety checks.
        """
        result = random.randint(1, self.sides)

        # Internal safety checks for the random generator output
        if result > self.sides:
            raise HigherRangeValueError(result, self.sides)
        if result <= 0:
            raise LowerRangeValueDiceThrowError(result, self.sides)
        return result
    
    def multiple_rolls(self, n_rolls = 1) -> tuple:
        """
        Executes multiple rolls and returns a tuple: (total_sum, list_of_results).
        Useful for combined results like '2d6'.
        """
        results = [self.roll() for _ in range(n_rolls)]

        # Validate that the number of generated results matches the request
        if n_rolls != len(results):
            raise MultipleDiceQuantityError(n_rolls, len(results))
        
        if self.is_numeric:
            # Ensure all results are numeric before summing
            if isinstance(results[0], numbers.Number):
                return sum(results), results
            else: 
                raise NonNumericResultError(results)
        return None, results
    
    def advantage_rolls(self, n_rolls = 2):
        """Returns multiple rolls sorted from highest to lowest."""
        return sorted(self.multiple_rolls(n_rolls), reverse=True)
    
    def disadvantage_rolls(self, n_rolls = 2):
        """Returns multiple rolls sorted from lowest to highest."""
        return sorted(self.multiple_rolls(n_rolls), reverse=False)
    
    def get_side(self):
        """Returns the total number of sides/faces of the dice."""
        return self.sides
    

class CustomDice(Dice):
    """
    A dice that maps numeric rolls to a custom list of values (e.g., symbols, colors).
    """
    def __init__(self, values = ['1'], name="dice", desc = None, is_numeric = True):
        sides = len(values)
        super().__init__(sides, name, desc, is_numeric)
        self.values= values 

    def roll(self):
        """
        Rolls the dice and returns the value corresponding to the index rolled.
        """
        # Get numeric result from base roll and map to custom value index
        value = super().roll()
        return self.values[value-1]
    

class RangeDice(Dice):
    """
    A weighted die where each value occupies a specific range of the total faces.
    Example: values=((2, "Fail"), (4, "Success")) means sides 1-2 are 'Fail' and 3-6 are 'Success'.
    """
    def __init__(self, values = ((2,"Rojo"), (3, "Amarillo"), (5, "Verde")), name="dice", desc = None, is_numeric = True):
        # Calculate total sides based on the sum of all weight ranges
        sides = sum([i[0] for i in values])
        super().__init__(sides, name, desc, is_numeric)
        self.values = values

    def roll(self):
        """
        Evaluates the numeric roll against defined weight ranges.
        """
        value = super().roll()
        current_sum = 0
        for weight, label in self.values:
            current_sum += weight
            if value <= current_sum:
                return f"{label}"

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