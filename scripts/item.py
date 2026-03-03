
import copy
from scripts.config import ITEMS_FILES
from scripts.exceptions import (
    ItemNotFoundError,
)
from scripts.system import read_json_files

class Item:
    """
    Represents an individual object in the game world.
    """
    def __init__(self, item_id, name, category, id_value = None,
                 rarity=None, traits=None,
                 level=None, price=None, bulk=None,
                 mechanics=None, lore=None):

        self.id = item_id
        self.name = name
        self.category = category
        self.id_value = id_value
        self.rarity = rarity
        self.traits = traits or []
        self.level = level
        self.price = price
        self.bulk = bulk

        self.mechanics = mechanics or {}
        self.lore = lore or {}

        self.status = None

    def __repr__(self):
        return f"<{self.category.upper()}: {self.name}>"


    def get_stat(self, key, default=None):
        """Safely retrieves a stat from the item."""
        return self.stats.get(key, default)


class ItemManager:
    """
    Manages the loading of CSV templates and the creation of new items.
    """
    def __init__(self, base_path="data/info"):
        self.base_path = base_path
        self.library = {}


    def load_all_items(self, structure=ITEMS_FILES):
        for folder, files in structure.items():
            for file in files:
                data = read_json_files(self.base_path, folder, file )

                for n, info in enumerate(data.items()):
                    item_id   = info[0]
                    item_data = info[1]
                    self.library[item_id] = Item(
                        item_id=item_id,
                        name=item_data["name"],
                        category=item_data["category"],
                        id_value        = n,
                        rarity = item_data.get("rarity", "Common"),
                        traits = item_data.get("traits", []),
                        level  = item_data.get("level", 0),
                        price  = item_data.get("price", 150),
                        bulk   = item_data.get("bulk", 1),
                        mechanics=item_data.get("mechanics", {}),
                        lore=item_data.get("lore", {})
                    )


    def spawn(self, item_name):
        """
        Creates and returns a unique, independent copy of an item.
        """
        template = self.library.get(item_name)
        if template:
            # deepcopy ensures the new item doesn't share memory with the template
            return copy.deepcopy(template) if template else None
        raise ItemNotFoundError(item_name)