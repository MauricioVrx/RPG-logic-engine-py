import copy
from scripts.entities.loader import EntityLoader
from scripts.entities.entity import Entity

class EntityManager:

    def __init__(self, loader):
        self.loader = loader

