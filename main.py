#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *

#Add one more class possibly for keys using GPIO

class Key:

    def __init__(self, x):

        self.xPos = x
        self.state = False

    def setState(self, state):

        self.state = state

    def render(self):

        self.text = font.render(str(self.state), True, (0, 0, 255))
        zone.blit(self.text, (self.xPos, 300))

class Controller:

    #Holds keys
    #Handles input methods
    #provides an output "note" which may be modified later

    def __init__(self, mode):

        self.mode = mode

        self.timer = 0

        self.keys = []

        self.keys.append(Key(50))
        self.keys.append(Key(80))
        self.keys.append(Key(110))
        self.keys.append(Key(140))
        self.keys.append(Key(200))
        self.keys.append(Key(230))

    def setState(self, k = []):

        for i in range(0, 6):

            self.keys[i].setState(k[i])

    def render(self):

        for i in range(0, 6):

            self.keys[i].render()

    def noteIsDown(self):

        for i in range(0, 6):

            if(self.keys[i].state):

                return True

        return False

class Note:

    def __init__(self, name, soundFile):

        self.name = name #May not be necessary
        self.soundFile = soundFile

    def play(self):

        self.soundFile.play()

class Instrument:

    #Holds all notes
    #Handles modulation

    def __init__(self):

        self.modulation = 0


print('q, w, o, p, s, l. Testing buttons. z to quit.')
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

zone = pygame.display.set_mode((600,400))

time = 0

font = pygame.font.Font('freesansbold.ttf', 32)

#Test stuff

beep1 = pygame.mixer.Sound('Test/beep1.ogg')
beep2 = pygame.mixer.Sound('Test/beep2.ogg')
beep3 = pygame.mixer.Sound('Test/beep3.ogg')
beep4 = pygame.mixer.Sound('Test/beep4.ogg')

note1 = Note("beep1", beep1)
note2 = Note("beep2", beep2)

c = Controller(0)

#---

clock = pygame.time.Clock()

while True:

    zone.fill((100, 200, 0))

    for event in pygame.event.get():
        
        keys = pygame.key.get_pressed()
        
        if event.type == QUIT or keys[pygame.K_z]:
            pygame.quit()
            sys.exit()

        c.setState([keys[pygame.K_q],
                   keys[pygame.K_w],
                   keys[pygame.K_o],
                   keys[pygame.K_p],
                   keys[pygame.K_s],
                   keys[pygame.K_l]])

    c.render()
    
    pygame.display.update()

    clock.tick(60)
    time = time + 1
