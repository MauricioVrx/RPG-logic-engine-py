import copy
from scripts.system.files_manager import read_json_files
from scripts.world.entities.entity import Entity

class EntityLoader:
    def __init__(self, base_path):
        self.base_path=base_path
