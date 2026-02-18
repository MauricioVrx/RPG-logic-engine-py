from scripts.constants  import ABILITY_SCORE, PROF_NAMES, PROF_RANG_BASE, SKILLS_BASE, SAV_THROWS_BASE, SKILLS, SAV_THROWS, PARAMETER_DEPENDENCE, SKILLS_NAMES, SAV_THROWS_NAMES
from scripts.config     import MAX_LEVEL, DEFAULTS_ACTIONS, MAX_DYING_COUNT
from scripts.mechanics  import calculate_ability_modifier, calculate_proficiency_bonus
from scripts.exceptions import (
    EntityParameterNotFoundError, 
    EntityAbilityNotFoundError, 
    EntityProficiencyNotFoundError, 
    EntityProficiencyLimitError, 
    EntityLevelLimitError, 
    EntityIsIntegerError, 
    EntityDataFormatError,
    ArmorNonEquippableItemError,
    ArmorNotFoundInInventoryError,
    ArmorInsufficientParameterError,
    WeaponNonEquippableItemError, 
    WeaponNotFoundInInventoryError,
    WeaponNotAvailableHandsError,
    WeaponNotEquipedError,
    EquipmentError
    )
from scripts.mechanics import add_item as add_it, remove_item as rem_it
from collections import Counter

