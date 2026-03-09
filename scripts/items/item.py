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

