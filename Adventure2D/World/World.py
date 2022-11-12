import pygame
import numpy as np
import pymunk
import pymunk.pygame_util
import xml.etree.ElementTree as ET
import World.WorldCommon as WC
from World.WorldObject import WorldObject
from World.Chars.Player import Player
from World.Chars.Enemy import Enemy

def Init(screen_size, screen):
    global _grass
    global _objectRect
    global _worldObjects
    global _draw_options
    ##Move to adventure, as ui is init before world and player hp bar wont show
    # WC.ScreenSize = np.array(screen_size)
    WC.ScreenSize = np.array(screen_size)
    WC.PhysicsEngine = pymunk.Space()
    WC.PhysicsEngine.gravity = 0,0
    _draw_options = pymunk.pygame_util.DrawOptions(screen)

    tree = ET.parse("Data/WorldData.xml")
    root = tree.getroot() # root is "World" element

    player = root.find("Player")
    if player != None:
        name = player.get("name")
        path = player.get("path")
        WC.Players[0] = Player(element=player, name=name)
        WC.Players[0].SetCenterPosition(WC.ScreenSize / 2, teleport = True)
        _worldObjects = [WC.Players[0]]
    else:
        _worldObjects = []


    objects = root.find("Objects")
    if objects != None:
        for object in objects.findall("Object"):
            wo = WorldObject(element=object)
            _worldObjects.append(wo)

    enemies = root.find("Enemies")
    if enemies != None:
        for enemy in enemies.findall("Enemy"):
            name = enemy.get("name")
            wo = Enemy(element=enemy, name = name)
            _worldObjects.append(wo)        

    _grass = pygame.image.load("TinyAdventurePack/Other/Grass.png")
    _grass = pygame.transform.scale(_grass, WC.ObjectSize)
    _objectRect = pygame.Rect(0, 0, WC.ObjectSize[0], WC.ObjectSize[1]) 

def ProcessEvent(event):
    global _worldObjects

    for i in _worldObjects:
        if i.ProcessEvent(event) == True:
            return True

    return False

def _SortWorldObjects(worldObject):
    box = worldObject.GetCollisionBox()
    return box.y + box.height

_timeStep = 1.0/60.0
_timeSinceLastFrame=0
def Update(deltaTime):
    global _worldObjects 
    global _timeStep
    global _timeSinceLastFrame

    _timeSinceLastFrame += deltaTime
    while( _timeSinceLastFrame >= _timeStep):
        WC.PhysicsEngine.step(_timeStep)
        _timeSinceLastFrame -= _timeStep

    WC.CameraXY= (WC.ScreenSize/2) - WC.Players[0].GetCenterPosition()

    for i in _worldObjects:
        i.Update(deltaTime)
    
    for i in range(len(_worldObjects)-1, -1, -1):
        if _worldObjects[i].timeToDestruction == 0:
            WC.PhysicsEngine.remove(_worldObjects[i].shape, _worldObjects[i].body)
            del _worldObjects[i]
        

    for i in _worldObjects:
        i.DetectCol()
        i.ProcessCollision()

    if len(WC.NewWorldObjects) >0:
        _worldObjects += WC.NewWorldObjects
        WC.NewWorldObjects.clear()

    _worldObjects.sort(key=_SortWorldObjects)



def Render(screen):
    global _grass
    global _objectRect
    global _worldObjects
    global _draw_options

    for i in range(0,  WC.ScreenSize[0], WC.ObjectSize[0]):
        for j in range(0, WC.ScreenSize[1], WC.ObjectSize[1]):
            screen.blit(_grass, (i,j))

    for i in _worldObjects:
        i.Render(screen) 
    ## show collision box
    #WC.PhysicsEngine.debug_draw(_draw_options)

def Cleanup():
    pass