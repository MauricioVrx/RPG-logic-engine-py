from scripts.constants import ABILITY_NAMES

# General basis of the project
class GameBaseError(Exception): pass

# DICE ERRORS
class DiceEngineError(GameBaseError):
    """Base class for exceptions in this module."""
    pass

class DiceNotFoundError(DiceEngineError):
    """Exception raised when a "dice" is not in the inventory."""
    def __init__(self, dice_name, inventory_list=None):
        self.dice_name         = dice_name
        self.available_options = inventory_list
        self.error_code        = "ERR_DICE_404"
        super().__init__(f"'Dice' not found: {dice_name}")
    
    def to_dict(self):
        return {
            "error"         : "DiceNotFoundError",
            "missing_token" : self.dice_name,
            "suggestions"   : self.available_options,
            "code"          : self.error_code
        }
    

class HigherRangeValueError(DiceEngineError):
    """Exception raised when a throw result is higher than "dice's" sides."""
    def __init__(self, result, dice_sides):
        self.result     = result
        self.dice_sides = dice_sides
        self.error_code = "ERR_DICE_HIGHER_RANGE_VALUE"
        self.message    = f"The result {result} is higher than the {dice_sides} sides'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : "HigherRangeValueError",
            "throw_value" : self.result,
            "dice_sides"  : self.dice_sides,
            "code"        : self.error_code
        }


class LowerRangeValueDiceThrowError(DiceEngineError):
    """Exception raised when a throw result less or equal to 0"""
    def __init__(self, result, dice_sides):
        self.result     = result
        self.dice_sides = dice_sides
        self.error_code = "ERR_DICE_LOWER_RANGE_VALUE"
        self.message    = f"The result {result} is less than the {dice_sides} sides'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : "LowerRangeValueDiceThrowError",
            "throw_value" : self.result,
            "dice_sides"  : self.dice_sides,
            "code"        : self.error_code
        }


class MultipleDiceQuantityError(DiceEngineError):
    """Exception generated when the count of multiple "dice" does not match the quantity request"""
    def __init__(self, n_rolls, rolled_dice):
        self.n_rolls     = n_rolls
        self.rolled_dice = rolled_dice
        self.error_code  = "ERR_DICE_MULTIPLE_DICE_QUIATITY"
        self.message     = f"The quantity of rolls({n_rolls}) required and rolled({rolled_dice}) are not same'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : "MultipleDiceQuantityError",
            "n_rolls"     : self.n_rolls,
            "rolled_dice" : self.rolled_dice,
            "code"        : self.error_code
        }


class NonNumericResultError(DiceEngineError):
    """Exception raised when a calculation is attempted on non-numeric "dice" results"""
    def __init__(self, rolled_dice):
        self.rolled_dice = rolled_dice
        self.error_code  = "ERR_DICE_NON_NUMERIC_RESULT"
        self.message     = f'the roled "dice" are not numeric: {rolled_dice}.'
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : "NonNumericResultError",
            "rolled_dice" : self.rolled_dice,
            "code"        : self.error_code
        }
    

# Specific errors in mathematical logic
class ParserError(GameBaseError): 
    """Base class for errors occurring during formula parsing and evaluation."""
    pass


class ParserInvalidFormulaError(ParserError): 
    """Raised when the formula string contains invalid syntax."""
    def __init__(self, formula):
        self.error_code = 'ERR_PARSER_INVALID_FORMULA'
        self.formula    = formula
        self.message    = f'Invalid syntax in formula: {formula}'
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"   : "ParserInvalidFormulaError",
            "formula" : self.formula,
            "code"    : self.error_code
        }


class ParserIncompleteResultError(ParserError): 
    """Raised when an expression cannot be fully resolved (e.g., missing operators)."""
    def __init__(self, formula):
        self.error_code = 'ERR_PARSER_INCOMPLETE_RESULT'
        self.formula    = formula
        self.message    = f"'The mathematical process could not be completed for formula: '{formula}'"
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"   : "ParserIncompleteResultError",
            "formula" : self.formula,
            "code"    : self.error_code
        }


class ParserZeroDivisionError(ParserError):
    """Raised when a division by zero occurs during evaluation."""
    def __init__(self, formula_segment):
        self.error_code      = 'ERR_PARSER_ZERO_DIVISION'
        self.formula_segment = formula_segment
        self.message         = f"Division by zero detected in segment: '{formula_segment}'"
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"           : "ParserZeroDivisirorError",
            "formula_segment" : self.formula_segment,
            "code"            : self.error_code
        }
    

