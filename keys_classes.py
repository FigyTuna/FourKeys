import pygame
import sys
from pygame.locals import *

DELAY = 4

class Mode:

    def __init__(self, modeFile):

        self.arr = []

        f = open(modeFile, 'r')

        for i in range(0, 16):

            self.arr.append(int(f.readline()))

    def get(self, key):

        return self.arr[key]

class Key:

    def __init__(self, x):

        self.xPos = x
        self.state = False

    def setState(self, state):

        self.state = state

    def render(self, font, screen):

        text = font.render(str(self.state), True, (0, 0, 255))#Temporary test stuff
        screen.blit(text, (self.xPos, 300))

class Controller:

    #Holds keys
    #Handles input methods
    #provides an output "note" which may be modified later

    def __init__(self, mode):

        self.mode = mode

        self.timer = 0
        self.played = False

        self.keys = []

        self.keys.append(Key(50))#Temp values
        self.keys.append(Key(80))
        self.keys.append(Key(110))
        self.keys.append(Key(140))
        self.keys.append(Key(200))
        self.keys.append(Key(230))

    def setState(self, k = []):

        for i in range(0, 6):

            self.keys[i].setState(k[i])

    def render(self, font, screen):

        for i in range(0, 6):

            self.keys[i].render(font, screen)

    def step(self):

        if(self.noteIsDown()):

            self.timer += 1

        else:

            self.timer = 0
            self.played = False

        if(self.timer > DELAY and not self.played):

            self.played = True
            return self.currentOutput()

        return 0

    def currentOutput(self):

        key = self.mode.get(self.keys[3].state +
                            self.keys[2].state * 2 +
                            self.keys[1].state * 4 +
                            self.keys[0].state * 8)

        octave = (self.keys[4].state * (-1) +
                  self.keys[5].state)

        key = key + octave * 12 + 12

        return key

    def noteIsDown(self):

        for i in range(0, 4):

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
