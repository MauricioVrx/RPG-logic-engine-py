from scripts.system import read_json_files

class ItemLoader:
    def __init__(self, base_path):
        self.base_path=base_path
    
    def load_items(self, structure):
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