class ParserConvertRPNError(ParserError):
    """Raised when the Shunting-yard algorithm encounters a logical inconsistency."""
    def __init__(self, token_error, formula):
        self.error_code  = 'ERR_PARSER_CONVERT_RPN'
        self.token_error = token_error
        self.formula     = formula
        self.message     = f"Failed to convert token '{token_error}' to RPN in formula: '{formula}'"
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : "ParserConvertRPNError",
            "token_error" : self.token_error,
            "formula"     : self.formula,
            "code"        : self.error_code
        }


class ParserTokenizeExceedIterator(ParserError):
    """Raised when the formula length or token count exceeds the safety iteration limit."""
    def __init__(self,iterator_limit, formula_size):
        self.error_code     = 'ERR_PARSER_TOKENRIZE_EXCEED_ITERATOR' 
        self.iterator_limit = iterator_limit
        self.formula_size   = formula_size
        self.message        = f"Formula length ({formula_size}) exceeds the safety limit of {iterator_limit} iterations."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : "ParserTokenizeExceedIterator",
            "iterator_limit" :  self.iterator_limit,
            "formula_size"   :  self.formula_size,
            "code"           : self.error_code
        }
    

# ENTITY ERRORS
class EntityEngineError(GameBaseError):
    """Base class for exceptions in this module."""
    pass


class EntityParameterNotFoundError(EntityEngineError):
    """Exception raised when a parameter not found """
    def __init__(self, parameter, feature):
        self.parameter  = parameter
        self.feature    = feature
        self.error_code = "ERR_ENTITY_PARAMETER_NOT_FOUND"
        self.message    = f"The parameter {parameter} NOT found in {feature}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"     : "EntityParameterNotFoundError",
            "parameter" : self.parameter,
            "feature"   : self.feature,
            "code"      : self.error_code
        }


class EntityAbilityNotFoundError(EntityEngineError):
    def __init__(self, ability):
        self.ability  = ability
        self.error_code = "ERR_ENTITY_ABILITY_NOT_FOUND"
        self.message    = f"The ABILITY '{ability}' NOT found'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : "EntityAbilityNotFoundError",
            "ability"        : self.ability,
            "all_abilities"  : ABILITY_NAMES,
            "code"           : self.error_code
        }
    

class EntityProficiencyNotFoundError(EntityEngineError):
    """Exception raised when a proficiency not found """
    def __init__(self, proficiency):
        self.proficiency = proficiency
        self.error_code  = "ERR_ENTITY_PROFICIENCY_NOT_FOUND"
        self.message     = f"The proficiency {proficiency} NOT found'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : "EntityProficiencyNotFoundError",
            "proficiency" : self.proficiency,
            "code"        : self.error_code
        }

    
class EntityProficiencyLimitError(EntityEngineError):
    """Exception raised try to promotion an proficiency over the limit"""
    def __init__(self, entity_name ,parameter, max_rank):
        self.entity_name = entity_name
        self.parameter   = parameter
        self.max_rank    = max_rank
        self.error_code  = "ERR_ENTITY_PROFICIENCY_LIMIT_RANK"
        self.message     = f"{entity_name}: '{parameter}' can NOT by higher than {max_rank}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"     : "EntityProficiencyLimitError",
            "parameter" : self.parameter,
            "max_rank"  : self.max_rank,
            "code"      : self.error_code
        }


class EntityLevelLimitError(EntityEngineError):
    """Exception raised try to level up over the limit"""
    def __init__(self, entity_name ,current_level, max_level):
        self.entity_name   = entity_name
        self.current_level = current_level
        self.max_level     = max_level
        self.error_code = "ERR_ENTITY_LEVEL_LIMIT"
        self.message    = f"{entity_name}: level {current_level} can NOT by higher than level {max_level}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"         : "EntityLevelLimitError",
            "entity_name"   : self.entity_name,
            "current_level" : self.current_level,
            "max_level"     : self.max_level,
            "code"          : self.error_code
        }


class EntityIsIntegerError(EntityEngineError):
    """Exception raised if the value is not a integer value"""
    def __init__(self, msg):
        self.msg        = msg
        self.error_code = "ERR_ENTITY_INTEGER_VALUE"
        self.message    = f"Number error: {msg}"
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"         : "EntityIsIntegerError",
            "msg"           : self.msg,
            "code"          : self.error_code
        }


class EntityDataFormatError(EntityEngineError):
    """Exception generated when an invalid data type is used."""
    def __init__(self, used_data, valid_data_type):
        self.valid_data_type = valid_data_type
        self.used_data       = type(used_data)
        self.error_code      = "ERR_ENTITY_FORMAT"
        self.message         = f"Invalid data type: {used_data}.Data must be {valid_data_type}"
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"           : "EntityDataFormatError",
            "valid_data_type" : self.valid_data_type,
            "used_data"       : self.used_data,
            "code"            : self.error_code
        }