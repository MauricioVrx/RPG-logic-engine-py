from scripts.actions.base.action           import Action
from scripts.actions.base.action_result    import ActionResult
from scripts.system.resolver.entity_resolver import instance_entity_validation
from scripts.system.resolver.item_resolver   import instance_item_validation


class EquipWeaponAction(Action):
    name = "equip_weapon"

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)
        weapon_name = self.params.get("weapon", None)

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if not entity:
            return False, msg
        
        # Item validation
        weapon, msg = instance_item_validation(entity, self.params, entity.get_component('inventory').items)
        if weapon == None:
            return None, msg
        
        ##########################################

        # Validate weapon
        validate_weapon = entity.get_component('equipment').validate_weapon_equipment(weapon)
        if not validate_weapon:
            return False, f"Error action 'EquipWeaponAction'."
        
        if hasattr(weapon, 'status') and weapon.status == 'equiped' :
            return None, f"Item '{weapon}' is already equiped."

        
        req_hands, available_hands = entity.get_component('equipment').hands_available_validation()
        if not available_hands >= req_hands: 
            return None, f"{entity_name} can't equip '{weapon}', needs {req_hands} available hands."
        
        # INFO
        self.context['entity'] = entity
        self.context['weapon'] = weapon

    def execute(self):
        # RETURN
        return ActionResult(
            message=f"",
            data={
            }
        )

# Equip/unequip weapon
# Equip/unequip armor