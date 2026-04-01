from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult

from scripts.system.resolver.entity_resolver      import instance_entity_validation
from scripts.system.resolver.throw_check_resolver import ability_parameter_resolver

from scripts.actions.registry import register_action

@register_action("skill", "saving_throw")
class ParameterCheckAction(Action):
        
    def validate(self):
        # Empty data validaton
        parameter_type  = self.params.get("type", None).lower()
        entity_name     = self.params.get("entity", None)
        parameter_name  = self.params.get("parameter_name", None).capitalize()

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if entity is None:
            return None, msg
        
        result_parameter, msg = ability_parameter_resolver(entity, parameter_type, parameter_name)
        if result_parameter is None:
            return None, f"{entity.name} {msg}"

        print(result_parameter) # <--- 
        
        return True, None


    def execute(self):
        return ActionResult(
            message=f"",
            data={
            }
        )