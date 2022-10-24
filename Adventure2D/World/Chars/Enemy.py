import pygame
import numpy as np
import pymunk
from World.Chars.Character import Character
from World.Chars.NPCState import State
import World.WorldCommon as WC

class Enemy(Character):
    def __init__(self, element=None, path=None, size=None, name = None):
        self.speed = 100
        self.moveDir = np.asfarray([1.0, 0])

        self.curState = None
        self.stateList = {}

        if element != None:
            ai = element.find("AI")
            if ai != None:
                for state in ai.findall("State"):
                    s = State(state)
                    self.stateList[s.name] = s
                    if self.curState == None:
                        self.curState = s.name
                        
        super().__init__(element=element,path=path,size=size, name=name)
        
    def DetectCol(self):
        super().DetectCol()
    
    def ProcessCollision(self):
        ###Check if rock collided with enemy, if so, rock disappear with enemy
        if len(self.collisionList) > 1:
            for collided in self.collisionList:
                if collided.name == "rock":
                    collided.timeToDestruction = 0
                    self.timeToDestruction = 0
                    print("hit by rock")
                    return True
        return False

    def Update(self, deltaTime):
        if self.curState != None:
            result = self.stateList[self.curState].Update(self, deltaTime)
            if result is not None:
                self.curState = result         
                self.stateList[self.curState].action.Enter(self)
        super().Update(deltaTime)
    
    def Render(self, screen):
        super().Render(screen)