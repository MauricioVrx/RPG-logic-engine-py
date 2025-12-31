import math

class FormulaProcessor:
    """
    Mathematical expression evaluator for dice rolls.
    Supports basic operators and custom dice inventory.
    """
    def __init__(self, dice_inventory, default_dice=None):
        # Dictionary mapping dice names to Dice objects
        self.dice_inventory = dice_inventory
        self.default_dice = default_dice
        self.operators = [')','^','*','/','+','-','(']
        self.precedence = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3,
            '(': 0 
        }


    def _tokenize(self, formula_text):
        """Splits formula string into a list of tokens (numbers, dice, operators)"""
        f_text = formula_text.replace(" ", "")
        elements = []
        len_value = 1
        while len(f_text) > 0:
            if f_text[0] in self.operators:
                elements.append(f_text[0])
            elif len_value < len(f_text) and f_text[len_value] in self.operators:
                elements.append(f_text[:len_value])
            elif len(f_text) == len_value and  f_text[:len_value] not in self.operators:
                elements.append(f_text[:len_value])
            else:
                len_value += 1
                continue
            f_text = f_text[len_value:]
            len_value = 1
        return elements
    

    def to_rpn(self, formula_text):
        """Converts infix notation to Reverse Polish Notation (RPN) using Shunting-yard"""
        tokens = self._tokenize(formula_text)
        output = []
        stack = []
        
        for token in tokens:
            if token not in self.precedence and token not in [')', '(']:
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else: 
                while stack and self.precedence.get(stack[-1], 0) >= self.precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
        
        while stack:
            output.append(stack.pop())
        return output


    def resolve(self, formula_text):
        """Evaluates RPN expression and returns the final numerical result"""
        rpn_list = self.to_rpn(formula_text)
        stack = []
        crit_fail = []

        for token in rpn_list:
            # 1. if is a Dice
            if token in self.dice_inventory:
                valor = self.dice_inventory[token].roll()
                if self.dice_inventory[token].sides == self.default_dice.sides:
                    crit_fail.append(valor)
                #*** MAKE TEST ***#
                stack.append(float(valor)) 
            
            # 2. if is a number
            elif token.replace('.', '', 1).isdigit(): 
                stack.append(float(token))
            
            # 3. if is a operator
            else:
                b = stack.pop()
                a = stack.pop()

                if   token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(a / b)
                elif token == '^': stack.append(math.pow(a, b))
        
        return stack[0], crit_fail