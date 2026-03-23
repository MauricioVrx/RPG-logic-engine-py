from scripts.actions.base.action import Action
from scripts.actions.base.action_result import ActionResult
from scripts.game.game_engine import find_npc_by_name

class AddItemAction(Action):

    name = "add_item"
    def validate(self):
        # Empty data validaton
        entity = self.params.get("entity", None)
        item   = self.params.get("item", None)  
        
        
        if item is None or item not in self.state.item_manager.templates:
            return False, "Invalid item."

        return True, None


    def execute(self):
        print("acá")
        
        entity_name = self.params.get("entity", None)
        item   = self.params.get("item", None)  
        entity = ""

        print(entity_name)

        print(self.state.__dict__)
        if entity_name == 'player':
            entity = self.state.player
        else:
            entity = find_npc_by_name(self.state, entity_name)

        return ActionResult(
            message=f"---{entity}.",
            data={}
        )