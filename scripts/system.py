import os
import json
from scripts.exceptions import FileNotFoundError

def read_json_files(file_path, folder_name, file_name):
    path = os.path.join(file_path, folder_name ,f"{file_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(file_name, folder_name, "json" )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
