from scripts.game_config.constants import ABILITY_NAMES

# General basis of the project
class GameBaseError(Exception): pass

# =============================================================================
# DICE ERRORS
# =============================================================================

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
            "error"         : self.__class__.__name__,
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
            "error"       : self.__class__.__name__,
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
            "error"       : self.__class__.__name__,
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
            "error"       : self.__class__.__name__,
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
            "error"       : self.__class__.__name__,
            "rolled_dice" : self.rolled_dice,
            "code"        : self.error_code
        }
    


# =============================================================================
# SPECIFIC ERRORS IN MATHEMATICAL LOGIC ERRORS
# =============================================================================

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
            "error"   : self.__class__.__name__,
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
            "error"   : self.__class__.__name__,
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
            "error"           : self.__class__.__name__,
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
            "error"       : self.__class__.__name__,
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
            "error"          : self.__class__.__name__,
            "iterator_limit" : self.iterator_limit,
            "formula_size"   : self.formula_size,
            "code"           : self.error_code
        }
    

# =============================================================================
# ENTITY ERRORS
# =============================================================================
class EntityEngineError(GameBaseError):
    """Base class for exceptions in this module."""
    pass

class EntityParameterNotFoundError(EntityEngineError):
    """Exception raised when a parameter not found """
    def __init__(self, parameter, feature):
        self.parameter  = parameter
        self.feature    = feature
        self.error_code = "ERR_ENTITY_PARAMETER_NOT_FOUND"
        self.message    = f"Parameter {parameter} NOT found in {feature}'." 
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"     : self.__class__.__name__,
            "parameter" : self.parameter,
            "feature"   : self.feature,
            "code"      : self.error_code
        }

class EntityAbilityNotFoundError(EntityEngineError):
    def __init__(self, ability):
        self.ability  = ability
        self.error_code = "ERR_ENTITY_ABILITY_NOT_FOUND"
        self.message    = f"Ability '{ability}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "ability"        : self.ability,
            "all_abilities"  : ABILITY_NAMES,
            "code"           : self.error_code
        }

class EntityProficiencyNotFoundError(EntityEngineError):
    """Exception raised when a proficiency not found """
    def __init__(self, proficiency):
        self.proficiency = proficiency
        self.error_code  = "ERR_ENTITY_PROFICIENCY_NOT_FOUND"
        self.message     = f"Proficiency '{proficiency}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"       : self.__class__.__name__,
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
            "error"     : self.__class__.__name__,
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
            "error"         : self.__class__.__name__,
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
            "error"         : self.__class__.__name__,
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
            "error"           : self.__class__.__name__,
            "valid_data_type" : self.valid_data_type,
            "used_data"       : self.used_data,
            "code"            : self.error_code
        }

# =============================================================================
# CHARACTER EXCEPTIONS
# =============================================================================
class CharacterEngineError(GameBaseError):
    """Base class for exceptions in this module."""
    pass

class CharacterNotFoundError(CharacterEngineError):
    """Raised when the specified Item does not found"""
    def __init__(self, character_name):
        self.character_name  = character_name
        self.error_code = "ERR_CHARACTER_NOT_FOUND"
        self.message    = f"Character : '{character_name}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "character_name" : self.character_name ,
            "code"           : self.error_code
        }


class CharacterDisabledParameterError(CharacterEngineError):
    """Raised when attempting to use a disabled Ancestry, Class, or Background."""
    def __init__(self, name, param_type):
        self.name         = name 
        self.param_type   = param_type 
        self.error_code   = "ERR_DISABLED_PARAMETER"
        self.message      = f"{param_type} '{name}' is currently disabled."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "type"           : self.param_type ,
            "code"           : self.error_code
        }


class CharacterAbilityLimitExceededError(CharacterEngineError):
    """Raised when the number of selected abilities exceeds the allowed limit."""
    def __init__(self, count_abilities, max_limit):
        self.count_abilities = count_abilities
        self.max_limit       = max_limit
        self.error_code = "ERR_ABILITY_LIMIT_EXCEEDED"
        self.message    = f"Ability limit exceeded. Max: {max_limit}, Provided: {count_abilities}."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"           : self.__class__.__name__,
            "count_abilities" : self.count_abilities ,
            "max_limit"       : self.max_limit ,
            "code"            : self.error_code
        }


