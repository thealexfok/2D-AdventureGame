import pygame
import numpy as np
import World.WorldCommon as WC

class WorldObject():

    def __init__(self, path, size, element=None):
        self.path = path if path is not None or element is None else element.get("path")
        self.surf = pygame.image.load(self.path)

        if size is None:
            self.size = np.asfarray(self.surf.get_rect().size) * 4
        else:
            self.size = np.asfarray(size)

        self.surf = pygame.transform.scale(self.surf,(int(self.size[0]), int(self.size[1])))
        self.pos = np.asfarray([0,0])

        if element is not None:
            self.SetCenterPosition(np.asfarray([float(element.get("x")),float(element.get("y"))]))

        self.rect = pygame.Rect(self.pos, self.size)


    def ProcessEvent(self,event):
        return False

    def GetCollisionBox(self):
        return pygame.Rect(self.pos, self.size)

    def SetCenterPosition(self, pos):
        self.pos = pos - (self.size / 2.0)

    def GetCenterPosition(self):
        return self.pos + (self.size / 2.0)

    def Update(self, deltaTime):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def Render(self, screen):
        screen.blit(self.surf, self.rect)