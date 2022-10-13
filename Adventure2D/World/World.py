import pygame
import numpy as np
import xml.etree.ElementTree as ET
import World.WorldCommon as WC
from World.WorldObject import WorldObject
from World.Chars.Player import Player

def Init(screen_size):
    global _grass
    global _objectRect
    global _worldObjects
    global _players
    global _charsize
    WC.ScreenSize = np.array(screen_size)

    # _char = pygame.image.load("TinyAdventurePack/Character/Char_one/Idle/Char_idle_down.png")
    # _charsize= np.asfarray([30,25])
    # _char = pygame.transform.scale(_char, WC.ScreenSize/2)
    
    WC.Players[0]= Player("TinyAdventurePack/Character/Char_one/Idle/Char_idle_down.png", WC.ObjectSize)
    WC.Players[0].SetCenterPosition(WC.ScreenSize / 2)
    _worldObjects = [WC.Players[0]]
    # _worldObjects = []

    tree = ET.parse("Data/WorldData.xml")
    root = tree.getroot() # root is "World" element

    objects = root.find("Objects")
    if objects != None:
        for object in objects.findall("Object"):
            wo = WorldObject(None, None, element=object)
            _worldObjects.append(wo)

    player = root.find("Player")
    if player != None:
        char = Player(None, None, element=player)
        _players.append(char)
            

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

def Update(deltaTime):
    global _worldObjects 

    for i in _worldObjects:
        i.Update(deltaTime)
    _worldObjects.sort(key=_SortWorldObjects)

def Render(screen):
    global _grass
    global _objectRect
    global _worldObjects

    for i in range(0,  WC.ScreenSize[0], WC.ObjectSize[0]):
        for j in range(0, WC.ScreenSize[1], WC.ObjectSize[1]):
            screen.blit(_grass, (i,j))
    # screen.blit(_char, (WC.ScreenSize - (_charsize)) / 2.0,(0,0,_charsize[0],_charsize[1]))
    for i in _worldObjects:
        i.Render(screen) 

def Cleanup():
    pass