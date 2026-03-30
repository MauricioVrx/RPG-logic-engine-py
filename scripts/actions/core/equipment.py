from scripts.actions.base.action             import Action
from scripts.actions.base.action_result      import ActionResult
from scripts.system.resolver.entity_resolver import instance_entity_validation
from scripts.system.resolver.item_resolver   import resolve_item, instance_item_validation

class EquipWeaponAction(Action):
    name = "equip_weapon"

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if entity is None:
            return None, msg
        
        # Item validation
        weapon, msg =instance_item_validation(entity, self.params, entity.get_component('inventory').items)
        if weapon is None:
            return None, msg
        
        # Validate weapon
        validate_weapon = entity.get_component('equipment').validate_weapon_equipment(weapon)
        if not validate_weapon:
            return None, f"Error action 'EquipWeaponAction'."
        
        if hasattr(weapon, 'status') and weapon.status == 'equiped' :
            return None, f"Item '{weapon}' is already equiped."
    
        req_hands, available_hands = entity.get_component('equipment').hands_available_validation(weapon)
        if not available_hands >= req_hands: 
            return None, f"{entity_name} can't equip '{weapon}', needs {req_hands} available hands."

        # INFO
        self.context['entity'] = entity
        self.context['weapon'] = weapon

        return True, None

    def execute(self):
        entity_name = self.params.get("entity", None)
        weapon_name = self.params.get("item", None)

        # Get entity
        entity = self.context['entity']

        # Get weapon
        weapon = self.context['weapon']  

        "Equip weapon"
        weapon_equiped = entity.get_component("equipment").equip_weapon_on_hand(weapon)

        # RETURN
        return ActionResult(
            message=f"{entity_name}: {weapon_equiped[1]}.",
            data={
                "entity" : entity,
                "weapon" : weapon_equiped[0]
            }
        )


class UnequipWeaponAction(Action):
    name = "unequip_weapon"

    def validate(self):
        # Empty data validaton
        entity_name = self.params.get("entity", None)
        weapon_name = self.params.get("item", None)

        # Entity validation
        entity, msg = instance_entity_validation(self.state, self.params["entity"], entity_name)
        if entity is None:
            return None, msg
        
        # Weapon validation
        weapon, msg = instance_item_validation(entity, self.params, entity.get_component('equipment').equipment['hands'], equiped = True, multiple= True )
        if weapon is None:
            return None, msg
        
        # Hands validation
        hands, msg = entity.get_component('equipment').validate_unequip_weapon(weapon)
        if hands is None:
            return None, f"{entity_name} : {msg}"
        
        
        # INFO
        self.context['entity'] = entity
        self.context['weapon'] = weapon

        return True, None


    def execute(self):
        entity_name = self.params.get("entity", None)

        # Get entity
        entity = self.context['entity']

        # Get weapon
        weapon = self.context['weapon'] 

        # Items validation
        unequiped_weapon = entity.get_component('equipment').unequip_weapon_on_hand(weapon)
        if unequiped_weapon is None:
            return None, f"{entity_name} : {unequiped_weapon[1]}"

        # RETURN
        return ActionResult(
            message=f"{entity_name}: {unequiped_weapon[1]}.",
            data={
                "entity" : entity,
                "weapon" : unequiped_weapon[0]
            }
        )