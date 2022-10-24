import pygame
pygame.init()

size = width, height = 640, 480

screen = pygame.display.set_mode(size)

import World.World as World
World.Init(size,screen)

def Update(deltaTime):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if World.ProcessEvent(event) == True:
            continue
        
        
    World.Update(deltaTime)
    return True

def Render(screen):
    screen.fill((0,0,0))
    World.Render(screen)
    pygame.display.flip()

_gTicksLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render(screen)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTicksLastFrame) / 1000.0 
    _gTicksLastFrame = t
World.Cleanup()