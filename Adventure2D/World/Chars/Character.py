import pygame
import pymunk
import numpy as np

import World.WorldCommon as WC
import World.World as World
from World.WorldObject import WorldObject

class Character(WorldObject):
    def __init__(self, path, size, element = None,name=None):
        self.collisionList = []
        if element is not None:
            path = element.get("path", "")
        if path != "":
            path += "/Idle/Char_idle_down.png"
            self.surf = pygame.image.load(path)
        super().__init__(path=path, size=size, element=element,name=name, body_type=pymunk.Body.KINEMATIC)
        
        

    def DetectCol(self):
        
        collisionbodies=[]
        result = WC.PhysicsEngine.shape_query(self.shape)
        for r in result:
            points = r.contact_point_set.points
            collisionbodies.append(r.shape._get_body())
            for object in World._worldObjects:
                if object.body in collisionbodies:
                    self.collisionList.append(object)
            if len(points) > 0:
                n = r.contact_point_set.normal * points[0].distance
                p = self.GetCenterPosition()
                p += n # Back out the movement to not overlapping
                
                self.SetCenterPosition(p)
                return True
        
        return False

    def ProcessCollision(self):
        pass

    def Update(self, deltaTime):
        super().Update(deltaTime)

    def Render(self, screen):
        screen.blit(self.surf, self.pos, self.col_rect)