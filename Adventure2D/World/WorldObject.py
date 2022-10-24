import pygame
import numpy as np
import pymunk
import World.WorldCommon as WC

class WorldObject():
    def __init__(self, path= None, size=None, element=None, name=None, body_type = pymunk.Body.STATIC):
        self.body = None
        self.name =name
        self.path = path if path is not None or element is None else element.get("path")
        self.surf = pygame.image.load(self.path)
        if size is None:
            self.size = np.asfarray(self.surf.get_rect().size) * 4
        else:
            self.size = np.asfarray(size)
        self.surf = pygame.transform.scale(self.surf,(int(self.size[0]), int(self.size[1])))
        if body_type == 1:
            self.size= np.asfarray([float(self.size[0]/6),self.size[1]])
        self.pos = np.asfarray([0,0])
        if element is not None:
            self.SetCenterPosition(np.asfarray([float(element.get("x")),float(element.get("y"))]))
        self.rect = pygame.Rect(self.pos, self.size)
        
        self.col_type = "capsule"
        if name == "rock":
            self.col_type = "box"
        self.col_rect = pygame.Rect((0,0),self.size)
        if element != None:
            col_elem = element.find("Col")
            if col_elem != None:
                self.col_rect = pygame.Rect((int(col_elem.get("xoff")),
                                            int (col_elem.get("yoff"))),
                                            (int(col_elem.get("w")),
                                            int (col_elem.get("h"))))
                self.col_type = col_elem.get("type")
                #offset += self.col_rect.topleft

        #print(self.col_type)
        

            
        

        mass = 10
        moment = 10

        self.body = pymunk.Body(mass, moment, body_type)

        center = self.GetCollisionBoxCenter()

        self.body.position = center[0],center[1]
        WC.PhysicsEngine.reindex_shapes_for_body(self.body)
        if self.col_type == "capsule":
            box = self.GetCollisionBox()
            w, h = box.size
            ###-40 for offset at sprite empty space
            self.shape = pymunk.Segment(self.body, (0,-(h-40)/4),(0,(h-40)/4),radius=w/4)
            self.shape.elasticity = 0.999

        elif self.col_type == "oval":    
            #box = self.GetCollisionBox()
            w,h = self.col_rect.w, self.col_rect.h
            #start from bottom left
            poly = [(-w/2,-h/4),(-w/4,-h/2), (w/4,-h/2), (w/2,-h/4), (w/2,h/4), (w/4,h/2), (-w/4,h/2),(-w/2,h/4)]
            self.shape = pymunk.Poly(self.body, poly)

        elif self.col_type == "box":    
            box = self.GetCollisionBox()
            self.shape = pymunk.Poly.create_box(self.body, box.size)

        WC.PhysicsEngine.add(self.body, self.shape)
        self.timeToDestruction = -1

    def DetectCol(self):
        pass
    
    def ProcessCollision(self):
        pass

    def ProcessEvent(self,event):
        return False

    def GetCollisionBox(self):
        return pygame.Rect(self.pos + np.asfarray(self.col_rect.topleft), self.col_rect.size)

    def SetCenterPosition(self, pos):
        self.pos = pos - (self.size / 2.0)
        if self.body != None:
            center = self.GetCollisionBoxCenter()
            self.body.position = center[0],center[1]
            WC.PhysicsEngine.reindex_shapes_for_body(self.body)

    def GetCollisionBoxCenter(self):
        box = self.GetCollisionBox()
        return np.asfarray([box.x + (box.w / 2), box.y + (box.h / 2)])

    def GetCenterPosition(self):
        return self.pos + (self.size / 2.0)

    def Update(self, deltaTime):
        if self.body.body_type == pymunk.Body.DYNAMIC:
            center = self.GetCollisionBoxCenter()
            self.pos[0] = self.body.position[0] - (center[0] - self.pos[0])
            self.pos[1] = self.body.position[1] - (center[1] - self.pos[1])

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.timeToDestruction != -1:
            self.timeToDestruction -= deltaTime
            if self.timeToDestruction < 0:
                self.timeToDestruction = 0

    def Render(self, screen):
        screen.blit(self.surf, self.rect)