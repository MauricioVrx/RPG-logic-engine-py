import copy
from scripts.world.entities.loader import EntityLoader
from scripts.world.entities.entity import Entity

class EntityManager:

    def __init__(self, loader):
        self.loader = loader

