class Item:
    """
    Represents a single item instance within the game world.

    This class defines the core properties of an item, including its
    identity, category, gameplay mechanics, and lore information.

    Items can represent:
    - Weapons
    - Armor
    - Consumables
    - Quest items
    - Miscellaneous objects
    """

    def __init__(self, item_id, name, category, id_value = None,
                 rarity=None, traits=None,
                 level=None, price=None, bulk=None,
                 mechanics=None, lore=None):
        """
        Attributes
        ----------
        id : str
            Unique identifier of the item.

        name : str
            Display name of the item.

        category : str
            Category/type of the item (e.g., weapon, armor, consumable).

        id_value : int, optional
            Internal numeric identifier.

        rarity : str, optional
            Rarity level (common, rare, epic, etc.).

        traits : list, optional
            List of traits or tags associated with the item.

        level : int, optional
            Recommended or required level.

        price : int, optional
            Value of the item in game currency.

        bulk : float, optional
            Weight or encumbrance value.

        mechanics : dict
            Gameplay-related data (damage, effects, bonuses, etc.).

        lore : dict
            Narrative or descriptive information.

        status : any
            Runtime state of the item (e.g., equipped, broken, etc.).
    
        """

        self.id       = item_id
        self.key_name = item_id
        self.name     = name
        self.category = category
        self.id_value = id_value
        self.rarity = rarity
        self.traits = traits or []
        self.level  = level
        self.price  = price
        self.bulk   = bulk

        self.mechanics = mechanics or {}
        self.lore = lore or {}

        self.status = None

    def __repr__(self):
        return f"<{self.category.upper()}: {self.name}>"


    def get_stat(self, key, default=None):
        """Safely retrieves a stat from the item."""
        return self.stats.get(key, default)

