import pandas as pd
import os
import copy
from scripts.config import ITEMS_CSV_FILES
from scripts.exceptions import (
    ItemNotFoundError,
    ItemFileNotFoundError
)

class Item:
    """
    Represents an individual object in the game world.
    """
    def __init__(self, name, category, **kwargs):
        self.name = name
        self.category = category
        # Stores all CSV columns (Price, Weight, Damage, etc.) filtering out NaN values
        self.stats = {k: v for k, v in kwargs.items() if pd.notna(v)}
        
    def __repr__(self):
        return f"<{self.category.upper()}: {self.name}>"

    def get_stat(self, key, default=None):
        """Safely retrieves a stat from the item."""
        return self.stats.get(key, default)


class ItemManager:
    """
    Manages the loading of CSV templates and the creation of new items.
    """
    def __init__(self, base_path="data/info_csv"):
        self.base_path = base_path
        self.library = {}

    def load_all_items(self):
        """
        Iterates through specific folders to load all game items.
        """
        structure = ITEMS_CSV_FILES

        for folder, files in structure.items():
                for file in files:
                    path = os.path.join(self.base_path, folder, f"{file}.csv")
                    if os.path.exists(path):
                        self._load_csv(path, category=file)
                    else:
                        raise ItemFileNotFoundError(folder, file)


    def _load_csv(self, path, category):
        """
        Reads a CSV and stores each row as a template Item.
        """
        df = pd.read_csv(path, sep=';')
        for _, row in df.iterrows():
            data = row.to_dict()
            name = data.pop("name", data.pop("name ", None)) 
            if name:
                # Create the 'Master' library template
                self.library[name] = Item(name, category, **data)


    def spawn(self, item_name):
        """
        Creates and returns a unique, independent copy of an item.
        """
        template = self.library.get(item_name)
        if template:
            # deepcopy ensures the new item doesn't share memory with the template
            return copy.deepcopy(template) if template else None
        raise ItemNotFoundError(item_name)