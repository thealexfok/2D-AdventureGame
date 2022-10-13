import pygame
import numpy as np

import World.WorldCommon as WC
from World.WorldObject import WorldObject

class Character(WorldObject):
    def init__(self, path, size,element=None):
        
        
        super ().__init__ (path, size,element)

    def Update(self, deltaTime):
        super().Update(deltaTime)

    def Render(self, screen):
        
        super().Render (screen)