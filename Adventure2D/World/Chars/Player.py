import pygame
import numpy as np
import pymunk
from pymunk.vec2d import Vec2d
from World.WorldObject import WorldObject
import World.WorldCommon as WC
from World.Chars.Character import Character

class Player(Character):
    _keypressed = {
        pygame.K_w: False,
        pygame.K_a: False,
        pygame.K_s: False,
        pygame.K_d: False}

    def __init__(self, path, size=None, name=None, element=None):
        self.speed = 200.0
        self.mousemove = False
        self.keymove = False
        self.moveDir = np.asfarray([1.0, 0])
        super().__init__(path=path, size=size, name=name, element=element)
        
        self.pos = (WC.ScreenSize - self.size) / 2.0
        
        
    def ProcessEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN :
            left, middle, right = pygame.mouse.get_pressed()

            if left:
                self.mouseTarget = np.asfarray(pygame.mouse.get_pos())
                self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(), self.mouseTarget)
                self.mousemove = True if len != 0 else False
                return True
        elif event.type == pygame.KEYDOWN:
            
            if event.key in Player._keypressed:
                Player._keypressed[event.key] = True
                self.moveDir = np.asfarray([0,0])
                if Player._keypressed[pygame.K_w]:
                    self.moveDir[1] -= 1
                if Player._keypressed[pygame.K_a]:
                    self.moveDir[0] -= 1
                if Player._keypressed[pygame.K_s]:
                    self.moveDir[1] += 1
                if Player._keypressed[pygame.K_d]:
                    self.moveDir[0] += 1
                self.keyTarget = self.GetCenterPosition() + self.moveDir * self.speed
                self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(), self.keyTarget)
                if len == 0:
                    self.keymove = False
                else:
                    self.keymove=True
                return True

        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:

            rock = WorldObject("TinyAdventurePack/Other/Rock.png",
                                np.array([15,15]), body_type=pymunk.Body.DYNAMIC, name = "rock")

            rock.shape.friction = 0
            rock.SetCenterPosition(self.GetCollisionBoxCenter() + (self.moveDir * 45))
            dir = Vec2d(self.moveDir[0], self.moveDir[1])
            #dir[1] = -dir[1]
            rock.body.apply_impulse_at_world_point(dir * 2500.0, rock.body.position)
            rock.timeToDestruction = 2.0
            WC.NewWorldObjects.append(rock)
            return True
            
        elif event.type == pygame.KEYUP:
            if event.key in Player._keypressed:
                Player._keypressed[event.key] = False
                return True

        return False

    def DetectCol(self):
        super().DetectCol()

    def ProcessCollision(self):
        ###Check if player collided with enemy, if so, player disappear 
        if len(self.collisionList) > 1:
            for collided in self.collisionList:
                if collided.name == "Skel":
                    self.timeToDestruction = 0
                    print("run into enemy")
                    return True
        return False

    def Update(self, deltaTime):
        if self.mousemove:
            self.keymove = False
            self.mousemove = WC.MoveDir(self, self.moveDir, self.mouseTarget, self.speed, deltaTime)
        if self.keymove:
            self.mousemove = False
            self.keymove = WC.MoveDir(self, self.moveDir, self.keyTarget, self.speed, deltaTime)
        super().Update(deltaTime)

    def Render(self, screen):
        super().Render(screen)
        
        
        