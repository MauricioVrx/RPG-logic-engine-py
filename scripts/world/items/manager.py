import copy
from scripts.world.items.loader import ItemLoader
from scripts.world.items.item   import Item
from scripts.system.loaders_folder_path import ITEMS_FILES 

from scripts.system.exceptions import (
    ItemNotFoundError
)


class ItemManager:
    def __init__(self, base_path="data/info"):
        self.loader = ItemLoader(base_path)
        self.templates = {}


    def load_all(self , structure = ITEMS_FILES):
        data = self.loader.load_items(structure)
        for item_id, info in data.items():
            self.templates[item_id] = Item(
                item_id   = info["item_id"],
                name      = info["name"],
                category  = info["category"],
                id_value  = info.get("id_value"),

                rarity    = info.get("rarity", "Common"),
                traits    = info.get("traits", []),

                level     = info.get("level", 0),
                price     = info.get("price", 150),
                bulk      = info.get("bulk", 1),

                mechanics = info.get("mechanics", {}),
                lore      = info.get("lore", {})
            )


    def spawn(self, item_name):
        """
        Creates and returns a unique, independent copy of an item.
        """
        template = self.templates.get(item_name)
        if not template:
            raise ItemNotFoundError(item_name)
            
        return copy.deepcopy(template) if template else None