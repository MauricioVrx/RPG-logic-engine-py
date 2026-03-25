from scripts.system.core.files_manager import read_json_files, get_list_files

class CharacterLoader:
    """
    Handles the loading of character JSON files from the filesystem.

    This class is responsible only for retrieving raw data from files.
    It does not create Character objects.
    """
    def __init__(self, base_path):
        self.base_path=base_path
    
    def load_characters(self, structure):
        characters = {}
        for folder, value in structure.items():
            if value == 1:
                list_files = get_list_files(self.base_path , folder)
                for file in list_files:
                    data = read_json_files(self.base_path, folder, file[:-5] )
                    characters[data['id']] = data
        return characters  
    

class CharacterIdentityLoader:
    """
    Loads JSON files containing character identity definitions such as
    ancestries, classes and backgrounds.
    """
    def __init__(self, base_path):
        self.base_path = base_path

    def load_characters_identity(self, folder ,file_name):
        print(f"{self.base_path}{folder}{file_name}")
        data = read_json_files(self.base_path, folder, file_name )
        return data
   
