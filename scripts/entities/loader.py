import copy
from scripts.system import read_json_files
from scripts.entities.entity import Entity

class EntityLoader:
    def __init__(self, base_path):
        self.base_path=base_path
