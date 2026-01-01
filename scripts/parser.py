import math

from scripts.dice import Dice
from scripts.exceptions import DiceNotFoundError, ParserInvalidFormulaError, ParserIncompleteResultError, ParserZeroDivisionError, ParserConvertRPNError, ParserTokenizeExceedIterator

class FormulaProcessor:
    """
    Mathematical expression evaluator for dice rolls.
    Implements the Shunting-yard algorithm to handle operator precedence 
    and custom dice inventory resolution.
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
        self.iterator_limit = 100 # Safety limit to prevent infinite loops and overflow

    def _sanitize(self, formula_text):
        # Limpiar espacios
        clean_text = formula_text.lower().replace(" ", "").strip()

        if not clean_text:
            raise ParserInvalidFormulaError("The formula cannot be empty.")
        # limitar caracteres validos 
        allow_chart = set("abcdefghijklmnopqrstuvwxyz0123456789.+-*/^()")
        for char in clean_text:
            if char not in allow_chart:
                raise ParserInvalidFormulaError(f"Illegal character found:{char}")
        
        # Validar igualdad de caracteres '(' y ')'
        if clean_text.count('(') != clean_text.count(')'):
            raise ParserInvalidFormulaError(f"Unbalanced parentheses in formular")
        
        return clean_text


    def _tokenize(self, formula_text):
        """
        Deconstructs the formula string into individual tokens (operands and operators).
        """
        f_text = formula_text
        # Validate formula length against safety limit
        if len(f_text) > self.iterator_limit:
            raise ParserTokenizeExceedIterator(self.iterator_limit, len(f_text))
        elements = []
        len_value = 1

        while len(f_text) > 0:
            if len_value > self.iterator_limit:
                raise ParserTokenizeExceedIterator(self.iterator_limit, len_value)
            
            # If the current character is a standalone operator 
            if f_text[0] in self.operators:
                elements.append(f_text[0])
            # If the next character is an operator, slice the current multi-char token (number or dice)
            elif len_value < len(f_text) and f_text[len_value] in self.operators:
                elements.append(f_text[:len_value])
            # Handle the last token in the string
            elif len(f_text) == len_value and  f_text[:len_value] not in self.operators:
                elements.append(f_text[:len_value])
            # Increment slice length to capture multi-character tokens
            else:
                len_value += 1
                continue
            f_text = f_text[len_value:]
            len_value = 1
        return elements
    

    def to_rpn(self, formula_text):
        """
        Converts infix notation to Reverse Polish Notation (RPN) using the Shunting-yard algorithm.
        """
        sanitized_formula = self._sanitize(formula_text)

        tokens = self._tokenize(sanitized_formula)
        output = []
        stack = []
        
        for token in tokens:
            try:
                # If token is an operand (number or dice), move directly to output
                if token not in self.precedence and token not in [')', '(']:
                    output.append(token)
                elif token == '(':
                    stack.append(token)
                # On closing parenthesis, pop from stack to output until an opening parenthesis is found
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    stack.pop() # Discard the opening parenthesis
                else: 
                    # Handle operator precedence: pop higher or equal priority operators to output
                    while stack and self.precedence.get(stack[-1], 0) >= self.precedence[token]:
                        output.append(stack.pop())
                    stack.append(token)
            except IndexError:
                raise ParserConvertRPNError(token, sanitized_formula)
        # Append remaining operators from stack to output
        while stack:
            output.append(stack.pop())
        return output


    def resolve(self, formula_text):
        """
        Evaluates an RPN expression and returns a tuple containing:
        (numerical_result, list_of_critical_or_botch_rolls)
        """
        rpn_list = self.to_rpn(formula_text)
        stack = []
        critical_or_botch = []
        
        for token in rpn_list:
            # Case 1: Token is a Dice key
            if 'd' in token:
                parts =  token.split(sep='d', maxsplit=1)
                raw_qty = parts[0]
                dice_name = f"d{parts[1]}"

                # if roll 1 Dice
                if raw_qty == "":
                    quantity = 1
                # if roll more tha one dice; the values must be whole numbers.
                elif raw_qty.isdigit(): 
                    quantity = int(raw_qty)
                else:
                    raise ParserInvalidFormulaError(f"Invalid dice quantity: '{raw_qty}'")

                if dice_name not in self.dice_inventory:
                    raise DiceNotFoundError(dice_name, self.dice_inventory)
                
                # Obtain results (total value and list of individual shots)
                total_val, individual_rolls = self.dice_inventory[dice_name].multiple_rolls(quantity)

                # Track rolls if they match the default dice type (for crit/botch detection)
                if self.dice_inventory[dice_name].sides == self.default_dice.sides:
                    critical_or_botch.extend(individual_rolls)

                stack.append(float(total_val)) 
            
            # Case 2: Token is a numeric constant
            elif token.replace('.', '', 1).isdigit(): 
                stack.append(float(token))
            
            # Case 3: Token is an operator
            elif token in self.operators:
                try:
                    b = stack.pop()
                    a = stack.pop()

                    if   token == '+': stack.append(a + b)
                    elif token == '-': stack.append(a - b)
                    elif token == '*': stack.append(a * b)
                    elif token == '/': stack.append(a / b)
                    elif token == '^': stack.append(math.pow(a, b))
                except ZeroDivisionError:
                    raise ParserZeroDivisionError(f"{a}/{b}") 
                except: 
                    raise ParserInvalidFormulaError(formula_text)
            else:
                # Token is neither an operator, number, nor recognized dice
                raise DiceNotFoundError(token, self.dice_inventory)

        # If more than one value remains, the formula was incomplete (e.g., missing operators)
        if len(stack) > 1:
            raise ParserIncompleteResultError(formula_text)

        return stack[0], critical_or_botch