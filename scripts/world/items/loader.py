from scripts.system.core.files_manager import read_json_files

class ItemLoader:
    """
    Responsible for loading item templates from JSON files.

    This class reads item definitions from a structured set of folders
    and files, then consolidates them into a single dictionary of
    item templates.

    Each item entry is enriched with:
    - item_id: unique identifier of the item
    - id_value: incremental numeric index (useful for internal systems)

    The loader does NOT create Item objects. It only returns raw data
    that can later be used by factories or managers.

    Parameters
    ----------
    base_path : str
        Base directory where item JSON files are stored.
    """
    def __init__(self, base_path):
        self.base_path=base_path
    
    def load_items(self, structure):
        """
        Loads item templates from multiple JSON files organized by folders.

        The structure parameter defines which folders and files should be read.
        Each JSON file may contain multiple item definitions.

        Parameters
        ----------
        structure : dict
            Dictionary where:
            - key = folder name
            - value = list of file names (without extension)

            Example:
            {
                "equipment": ["armor", "weapon", "shield"],
                "item": ["adventuring_gear", "consumables"]
            }

        Notes
        -----
        - Each item is assigned an incremental id_value.
        - Later items may overwrite previous ones if IDs collide.
        """
        templates = {}
        for folder, files in structure.items():
            for file in files:
                data = read_json_files(self.base_path, folder, file )
                for n, (item_id, item_data) in enumerate(data.items()):
                    templates[item_id] = {
                        "item_id": item_id,
                        "id_value": n,
                        **item_data
                    }
        return templates