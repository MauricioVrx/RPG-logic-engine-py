from scripts.actions.core.wait import (
    WaitAction, 
    SleepAction, 
    WaitToMorningAction,
    )

from scripts.actions.core.inventory import (
    AddItemAction,
    ListItemAction,
    RemoveItemAction,
    TransferItemAction,
    )

from scripts.actions.core.equipment import (
    EquipWeaponAction,
)

ACTIONS = {
    # TIME
    "wait"            : WaitAction,
    "sleep"           : SleepAction,
    "wait_to_morning" : WaitToMorningAction,

    # ITEMS
    "add_item"        : AddItemAction,
    "list_items"      : ListItemAction,
    "remove_item"     : RemoveItemAction,
    "transfer_item"   : TransferItemAction,

    # Equipment
    "equip_weapon"    :EquipWeaponAction,
}

def execute_action(action_name, state, **kwargs):

    action_class = ACTIONS.get(action_name)
    
    if not action_class:
        return {
            "message": f"Unknown action: {action_name}",
            "data": {},
            "events": []
        }

    action = action_class(state, **kwargs)
    result = action.run()

    return result.to_dict()