from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult

from scripts.system.resolver.entity_resolver      import instance_entity_validation
from scripts.system.resolver.throw_check_resolver import ability_parameter_resolver

from scripts.actions.registry    import register_action
from scripts.mechanics.mechanics import skill_cd, saving_throw_cd

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
        
        # Info
        self.context['entity'] = entity

        return True, None


    def execute(self):
        parameter_type  = self.params.get("type", None).lower()
        parameter_name  = self.params.get("parameter_name", None).capitalize()
        cd_value        = self.params.get("cd_value", None)

        # Get entity
        entity = self.context['entity']

        if parameter_type == "skill":
            result = skill_cd(entity, parameter_name, cd_value)
        elif parameter_type == "saving_throw" :
            result = saving_throw_cd(entity, parameter_name, cd_value)

        # Message
        diff_result    = ""
        pass_difficult = ""
        if not cd_value <= 0:
            diff_result    = f"\n\tDiff critical : {result['critical_diff']}"
            pass_difficult = f"\n\tPass : {result['passed']}"
        msg = f"\n\tResult roll : {result['result']}\n\tNatural critical : {result['natural_critical']}{diff_result}{pass_difficult}"

        return ActionResult(
            message=f"""Throw result : {msg}""",
            data={
                "entity" : entity,
                "result" : result,
            }
        )