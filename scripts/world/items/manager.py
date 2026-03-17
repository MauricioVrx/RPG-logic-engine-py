import copy
from scripts.world.items.loader import ItemLoader
from scripts.world.items.item   import Item
from scripts.system.loaders_folder_path import ITEMS_FILES 

from scripts.system.exceptions import (
    ItemNotFoundError
)


class ItemManager:
    """
    Manages the loading, storage and instantiation of item objects.

    This manager is responsible for reading item definitions from JSON files
    using the ItemLoader and converting them into Item objects.

    All loaded items are stored as templates (blueprints). When an item is
    requested through the spawn() method, a deep copy of the template is
    returned to ensure independence between instances.

    Responsibilities:
    - Load item data from JSON files
    - Create Item objects from raw data
    - Store item templates for reuse
    - Spawn independent item instances

    """
    def __init__(self, base_path="data/info"):
        self.loader = ItemLoader(base_path)
        self.templates = {}


    def load_all(self , structure = ITEMS_FILES):
        """
        Loads all item definitions from the specified file structure.

        This method uses the ItemLoader to retrieve raw JSON data and converts
        each entry into an Item object, storing it as a template.

        Parameters
        ----------
        structure : dict
            Defines the folder/file structure used to locate item JSON files.
        """
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

        The method retrieves the corresponding item template and returns a
        deep copy of it. This ensures that the spawned item does not share
        state with the original template.

        Parameters
        ----------
        item_name : str
            Identifier of the item to be created.

        Raises
        ------
        ItemNotFoundError
            If the requested item does not exist in the templates.
        """
        template = self.templates.get(item_name)
        if not template:
            raise ItemNotFoundError(item_name)
            
        return copy.deepcopy(template) if template else None