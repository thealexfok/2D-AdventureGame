import pygame
import pymunk
import numpy as np
import random
import math
from enum import IntEnum
import World.WorldCommon as WC
import World.World as World
import UI.UI as UI
from World.WorldObject import WorldObject


class AnimType(IntEnum):
    IDLE = 0
    WALK = 1
    ATTACK = 2

class AnimDir(IntEnum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3


class Character(WorldObject):
    _animFrameLen = 0.1667
    _charWidth = 120
    _charHeight = 100
    _imageCount = 6
    _size = np.array([_charWidth * _imageCount, _charWidth])

    @staticmethod
    def _LdChrSrf (path, folder, name, dir):
        surf, size = WorldObject._LoadSurf(path + '/' + folder + "/Char_" + name + "_" + dir + ".png", Character._size)
        return surf

    def __init__(self, path, size, element = None,name=None):
        self.collisionList = []
        if element is not None:
            path = element.get("path", "")
            self.hp = int(element.get("hp"))
            
        base = path
        if path != "":
            path += "/Idle/Char_idle_down.png"
            self.surf = pygame.image.load(path)
        self.area = pygame.Rect((0,0),(Character._charWidth, Character._charHeight))
        super().__init__(path=path, size=Character._size, element=element,name=name, body_type=pymunk.Body.KINEMATIC)
        self.hpbar = UI.GetElementByName(self.name)
        self.lose = UI.GetElementByID("lose")
        self.win = UI.GetElementByID("win")
        self.hplen = self.hpbar.width/self.hp
        # Outer List: AnimType; Inner List: AnimDir
        self.anims = [[self.surf,
                    Character._LdChrSrf(base, "Idle", "idle", "left"),
                    Character._LdChrSrf(base, "Idle", "idle", "up"),
                    Character._LdChrSrf(base, "Idle", "idle", "right")],
                    [Character._LdChrSrf(base, "Walk", "walk", "down"),
                    Character ._LdChrSrf(base, "Walk", "walk", "left"),
                    Character._LdChrSrf(base, "Walk", "walk", "up"),
                    Character._LdChrSrf(base, "Walk", "walk", "right")],
                    [Character._LdChrSrf(base, "Attack", "atk", "down"),
                    Character ._LdChrSrf(base, "Attack", "atk", "left"),
                    Character._LdChrSrf(base, "Attack", "atk", "up"),
                    Character._LdChrSrf(base, "Attack", "atk", "right")]]
        self.animDir = AnimDir.DOWN
        self.animType = AnimType.IDLE
        self.animTime = random.uniform(0, Character._animFrameLen * Character._imageCount)
        self.charLastPos = self.GetCenterPosition()
        self.walkSound= WorldObject._LoadSoundEffect("Data/Footsteps-in-grass-fast.mp3")
        
    def SetCenterPosition(self, pos, teleport=False):
        super().SetCenterPosition(pos, teleport)
        if teleport:
            self.charLastPos = self.GetCenterPosition()
            
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
                
                self.SetCenterPosition(p,teleport=True)
                return True
        
        return False

    def ProcessCollision(self):
        pass

    def Update(self, deltaTime):
        if self.hp == 0:
            self.hpbar.visible = False
        self.animTime += deltaTime
        if self.animTime >= Character._animFrameLen * Character._imageCount:
            self.animTime -= Character._animFrameLen * Character._imageCount
        frame = self.animTime // Character._animFrameLen
        self.area = pygame.Rect((frame * Character._charWidth, 8), \
                                (Character._charWidth, Character._charHeight))
        curPos = self.GetCenterPosition()
        curDir = curPos - self.charLastPos
        self.charLastPos = curPos

        if curDir[0] != 0 or curDir[1] != 0:
            if math.fabs(curDir[0]) > math.fabs(curDir[1]):
                if curDir[0] > 0:
                    self.animDir = AnimDir.RIGHT
                else:
                    self.animDir = AnimDir.LEFT
            else:
                if curDir[1] > 0:
                    self.animDir = AnimDir.DOWN
                else:
                    self.animDir = AnimDir.UP
        super().Update(deltaTime)

    def Render(self, screen):
        rect = self.rect.copy()
        rect.x += WC.CameraXY[0]
        rect.y += WC.CameraXY[1]
        screen.blit(self.anims[self.animType][self.animDir],rect,self.area)
        # screen.blit(self.surf, self.pos, self.col_rect)