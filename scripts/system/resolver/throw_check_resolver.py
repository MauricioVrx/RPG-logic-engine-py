from scripts.mechanics.mechanics             import validate_ability_parameter

def ability_parameter_resolver(entity, parameter_type, parameter_name):
    # Components validation
    if not entity.has_component('ability'):
        return None, f"{entity.name} : don't have {parameter_type}."
    parameters = validate_ability_parameter(entity, parameter_type, parameter_name)
    if parameters[0] is None:
        return parameters
    
    return parameters