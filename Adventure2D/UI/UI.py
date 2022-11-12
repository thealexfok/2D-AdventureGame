import pygame
import xml.etree.ElementTree as ET
from UI.UIImage import UIImage
from UI.UIText import UIText
from UI.UIButton import UIButton

def GetElementByID(id):
    global _uiIds
    return _uiIds[id]

def GetElementByName(name):
    global _uiNames
    return _uiNames[name]

def Init():
    global _uiObjects
    global _uiIds
    global _uiNames
    _uiObjects = []
    _uiIds = {}
    _uiNames = {}

    tree = ET.parse("Data/UI.xml")
    root = tree.getroot() # root is "UI" element
    groups = root.findall("Group")
    ###flyweight in the future
    if groups != None:
        for group in groups:
            if group != None:
                for element in group.findall("*"):
                    if element.tag == "Image":
                        img = UIImage(element)
                        _uiObjects.append(img)
                        #print(img)
                    elif element.tag == "Text":
                        img = UIText(element)
                        _uiObjects.append(img) 
                    elif element.tag == "Button":
                        img = UIButton(element)
                        _uiObjects.append(img) 
                    else:
                        img = None

                    if img != None:
                        id = element.get("id")
                        if id != None:
                            _uiIds[id] = img
                    if img != None:
                        name = group.get("name")
                        if name != None:
                            _uiNames[name] = img
                
def ProcessEvent (event):
    global _uiObjects
    for i in reversed(_uiObjects):
        if i.ProcessEvent(event) == True:
            return True
    return False

def Update(deltaTime):
    global _uiObjects
    for i in _uiObjects:
        i.Update(deltaTime)

def Render(screen):
    global _uiObjects
    for i in _uiObjects:
        i.Render(screen)

def Cleanup():
    pass