from scripts.constants  import ABILITY_SCORE, PROF_NAMES, PROF_RANG_BASE, SKILLS_BASE, SAV_THROWS_BASE, SKILLS, SAV_THROWS, PARAMETER_DEPENDENCE, SKILLS_NAMES, SAV_THROWS_NAMES
from collections import Counter

from scripts.mechanics  import calculate_ability_modifier, calculate_proficiency_bonus
from scripts.exceptions import (
    EntityParameterNotFoundError, 
    EntityAbilityNotFoundError, 
    EntityProficiencyNotFoundError, 
    EntityProficiencyLimitError,  
    EntityIsIntegerError, 
    EntityDataFormatError,
    )

class AbilityComponent:
    component_name = "ability"
    def __init__(self, entity):
        self.entity = entity
        self.proficiency_rank    = PROF_RANG_BASE.copy() # Proficiency rank dict  
        self.core_ability_score  = ABILITY_SCORE.copy()  # Ability
        self.extra_ability_score = {name: 0 for name, _ in self.core_ability_score.items()} 
        self.skill               = self.__initial_insert_parameters_points(SKILLS_BASE.copy())     # All Skills with dependences values
        self.saving_throws       = self.__initial_insert_parameters_points(SAV_THROWS_BASE.copy()) # Saving parameters with dependences values
        self.acquired_feats      = [] # Feats 
        self.custom_feats        = {} # Feats created just for this entity

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if key == "custom_skill":
                for skill_name, skill_value in value.items():
                    self.update_skill(skill_name, custom=skill_value)
                continue
            if key == "custom_saving_throws":
                for st_name, st_value in value.items():
                    self.update_saving_throw(st_name, custom=st_value)
                continue
            if key == "proficiency_rank":
                self.proficiency_rank.update(value)
            if hasattr(self, key):
                if key == "extra_ability_score":
                    for ability_name, ability_value in value.items():
                        self.extra_ability_score[ability_name] += ability_value
                    continue
                setattr(self, key, value)
            

    def __initial_insert_parameters_points(self, parameters):  
        """
        insert the parameter points when it's created
        """
        parameters_dict = {}
        for parameter in parameters:
            parameters_dict[parameter[0]] =  self.update_parameter_point(parameter[1], parameter[0], parameter[2])
        return parameters_dict
    

    def __sum_parameters_points(self, parameters):
        """
        Sum all points for a parameter
        """
        if not isinstance(parameters, dict):
            raise EntityDataFormatError(parameters, dict)
        if  parameters['custom'] == 0:
            return parameters['mod'] + parameters['proficiency']
        else:
            return parameters['custom']
    
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

    def _get_level(self):
        return self.entity.get_component("progression").level

    def proficiency_value(self, name):
        """
        Get proficiency bonus value, by proficiency rank and entity level
        """
        if name not in self.proficiency_rank:
            return 0
        rank = self.proficiency_rank[name]
        sum_points = calculate_proficiency_bonus(self._get_level(), rank)
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
                self.skill[proficiency_name]['proficiency'] = calculate_proficiency_bonus(self.entity.get_component("progression").level, self.proficiency_rank[proficiency_name])        
            if proficiency_name in self.saving_throws:
                self.saving_throws[proficiency_name]['proficiency'] = calculate_proficiency_bonus(self.entity.get_component("progression").level, self.proficiency_rank[proficiency_name])        
            return self.proficiency_rank[proficiency_name]
        else:
            raise EntityProficiencyLimitError(self.entity.get_component("identity").name, proficiency_name, PROF_NAMES[-1])

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
        
        param_dict[name]['proficiency'] = calculate_proficiency_bonus(self.entity.get_component("progression").level, self.proficiency_rank[name])
       
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
   