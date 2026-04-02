import os
import json
from scripts.system.exceptions import FileNotFoundError

def read_json_files(file_path, folder_name, file_name):
    """
    Reads and parses a JSON file from the specified directory.

    This utility function builds the full file path using the provided
    base path, folder name and file name, then loads the JSON content
    into a Python dictionary.

    The function is commonly used by loaders to retrieve structured
    game data such as characters, items, world definitions or identities.

    Parameters
    ----------
    file_path : str
        Base directory path where the folder is located.

    folder_name : str
        Name of the folder containing the JSON file.

    file_name : str
        Name of the JSON file without the ".json" extension.

    Returns
    -------
    dict
        Parsed JSON data loaded as a Python dictionary.

    Raises
    ------
    FileNotFoundError
        If the target JSON file does not exist in the specified path.

    """
    path = os.path.join(file_path, folder_name ,f"{file_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(file_name, folder_name, "json" )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_list_files(path, folder):
    """
     Returns a list of files contained in the specified folder.

    This function is typically used by loaders to iterate through
    multiple JSON files in a directory when loading game data such
    as characters, items, or world entities.

    Parameters
    ----------
    path : str
        Base directory path.

    folder : str
        Folder name to search within the base path.

    Returns
    -------
    list[str]
        List of file names present in the specified folder.

    Example
    -------
    get_list_files("data/world/entities/", "characters")
    """
    list_files = os.listdir(f"{path}{folder}")
    return list_files