class CharacterDuplicateAbilityError(CharacterEngineError):
    """Exception generated when asign a free ability, but its already activate by the parameter"""
    def __init__(self, name, type, fixed_boost):
        self.name        = name
        self.type        = type
        self.fixed_boost = fixed_boost
        self.error_code = "ERR_CHARACTER_ABILITY_DUPLICATED"
        self.message    = f"Ability '{name}' is already a fixed boost({fixed_boost}) for this {type}."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name,
            "type"           : self.type,
            "fixed_boost"    : self.fixed_boost,
            "code"           : self.error_code
        }
    

class CharacterInvalidDistributionError(CharacterEngineError):
    """Raised when the provided ability distribution contains non-unique parameters."""
    def __init__(self, abilities):
        self.abilities  = abilities
        self.error_code = "ERR_CHARACTER_INVALID_DISTRIBUTION"
        self.message    = f"Ability distribution must be unique. Received: {abilities}."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "abilities"      : self.abilities ,
            "code"           : self.error_code
        }


class CharacterChangePastError(CharacterEngineError):
    """Raised when the try to change the character's ancestry, class or background."""
    def __init__(self,char_name, past_type):
        self.char_name  = char_name
        self.past_type  = past_type
        self.error_code = "ERR_CHARACTER_CHANGE_PAST"
        self.message    = f"You cannot change the {past_type} from {char_name}."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "char_name"      : self.char_name,
            "past_type"      : self.past_type,
            "code"           : self.error_code
        }


class CharacterIdentityNotFoundError(CharacterEngineError):
    """Raised when the try to change the character's ancestry, class or background."""
    def __init__(self, char_identity, name):
        self.char_identity  = char_identity
        self.name  = name
        self.error_code = "ERR_CHARACTER_IDENTITY_NOT_FOUND"
        self.message    = f" {char_identity} : {name} not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "char_identity"  : self.char_identity,
            "name"           : self.name,
            "code"           : self.error_code
        }

# =============================================================================
# ANCESTRY EXCEPTIONS
# =============================================================================
class AncestryNotFoundError(CharacterEngineError):
    """Raised when the specified Ancestry does not exist in the database."""
    def __init__(self, name):
        self.name       = name
        self.error_code = "ERR_ANCESTRY_NOT_FOUND"
        self.message    = f"Ancestry '{name}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "code"           : self.error_code
        }
    
# =============================================================================
# CLASS EXCEPTIONS
# =============================================================================
class ClassNotFoundError(CharacterEngineError):
    """Raised when the specified Class does not found"""
    def __init__(self, name):
        self.name       = name
        self.error_code = "ERR_CLASS_NOT_FOUND"
        self.message    = f"Class '{name}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error" : self.__class__.__name__,
            "name"  : self.name ,
            "code"  : self.error_code
        }
    
class ClassMainAbilityRequiredError(CharacterEngineError):
    """Raised when the selection does not satisfy the class's mandatory ability option."""
    def __init__(self, name, ability_options):
        self.name            = name
        self.ability_options = ability_options
        self.error_code      = "ERR_CLASS_MAIN_ABILITY_REQUIRED"
        self.message         = f"ERROR: Class '{name}' required 1 point boosts on '{ability_options}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"           : self.__class__.__name__,
            "class"           : self.name ,
            "ability_options" : self.ability_options ,
            "code"            : self.error_code
        }

# =============================================================================
# BACKGROUND EXCEPTIONS
# =============================================================================
class BackgroundNotFoundError(CharacterEngineError):
    """Raised when the specified Background does not found"""
    def __init__(self, name):
        self.name       = name
        self.error_code = "ERR_BACKGROUND_NOT_FOUND"
        self.message    = f"Background '{name}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "code"           : self.error_code
        }

class BackgroundMinAbilityRequiredError(CharacterEngineError):
    """Raised when the selection does not satisfy the background's mandatory ability options."""
    def __init__(self, background, ability_options):
        self.background      = background
        self.ability_options = ability_options
        self.error_code      = "ERR_MIN_ABILITY_REQUIRED"
        self.message         = f"ERROR: Background '{background}' required 1 point boosts on '{ability_options}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"           : self.__class__.__name__,
            "background"      : self.background ,
            "ability_options" : self.ability_options ,
            "code"            : self.error_code
        }
    

