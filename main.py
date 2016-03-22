#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *

#Add one more class possibly for keys using GPIO

class Key:

    def __init__(self, x):

        self.xPos = x
        self.state = 0

    def press(self):

        self.state = 1
        
    def clear(self):
        
        self.state = 0

    def render(self):

        self.text = font.render(str(self.state), True, (0, 0, 255))
        zone.blit(self.text, (self.xPos, 300))

class Controller:

    #Holds keys
    #Handles input methods
    #provides an output "note" which may be modified later

    def __init__(self):

        print("Placeholder")

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


print('A test. Use q and w to test sounds.')
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

key1 = Key(50)
key2 = Key(80)

#---

clock = pygame.time.Clock()

while True:

    zone.fill((100, 200, 0))

    for event in pygame.event.get():
        
        keys = pygame.key.get_pressed()
        
        if event.type == QUIT or keys[pygame.K_z]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_q]:
            key1.press()
            note1.play()
        if keys[pygame.K_w]:
            key2.press()
            note2.play()

    key1.render()
    key2.render()

    pygame.display.update()

    key1.clear()
    key2.clear()

    clock.tick(60)
    time = time + 1
