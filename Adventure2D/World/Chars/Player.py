import pygame
import numpy as np
import World.WorldCommon as WC
from World.Chars.Character import Character

class Player(Character):
    _keypressed = {
        pygame.K_w: False,
        pygame.K_a: False,
        pygame.K_s: False,
        pygame.K_d: False}

    def __init__(self, path, size,element=None):
        self.speed = 200.0
        self.mousemove = False
        self.keymove = False
        self.mousedir = np.asfarray([1.0, 0])
        self.keydir = np.asfarray([1.0,0])
        super().__init__ (path, size,element)

    def ProcessEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN :
            left, middle, right = pygame.mouse.get_pressed()

            if left:
                self.mouseTarget = np.asfarray(pygame.mouse.get_pos())
                self.mousedir, len = WC.ComputeDir(self.GetCenterPosition(), self.mouseTarget)
                self.mousemove = True if len != 0 else False
                return True

        if event.type == pygame.KEYDOWN:
            if event.key in Player._keypressed:
                Player._keypressed[event.key] = True
                if Player._keypressed[pygame.K_w]:
                    self.keydir[1] -= 1
                    self.keymove = True
                if Player._keypressed[pygame.K_a]:
                    self.keydir[0] -= 1
                    self.keymove = True
                if Player._keypressed[pygame.K_s]:
                    self.keydir[1] += 1
                    self.keymove = True
                if Player._keypressed[pygame.K_d]:
                    self.keydir[0] += 1
                    self.keymove = True
                self.keyTarget = self.GetCenterPosition() + self.keydir * self.speed
                self.keydir, len = WC.ComputeDir(self.GetCenterPosition(), self.keyTarget)
                self.keymove = True if len != 0 else False
                return True

        elif event.type == pygame.KEYUP:
            if event.key in Player._keypressed:
                Player._keypressed[event.key] = False
                return True

        return False

    def Update(self, deltaTime):
        if self.mousemove:
            self.mousemove = WC.MoveDir(self, self.mousedir, self.mouseTarget, self.speed, deltaTime)
        if self.keymove:
            self.keymove = WC.MoveDir(self, self.keydir, self.keyTarget, self.speed, deltaTime)
        super().Update(deltaTime)

    def Render(self, screen):
        super().Render(screen)