# =============================================================================
# DATAFRAMES EXCEPTIONS
# =============================================================================
class DataFrameError(GameBaseError): 
    """Base class for DataFrame errors."""
    pass


class DataFrameMultipleRowsError(DataFrameError):
    """Raised when the DataFrame does multiple rows."""
    def __init__(self, name, column, df_name):
        self.name    = name
        self.column  = column
        self.df_name = df_name
        self.error_code = "ERR_DATAFRAME_FOUND_MULTIPLE_ROWS"
        self.message    = f"DATAFRAME ERROR: '{name}' name have more than one rows on '{df_name}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "column"         : self.column ,
            "dataframe_name" : self.df_name ,
            "code"           : self.error_code
        }

class DataFrameRowNotFoundError(DataFrameError):
    """Raised when the DataFrame does multiple rows."""
    def __init__(self, name, column, df_name):
        self.name    = name
        self.column  = column
        self.df_name = df_name
        self.error_code = "ERR_DATAFRAME_VALUE_NOT_FOUND"
        self.message    = f"Background '{name}' not found on '{df_name}."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "column"         : self.column ,
            "dataframe_name" : self.df_name ,
            "code"           : self.error_code
        }


# =============================================================================
# ITEMS EXCEPTIONS
# =============================================================================
class ItemError(GameBaseError): 
    """Base class for errors occurring during Items usage, equip and tranfer."""
    pass

class ItemNotFoundError(ItemError):
    """Raised when the specified Item does not found"""
    def __init__(self, item_name):
        self.item_name  = item_name
        self.error_code = "ERR_ITEM_NOT_FOUND"
        self.message    = f"Item : '{item_name}' not found."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "item_name"      : self.item_name ,
            "code"           : self.error_code
        }


class ItemNotRemovedError(ItemError):
    """Raised when try to remove an equiped Item"""
    def __init__(self, item_name):
        self.item_name  = item_name
        self.error_code = "ERR_ITEM_NOT_REMOVED"
        self.message    = f"Item : '{item_name}' could not be deleted."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "item_name"      : self.item_name ,
            "code"           : self.error_code
        }
    

# =============================================================================
# EQUIPMENT EXCEPTIONS
# =============================================================================

class EquipmentError(GameBaseError): 
    """Base class for exceptions in this module."""
    pass

class ArmorNonEquippableItemError(EquipmentError):
    """Raised when try to equip an incorrect items"""
    def __init__(self, name):
        self.name    = name
        self.error_code = "ERR_ARMOR_NON_EQUIPPABLE_ITEM"
        self.message    = f"'{name}' is not an equipable armor."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "code"           : self.error_code
        }

class ArmorNotFoundInInventoryError(EquipmentError):
    """Raised when try to equip an items who is not in it's own inventory"""
    def __init__(self, entity_name, armor_name):
        self.armor_name    = armor_name
        self.entity_name    = entity_name
        self.error_code = "ERR_ARMOR_NOT_FOUND_IN_INVENTORY"
        self.message    = f"'{armor_name}' is not an in {entity_name} inventory."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "armor_name"     : self.armor_name ,
            "entity_name"    : self.entity_name ,
            "code"           : self.error_code
        }

class ArmorInsufficientParameterError(EquipmentError): 
    """Raised when an entity attempts to equip armor whose parameters are insufficient"""
    def __init__(self, entity_name, entity_value, armor_name ,parameter_name , parameter_required_value):
        self.entity_name    = entity_name
        self.entity_value   = entity_value
        self.armor_name     = armor_name
        self.parameter_name = parameter_name
        self.parameter_required_value = parameter_required_value
        self.error_code = "ERR_ARMOR_INSUFFICIENT_PARAMETER"
        self.message    = f"'{entity_name}'({parameter_name} : {entity_value}) attempted to equip '{armor_name} but requires {parameter_required_value} {parameter_name}."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"              : self.__class__.__name__,
            "entity_name"        : self.entity_name ,
            "entity_value"       : self.entity_value ,
            "armor_name"         : self.armor_name ,
            "parameter_name"     : self.parameter_name ,
            "parameter_required_value" : self.parameter_required_value ,
            "code"               : self.error_code
        }
    

class WeaponNonEquippableItemError(EquipmentError):
    """Raised when try to equip an incorrect items"""
    def __init__(self, name):
        self.name    = name
        self.error_code = "ERR_WEAPON_NON_EQUIPPABLE_ITEM"
        self.message    = f"'{name}' is not an equipable WEAPON."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "code"           : self.error_code
        } 
    
