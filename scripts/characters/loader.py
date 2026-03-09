from scripts.system import read_json_files, get_list_files
import os

class CharacterLoader:
    def __init__(self, base_path):
        self.base_path=base_path
    
    def load_characters(self, structure):
        for folder, value in structure.items():
            characters = {}
            if value == 1:
                list_files = get_list_files(self.base_path , folder)
                for file in list_files:
                    data = read_json_files(self.base_path, folder, file[:-5] )
                    characters[data['id']] = data
            else:
                print(f"{folder} - No")
        return characters
