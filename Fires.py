import pygame
from pygame.locals import *
import numpy as np 
import random

prob = 0.6
terrain_size = (500,500)

# clear land, ie. dirt and desert that are not consumed by fires (brownish)
clear = [125,75,20]
# woods, forest, combustible pixels that go boom
fuel = [0,255,0]
# literally on fire mua ha ha
burning = [255,0,0]

FramePerSec = pygame.time.Clock()
FPS = 45

class Main:
    def __init__(self):
        # and so it begins...
        self.running = True
        self.display_surf = None
        self.size = self.width, self.height = terrain_size
        # state holds the current state/numpy array of the screen
        self.state = np.zeros(terrain_size)
        # creates random fuel/clear cells
        self.state = np.random.choice([0,1],size=terrain_size,p=[1-prob,prob])
        self.state[self.state.shape[0]*2//5:self.state.shape[0]*3//5, self.state.shape[1]*2//5:self.state.shape[1]*3//5] = np.random.choice([0,1,2],size=(100,100),p=[0.99-prob,prob,0.01])
        self.disp()
        self.pos = (-50,-50)
        self.dims = 51
        self.player = Player()
 
    def init(self):
        # initializes pygame
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.running = True
        
    def disp(self):
        # displays the current frame by converting array into RGB
        self.colored = np.zeros((*terrain_size,3),dtype=np.uint8)
        for x in range(self.state.shape[0]):
            for y in range(self.state.shape[1]):
                value = self.state[x,y].copy()
                if value == 0:
                    self.colored[x,y] = clear
                elif value == 1: 
                    self.colored[x,y] = fuel
                elif value == 2: 
                    self.colored[x,y] = burning
        self.surf = pygame.surfarray.make_surface(self.colored)
                    
    def update(self):
        # with each new frame the fire burns away...
        temp = self.state.copy()
        for x in range(self.width//2 - self.dims, self.width//2 + self.dims):
            for y in range(self.height//2 - self.dims, self.height//2 + self.dims):
                if self.state[x,y] == 2: 
                    # for each cell on fire, there is a 25% chance it will die out from lack of fuel/natural causes
                    if random.random() < 0.25:
                        temp[x,y] = 0 
                    # if fire truck to rescue, then it will be put out
                    elif self.pos[0]-50 < x < self.pos[0]+50 and self.pos[1]-50 < y < self.pos[1]+50:
                        temp[x,y] = 0
                    # fire spreads into surrounding cells with fuel (50% chance)
                    else:      
                        for i in [(x-1,y), (x,y+1), (x+1,y), (x,y-1), (x-1,y-1), (x-2,y), (x-1,y+1), (x,y+2), (x+1,y+1), (x+2,y), (x+1,y-1), (x,y-2)]:
                            if self.state[i[0], i[1]] == 1 and random.random() < 0.50:
                                temp[i[0], i[1]] = 2
        if self.dims < 249:
            self.dims += 2
        self.state = temp
 
    def event(self, event):
        # On event of user interaction
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)

    def cleanup(self):
        # Quits game :(
        pygame.quit()
 
    def execute(self):
        # Primary game loop
        if self.init() == False:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.event(event)
            # updates the fire and firetruck player sprite
            self.update()
            self.disp()
            self.display_surf.blit(self.surf, (0, 0))
            self.display_surf.blit(self.player.surf, self.player.rect)
            pygame.display.update()
            FramePerSec.tick(FPS)
        self.cleanup()
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # creates brave firetruck protagonist
        super(Player, self).__init__()
        self.surf = pygame.image.load("firetruck.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        # Commands for sprite, space bar causes firefighters to use fire hose to put out surrounding fires
        if pressed_keys[K_SPACE]:
            Main.pos = self.rect.center
        
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
            
if __name__ == "__main__" :
    Main = Main()
    Main.execute()