class WeaponNotFoundInInventoryError(EquipmentError):
    """Raised when try to equip an items who is not in it's own inventory"""
    def __init__(self, entity_name, weapon_name):
        self.weapon_name    = weapon_name
        self.entity_name    = entity_name
        self.error_code = "ERR_WEAPON_NOT_FOUND_IN_INVENTORY"
        self.message    = f"'{weapon_name}' is not an in {entity_name} inventory."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "weapon_name"    : self.weapon_name ,
            "entity_name"    : self.entity_name ,
            "code"           : self.error_code
        }
    
class WeaponNotAvailableHandsError(EquipmentError):
    """Raised when try to equip an items with busy hands"""
    def __init__(self, entity_name, weapon_name):
        self.weapon_name    = weapon_name
        self.entity_name    = entity_name
        self.error_code = "ERR_WEAPON_NOT_FOUND_IN_INVENTORY"
        self.message    = f"'{entity_name}' can't hold '{weapon_name}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "weapon_name"    : self.weapon_name ,
            "entity_name"    : self.entity_name ,
            "code"           : self.error_code
        }
    

class WeaponNotEquipedError(EquipmentError):
    """Raised when try to equip an items with busy hands"""
    def __init__(self, entity_name, weapon_name):
        self.weapon_name    = weapon_name
        self.entity_name    = entity_name
        self.error_code = "ERR_WEAPON_NOT_EQUIPED"
        self.message    = f"'{weapon_name}' is not equipped by '{entity_name}'."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "weapon_name"    : self.weapon_name ,
            "entity_name"    : self.entity_name ,
            "code"           : self.error_code
        }


# =============================================================================
# STORAGE EXCEPTIONS
# =============================================================================

class StorageError(GameBaseError): 
    """Base class for exceptions in this module."""
    pass


class StorageLimitItemsError(StorageError):
    """Raised when the items storage exceed limit"""
    def __init__(self, name, space_occuped, limit):
        self.name          = name
        self.limit         = limit
        self.space_occuped = space_occuped
        self.error_code = "ERR_STORAGE_LIMIT_ITEM"
        self.message    = f"The storage '{name}' exceed items quantity({space_occuped}/{limit})."
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error"          : self.__class__.__name__,
            "name"           : self.name ,
            "limit"          : self.limit ,
            "space_occuped"  : self.space_occuped ,
            "code"           : self.error_code
        }

# =============================================================================
# SYSTEM EXCEPTIONS
# =============================================================================

class SystemError(GameBaseError): 
    """Base class for exceptions in this module."""
    pass


class FileNotFoundError(SystemError):
    """Exception raised when a "dice" is not in the inventory."""
    def __init__(self, file_name, folder, file_format):
        self.file_name   = file_name
        self.folder      = folder
        self.file_format = file_format
        self.error_code  = "ERR_FILE_NOT_FOUND"
        super().__init__(f"'{file_name}.{file_format}' not found in '{folder}' folder")
    
    def to_dict(self):
            return {
                "error"       : self.__class__.__name__,
                "file_name"   : self.file_name ,
                "folder"      : self.folder ,
                "file_format" : self.file_format,
                "code"           : self.error_code
        }

# =============================================================================
# CALENDAR EXCEPTION
# =============================================================================

class CalendarError(GameBaseError): 
    """Base class for exceptions in this module."""
    pass

class TimeFormatError(SystemError):
    """Exception raised when time values exceend range limits"""
    def __init__(self, names):
        self.names       = names
        self.error_code  = "ERR_TIME_FORMAT"
        super().__init__(f"'Time error: {names}.")
    
    def to_dict(self):
            return {
                "error"   : self.__class__.__name__,
                "names"   : self.names ,
                "code"    : self.error_code
        }


class TimeNamePhaseNotFoundError(SystemError):
    """Exception raised when try to find a wrong day phase."""
    def __init__(self, name):
        self.name   = name
        self.error_code  = "ERR_TIME_PHASE_NOT_FOUND"
        super().__init__(f"Day phase'{name}' not found.")
    
    def to_dict(self):
            return {
                "error"       : self.__class__.__name__,
                "name"        : self.name ,
                "code"        : self.error_code
        }