class Entity:
    """
    Base class for all creatures
    """

    def __init__(self):
        self.id_entity   = None 
        self.name        = ""   # Name of entity
        self.alias       = ""   # Alias of entity
        self.age         = None # Count of ages
        self.appearance  = ""   # physical appearance
        self.years_old   = ""   # Years old
        self.gender      = 0    # 0 = None, 1 = Male, 2 = Female, 3 = Other
        self.location    = ""   # id o description

        self.level       = 1 # Current level
        self.exp         = 0 # Total current exp
        self.dying       = 0 # Counts 
        self.speed       = 0 # movement in mts

        self.state     = "Stable" # State if is alive, dead or another 

        self.backstory = "" # Previous and start history
        self.alignment = "" # Alignment preferences
        self.belief    = "" # If beliebe in something or someone
        self.attitude  = "" # Base attitud 

        self.language  = [] # Language comprehension 
        self.sense     = [] # Unusual senses
        
        self.like      = [] # Preferences something or someone
        self.dislike   = [] # Aversion something or someone

        self.ally      = [] # Allied individuals or group
        self.enemy     = [] # Enemy individuals or groups

        self.resistance  = [] # Types of resistance or vulnerability according to level: Vulnerability(>0), Resisitance(<0), Immunity(==0)

        self.actions = DEFAULTS_ACTIONS # Type and count 3 actions, 1 reaction, 1 free action
        self.size    = 3                # Size rank

        self.trait     = ['general'] # All entity tags 
        self.condition = []          # Altered conditions 

        self.proficiency_rank    = PROF_RANG_BASE.copy() # Proficiency rank dict  
        self.core_ability_score  = ABILITY_SCORE    # Ability
        self.extra_ability_score = {name: 0 for name, _ in self.core_ability_score.items()} 
        self.skill               = self.__initial_insert_parameters_points(SKILLS_BASE.copy())     # All Skills with dependences values
        self.saving_throws       = self.__initial_insert_parameters_points(SAV_THROWS_BASE.copy()) # Saving parameters with dependences values

        self.acquired_feats = [] # Feats 
        self.custom_feats   = {} # Feats created just for this entity
        
        self.hit_points_max      = self.core_ability_score["CON"] # Maximum health points of the entity 
        self.hit_points_current  = self.hit_points_max            # Current health points of the entity 
        self.perception          = 0 #  Entity's general awareness and ability to notice their surroundings

        self.armor_class = 0 # Difficult a character is to hit in combat
        self.class_cd    = 0 # Specific abilities(from class or creatures) that force other creatures to attempt a saving throw

        self.inventory = [] 
        self.capacity  = 30                                                       # temporal - Inventory of objects
        self.equipment = {'armor' : None, "accesory" : [], "hands" : [None, None]}  # Humanoid template


    def __str__(self): 
        return f"{self.name} Lv: {self.level} - HP: {self.hit_points_current}/{self.hit_points_max}"


    # ==============================================================
    # INIT FUNCTIONS 
    # ==============================================================

    def __initial_insert_parameters_points(self, parameters):  
        """
        insert the parameter points when it's created
        """
        parameters_dict = {}
        for parameter in parameters:
            parameters_dict[parameter[0]] =  self.update_parameter_point(parameter[1], parameter[0], parameter[2])
        return parameters_dict
    

    # ==============================================================
    # ABILITY / SKILLS / SAVING THROWS / PROFICIENCY - FUNCTIONS
    # ==============================================================
    def __sum_parameters_points(self, parameters):
        """
        Sum all points for a parameter
        """
        if not isinstance(parameters, dict):
            raise EntityDataFormatError(parameters, dict)
        if  parameters['custom'] == 0:
            return parameters['mod'] + parameters['proficiency']
        else:
            return parameters['mod'] + parameters['custom']
    
    def ability_calculation(self, name): 
        """
        Convert ability base points into modifier value
        """
        ability_value = self.get_ability_value(name) 
        return calculate_ability_modifier(ability_value)

    def get_ability_value(self, name):
        """
        Sum entity a base value ability with the extra ability value
        """
        if name not in self.core_ability_score:
            raise EntityAbilityNotFoundError(name)
        return self.core_ability_score[name] + self.extra_ability_score[name]

    def get_ability_score(self):
        """
        Sum entity all bases values abilities with the extras abilities values
        """
        return dict(Counter(self.core_ability_score) + Counter(self.extra_ability_score))

    def get_skill_value(self, name):
        """
        Obtain single skill value
        """
        if name not in self.skill:
            raise EntityParameterNotFoundError(name, "skill")
        return self.__sum_parameters_points(self.skill[name])

    def get_saving_throws_value(self, name): 
        """
        Obtain single saving throw value
        """
        if name not in self.saving_throws:
            raise EntityParameterNotFoundError(name, "saving_throws")
        return self.__sum_parameters_points(self.saving_throws[name])   


    def proficiency_value(self, name):
        """
        Get proficiency bonus value, by proficiency rank and entity level
        """
        if name not in self.proficiency_rank:
            return 0
        rank = self.proficiency_rank[name]
        sum_points = calculate_proficiency_bonus(self.level, rank)
        return sum_points


    def proficiency_promotion(self, proficiency_name, force_promotion = False): 
        """
        Ascend one entity's proficiency rank
        """
        if proficiency_name not in self.proficiency_rank:
            raise EntityProficiencyNotFoundError(proficiency_name)
        if self.proficiency_rank[proficiency_name] < len(PROF_NAMES) or force_promotion == True:
            self.proficiency_rank[proficiency_name] += 1
            if proficiency_name in self.skill:
                self.skill[proficiency_name]['proficiency'] = calculate_proficiency_bonus(self.level, self.proficiency_rank[proficiency_name])        
            if proficiency_name in self.saving_throws:
                self.saving_throws[proficiency_name]['proficiency'] = calculate_proficiency_bonus(self.level, self.proficiency_rank[proficiency_name])        
            return self.proficiency_rank[proficiency_name]
        else:
            raise EntityProficiencyLimitError(self.name, proficiency_name, PROF_NAMES[-1])

    # ==============================================================
    # UPDATES FUNCTIONS
    # ==============================================================
    def update_parameter_point(self, ability, proficiency, custom): 
        """
        Update the parameter points
        """
        parameter = {'mod': self.ability_calculation(ability),'proficiency': self.proficiency_value(proficiency), 'custom' : custom}
        return parameter

    def _update_sub_parameter(self, param_dict, name, custom=None, source_label="parameter"):
        """
        Internal helper to update proficiency and custom bonuses for any parameter dictionary.
        """
        if name not in param_dict:
            raise EntityParameterNotFoundError(name, source_label)
        if name not in self.proficiency_rank:
            raise EntityProficiencyNotFoundError(name)
        
        # Validation
        if custom is not None and not isinstance(custom, int):
            raise EntityIsIntegerError("Custom bonus value must be an integer.")
        
        param_dict[name]['proficiency'] = calculate_proficiency_bonus(self.level, self.proficiency_rank[name])

        # Update values if provided
        if custom is not None:
            param_dict[name]['custom'] = custom

    def update_skill(self, name, custom=None):
        """
        Updates a specific skill's bonuses and recalculates its ability modifier dependency.
        """
        self._update_sub_parameter(self.skill, name, custom, "skill")
        related_ability = SKILLS[name]
        self.skill[name]['mod'] = self.ability_calculation(related_ability)  

    def update_saving_throw(self, name, custom=None):
        """
        Updates a specific saving throw's bonuses and recalculates its modifier.
        """
        self._update_sub_parameter(self.saving_throws, name, custom, "saving_throw")
        related_ability = SAV_THROWS[name]
        self.saving_throws[name]['mod'] = self.ability_calculation(related_ability)

    def update_extra_ability_score(self, name, value):
        """
        Update a new extra ability score and triggers a cascading update for all dependent parameters.
        """
        if name not in self.extra_ability_score:
            raise EntityAbilityNotFoundError(name)
        if not isinstance(value, int):
            raise EntityIsIntegerError(f"Ability score for {name} must be an integer.")
        
        self.extra_ability_score[name] = value

        # Cascading update using the dependency map
        # idx 0: Skills, idx 1: Saving Throws
        dependencies = PARAMETER_DEPENDENCE.get(name, [[], []])

        self.update_parameters_by_ability(skills = dependencies[0], saving_throws = dependencies[1])
            
        return self.extra_ability_score[name]

    def update_parameters_by_ability(self, skills = SKILLS_NAMES, saving_throws = SAV_THROWS_NAMES): 
        """
        Update skills/saving_throw mods values by its ability 
        """
        for skill_name in skills:
            self.update_skill(skill_name)
            
        for save_name in saving_throws:
            self.update_saving_throw(save_name)

        return True

    # ==============================================================
    # HIT POINTS / LEVEL / ARMOR CLASS / PERCEPTION - FUNCTIONS
    # ==============================================================
    def level_up(self, force_lvl = False): 
        """
        Arise the entity's level by one
        """
        if self.level < MAX_LEVEL or force_lvl == True: # /---/  + hit points
            self.level += 1
            self.exp    = 0
        else:
            raise EntityLevelLimitError(self.name, self.level, MAX_LEVEL)
        return self.level

    def sum_exp(self, value):
        """
        Sum entity expecience
        """
        if not isinstance(value, int):
            raise EntityIsIntegerError("The experience points must be a integer.")
        self.exp = 0 if self.exp + value < 0 else self.exp + value
        return (self.exp)

    def sum_hit_points(self, value): 
        """
        Recovers or damages the entity
        """
        if not isinstance(value, int):
            raise EntityIsIntegerError("Damage/Healt points must be a integer.")

        previous_hp = self.hit_points_current

        # Apply change
        self.hit_points_current += value

        # Apply limits
        if self.hit_points_current > self.hit_points_max:
            self.hit_points_current = self.hit_points_max

        # State logic
        if previous_hp > 0 and self.hit_points_current <= 0:
            self.dying += 1
            if self.dying > MAX_DYING_COUNT:
                self.state = "Death"
            else:
                self.state = "Dying"
        elif previous_hp <= 0 and self.hit_points_current > 0:
            self.state = "Stable"
        elif self.state == "Dying" and value < 0:
            self.dying += 1
        if self.hit_points_current < self.get_ability_value("CON") * -1:
            self.state = "Death"

        return previous_hp, self.hit_points_current, self.state


    def calculate_armor_class(self): 
        """
        Get armor class result
        """
        ac = self.ability_calculation('DEX')
        
        if self.equipment['armor'] in [None, "armor_unarmored"]:
            if type(self.equipment['armor']) != type(None):
                if ac > self.equipment['armor']['DEX_cap']:
                    ac = self.equipment['armor']['DEX_cap']
                
                # Bonus CA 
                ac += self.equipment['armor']['AC_bonus']
                
                # Armor actegory proficiency
                ac += self.proficiency_value(self.equipment['armor']['armor_category'])
            else:
                ac += self.proficiency_value('armor_unarmored')

        ac += 10  
        self.armor_class = ac
        return ac

    def calculate_perception(self): 
        perception = self.ability_calculation('WIS')
        if 'perception' in self.proficiency_rank :
            perception += self.proficiency_value('perception')
        return perception
    

    # ==============================================================
    # ITEMS / EQUIPMENT / INVENTORY - FUNCTIONS
    # ==============================================================
    def pick_up_item(self, item_instance):
        """
        Add an object to inventory.
        """
        if item_instance:
            self.inventory.append(item_instance)
            return True
        return False


    def add_item(self, item_instance):
        """
        Add an object to inventory.
        """
        return add_it(self, item_instance)
    

    def remove_item(self, item_instance):
        """
        Remove an object from inventory.
        """
        return rem_it(self, item_instance)


    def get_inventory_desc(self):
        """
        Return a inventory object list from entity  
        """
        return ", ".join([item.name for item in self.inventory]) or "Empty"
    

    def equip_armor(self, armor_instance): 
        """
        Equip an armor to entity.
        """
        # Check instance params 
        if hasattr(armor_instance, 'stats') and 'armor_category' not in armor_instance.stats:
            raise ArmorNonEquippableItemError(armor_instance)

        # Check if armor not in inventory
        if armor_instance not in self.inventory:
            raise ArmorNotFoundInInventoryError(self.name, armor_instance)
        
        # Check if the minimum STR required to use the equipment is available.
        if not self.ability_calculation('STR') >= armor_instance.stats.get('str_req', 0):
            raise ArmorInsufficientParameterError(self.name, self.ability_calculation('STR'), armor_instance.name, 'STR', armor_instance.stats['str_req'])

        # Check if a the armor is already equiped, this will be unequip
        if self.equipment['armor'] != None:
            self.unequip_armor()
      
        # Equip armor
        self.equipment['armor'] = armor_instance
        armor_instance.status = "equiped" # Change armor status 

        return True
    

    def unequip_armor(self):
        """
        Equip the equiped armor to entity.
        """ 
        if self.equipment['armor'] != None:
            self.equipment['armor'].status = None
            self.equipment['armor'] = None
            return True
        return False


    def equip_weapon_on_hand(self, weapon_instance):
        """
        Equip an weapon to entity. The entity must have hands available to equip the weapon.
        """
        # Check instance params 
        if hasattr(weapon_instance, 'stats') and 'weapon_category' not in weapon_instance.stats:
            raise WeaponNonEquippableItemError(weapon_instance)

        # Check if weapon not in inventory
        if weapon_instance not in self.inventory:
            raise WeaponNotFoundInInventoryError(self.name, weapon_instance)
        
        # Check if a the weapon is already equiped
        if weapon_instance.status == "equiped":
            raise EquipmentError()

        available_hands = self.equipment['hands'].count("weapon_unarmed") + self.equipment['hands'].count(None)

        # Check the number of hands available against the number of hands required.
        if not available_hands >= int(weapon_instance.stats['hands']):
            raise WeaponNotAvailableHandsError(self.name, weapon_instance)

        # Python list of available hands
        equipable_slots = [weapon_instance] + ["holding_weapon" for _ in range(int(weapon_instance.stats['hands'])-1)]

        # Equip weapon using the necessary count of hands
        for idx, hand in enumerate(self.equipment['hands']):
            if hand == "weapon_unarmed" or hand == None:
                self.equipment['hands'][idx] = equipable_slots.pop(0)
            if len(equipable_slots) == 0:
                break
        
        weapon_instance.status = "equiped"

        return True
    

    def unequip_weapon_on_hand(self, weapon_instance):
        # check inventory item, 
        if weapon_instance not in self.inventory:
            raise WeaponNotFoundInInventoryError(self.name, weapon_instance)
        
        # Check if a the weapon is already equiped
        if weapon_instance not in self.equipment['hands']:
            raise WeaponNotEquipedError(self.name, weapon_instance)

        # count of hands
        equipable_slots = ["weapon_unarmed" for _ in range(int(weapon_instance.stats['hands']))]

        # remove weapon and "holding_weapon" to "weapon_unarmed"
        for idx, hand in enumerate(self.equipment['hands']):
            if hand == weapon_instance or hand == "holding_weapon":
                self.equipment['hands'][idx] = equipable_slots.pop(0)
            if len(equipable_slots) == 0:
                break

        # change status weapon
        weapon_instance.status = None

        return True

