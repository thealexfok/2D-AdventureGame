import pygame
import numpy as np
import threading
import requests
import json
from flask import jsonify
import World.World as World
import UI.UI as UI
import World.WorldCommon as WC
from UI.UIButton import RegisterButtonAction

pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.mixer.init(frequency=22050,size=16,channels=2,buffer=4096)
pygame.mixer.music.load("Data/bensound-epic.ogg")

WC.ScreenSize = np.array(size)
UI.Init()
World.Init(size,screen)

def StartForRealThisTime():
    r = requests.get(url = "http://localhost:5005/newgame/0")
    data = r.json()
    WC.Players[0].SetCenterPosition(np.asfarray([data['x'],data['y']]), teleport = True)
    WC.TogglePause = True

def StartGame():
    for b in ["newWorldButton","loadGameButton","volume-","volume+"]:
        button = UI.GetElementByID(b)
        button.visible = False
    #WC.TogglePause = True
    t = threading.Thread(target=StartForRealThisTime)
    t.start()

RegisterButtonAction("StartGame", StartGame)


# Load Game
def LoadPos():
    r = requests.get(url = "http://localhost:5005/savepos/0")
    data = r.json()
    WC.Players[0].SetCenterPosition(np.asfarray([data['x'],data['y']]), teleport = True)
    WC.TogglePause = True

def LoadGame():
    for b in ["newWorldButton","loadGameButton","volume-","volume+"]:
        button = UI.GetElementByID(b)
        button.visible = False
    #WC.TogglePause = True
    t = threading.Thread(target=LoadPos)
    t.start()

RegisterButtonAction("LoadGame", LoadGame)

def SaveGame():
    
    currentpos = WC.Players[0].GetCenterPosition()
    pos = {'x':currentpos[0], 'y':currentpos[1]}
    print(pos)
    r = requests.post(url = "http://localhost:5005/savepos/0", json = pos)
    print("Autosaving")
    #r.json()

def AutoSave():
    #WC.TogglePause = True
    t = threading.Thread(target=SaveGame)
    t.start()

def VolUp():
    volume = pygame.mixer.music.get_volume()
    if volume < 1:
        volume += 0.1
        if volume > 1:
            volume = 1.0
        pygame.mixer.music.set_volume(volume)
        SaveSettings()
RegisterButtonAction("Volume+", VolUp)

def VolDown():
    volume = pygame.mixer.music.get_volume()
    if volume > 0:
        volume -= 0.1
        if volume < 0:
            volume = 0.0
        pygame.mixer.music.set_volume(volume)
        SaveSettings()
RegisterButtonAction("Volume-", VolDown)

pygame.mixer.music.play(loops = -1)
try:
    with open("SettingsFile.txt","r") as setFile:
        for line in setFile:
            i = line.find("volume ", 0, 7)
            if i != -1:
                volume = float(line[7:])
                if volume > 1:
                    volume = 1
                elif volume < 0:
                    volume = 0
                print(volume)
                pygame.mixer.music.set_volume(volume)
                continue

            i = line.find("END\n", 0, 4)
            if i != -1:
                break
except:
    pass

SettingsFile = open("SettingsFile.txt", "w")
def SaveSettings():
    global SettingsFile
    
    volume = pygame.mixer.music.get_volume()
    #print(volume)
    SettingsFile.write("volume " + str(volume) + "\n")
    SettingsFile.write("END\n")
    SettingsFile.flush()
    SettingsFile.seek(0,0)
SaveSettings()

_timetosave = 3
def Update(deltaTime):
    global _timetosave

    if WC.TogglePause:
        WC.Paused = not WC.Paused
        WC.TogglePause = False

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if UI.ProcessEvent(event) == True:
            continue
        if WC.Paused:
            continue
        if World.ProcessEvent(event) == True:
            continue
    if not WC.Paused:
        World.Update(deltaTime)
    UI.Update(deltaTime)
    if _timetosave > 0:
        _timetosave -= deltaTime
        
    else:
        AutoSave()
        _timetosave = 3
    #print(_timetosave)
    ####Send save request to server every 3 seconds
    #print(_timeStep)

    return True

def Render(screen):
    screen.fill((0,0,0))
    World.Render(screen)
    UI.Render(screen)
    pygame.display.flip()

_gTicksLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0

while Update(_gDeltaTime):
    Render(screen)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTicksLastFrame) / 1000.0 
    _gTicksLastFrame = t
World.Cleanup()