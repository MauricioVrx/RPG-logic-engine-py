from scripts.system.exceptions import (
    ArmorNonEquippableItemError,
    ArmorNotFoundInInventoryError,
    ArmorInsufficientParameterError,
    WeaponNonEquippableItemError,
    WeaponNotFoundInInventoryError,
    WeaponNotAvailableHandsError,
    WeaponNotEquipedError,
    EquipmentError
    )

class EquipmentComponent:
    """
    Handles equipmet for an entity.

    This component allows equip and unequip armors, weapons from inventory.

    Responsibilities
    ----------------
    - equip and unequip armors
    - equip and unequip weapons

    Dependencies
    ------------
    - Inventory component
    - Identity component
    - Ability component
    - Combat component

    Attributes
    ----------
    entity : Entity
        Reference to the entity that owns this inventory.

    equipment : dict
        dict of character equipment (armor, accesory, hands, back).

    Methods
    -------
    equip_armor(armor_instance)
        Equip an armor to entity from inventory.

    unequip_armor()
        Unequip the equiped armor to entity.

    equip_weapon_on_hand(weapon_instance)
        Equip an weapon to entity. The entity must have hands available to equip the weapon.

    unequip_weapon_on_hand
        Unequip the equiped weapons to entity.

    load_from_dict(data)
        Loads items from JSON data using the item factory.
    """
    component_name = "equipment"
    def __init__(self, entity):

        self.entity = entity
        self.equipment = {'armor' : None, "accesory" : [], "hands" : [None, None], 'back' : None}  # Humanoid template
        # /---/ make accesory back equipment

    def load_from_dict(self, data: dict, factory):
        for key, value in data.items():
            if key == "equipment":
                for category, equipments in value.items():
                    equipment = []
                    [equipment.append(self.entity.get_component("inventory").add_item(factory.spawn(equip), force_add = True)[0]) for equip in equipments]
                    if category == "armor":
                        [self.equip_armor(equip) for equip in equipment]
                    elif category == "hands":
                        [self.equip_weapon_on_hand(equip) for equip in equipment]
                continue
            if hasattr(self, key):
                setattr(self, key, value)


    def equip_armor(self, armor_instance):
        """
        Equip an armor to entity.
        """

        # Check instance params
        if hasattr(armor_instance, 'mechanics') and 'armor_category' not in armor_instance.mechanics:
            raise ArmorNonEquippableItemError(armor_instance)

        # Check if armor not in inventory
        if armor_instance not in self.entity.get_component("inventory").items:
            raise ArmorNotFoundInInventoryError(self.entity.get_component("identity").name, armor_instance)

        # Check if the minimum STR required to use the equipment is available.
        if not self.entity.get_component("ability").ability_calculation('STR') >= armor_instance.mechanics.get('strength_requirement', 0) and not armor_instance.mechanics.get('armor_category') == "unarmored":
            raise ArmorInsufficientParameterError(self.entity.get_component("identity").name, self.entity.get_component("ability").ability_calculation('STR'), armor_instance.name, 'STR', armor_instance.mechanics['strength_requirement'])

        # Check if a the armor is already equiped, this will be unequip
        if self.equipment['armor'] != None:
            self.unequip_armor()

        # Equip armor
        self.equipment['armor'] = armor_instance
        armor_instance.status = "equiped" # Change armor status
        self.entity.get_component("combat").calculate_armor_class()


        return True


    def unequip_armor(self):
        """
        Unequip the equiped armor to entity.
        """
        if self.equipment['armor'] != None:
            self.equipment['armor'].status = None
            self.equipment['armor'] = None
            return True
        return False


    def validate_weapon_equipment(self, weapon_instance):
        # Check instance params
        if weapon_instance.category not in ['shield', 'weapon']:
            raise WeaponNonEquippableItemError(weapon_instance)

        # Check if weapon not in inventory
        if weapon_instance not in self.entity.get_component("inventory").items:
            raise WeaponNotFoundInInventoryError(self.entity.get_component("identity").name, weapon_instance)

        # Check if a the weapon is already equiped
        if weapon_instance.status == "equiped":
            raise EquipmentError()

        return True, ""

    def hands_available_validation(self, weapon_instance):
        req_hands = 0
        if hasattr(weapon_instance, 'mechanics') and 'hands' in weapon_instance.mechanics :
            # Weapon
            req_hands = int(weapon_instance.mechanics['hands'])
        else:
            # Shield
            req_hands = 1

        available_hands = self.equipment['hands'].count("weapon_unarmed") + self.entity.get_component("equipment").equipment['hands'].count(None)

        # Check the number of hands available against the number of hands required.
        if not available_hands >= req_hands:
            # return None, f"Not available hands for '{weapon_instance}'" /---/
            raise WeaponNotAvailableHandsError(self.entity.get_component("identity").name, weapon_instance)

        return req_hands, available_hands


    def equip_weapon_on_hand(self, weapon_instance):
        """
        Equip an weapon to entity. The entity must have hands available to equip the weapon.
        """
        # validation = self.validate_weapon_equipment(weapon_instance)
        # if validation[0] == None:
        #     return validation

        req_hands, _ = self.hands_available_validation(weapon_instance)

        # Python list of available hands
        equipable_slots = [weapon_instance] + ["holding_weapon" for _ in range(req_hands-1)]

        # Equip weapon using the necessary count of hands
        for idx, hand in enumerate(self.entity.get_component("equipment").equipment['hands']):
            if hand == "weapon_unarmed" or hand == None:
                self.equipment['hands'][idx] = equipable_slots.pop(0)
            if len(equipable_slots) == 0:
                break

        weapon_instance.status = "equiped"

        return weapon_instance, f"'{weapon_instance.name}' equiped"


    def unequip_weapon_on_hand(self, weapon_instance):
        """
        Unequip the equiped weapons to entity.
        """
        # check inventory item,
        if weapon_instance not in self.entity.get_component("inventory").items:
            raise WeaponNotFoundInInventoryError(self.entity.get_component("identity").name, weapon_instance)

        # Check if a the weapon is already equiped
        if weapon_instance not in self.entity.get_component("equipment").equipment['hands']:
            raise WeaponNotEquipedError(self.entity.get_component("identity").name, weapon_instance)

        # count of hands
        equipable_slots = ["weapon_unarmed" for _ in range(int(weapon_instance.mechanics['hands']))]

        # remove weapon and "holding_weapon" to "weapon_unarmed"
        for idx, hand in enumerate(self.equipment['hands']):
            if hand == weapon_instance or hand == "holding_weapon":
                self.entity.get_component("equipment").equipment['hands'][idx] = equipable_slots.pop(0)
            if len(equipable_slots) == 0:
                break

        # change status weapon
        weapon_instance.status = None

        return True
