import pygame
import sys
from pygame.locals import *

DELAY = 4
NOTE_NAMES = ["a", "a#", "b", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#"]

I_ON = pygame.image.load('Images/on.png')
I_OFF = pygame.image.load('Images/off.png')
I_HIT = pygame.image.load('Images/hit.png')
I_O_ON = pygame.image.load('Images/onoctave.png')
I_O_OFF = pygame.image.load('Images/offoctave.png')
I_O_HIT = pygame.image.load('Images/hitoctave.png')
I_INV = pygame.image.load("Images/invisible.png")

HIT_SPACE = 130#pixels

class Mode:

    def __init__(self, modeFile):

        self.arr = []

        f = open(modeFile, 'r')

        for i in range(0, 16):

            self.arr.append(int(f.readline()))

    def get(self, key):

        return self.arr[key]

    def getBack(self, note):

        for i in range(1, 16):

            if(self.arr[i] % 12 == note % 12):

                return i

        return 0


MODES = [Mode("Modes/minor.txt"),
         Mode("Modes/major.txt")]

class Key:

    def __init__(self, x, y, on, off):

        self.xPos = x
        self.yPos = y
        self.on = on
        self.off = off
        self.state = False

    def setState(self, state):

        self.state = state

    def updatePos(self, x, y):

        self.x = x
        self.y = y

    def render(self, font, screen):

        text = font.render(str(self.state), True, (0, 0, 255))#Temporary test stuff

        display = self.off
        
        if self.state:
            display = self.on
            
        screen.blit(display, (self.xPos, self.yPos))

class Controller:

    #Holds keys
    #Handles input methods
    #provides an output "note" which may be modified later

    def __init__(self, mode, x = 140, y = 300):

        self.mode = mode

        self.timer = 0
        self.played = False

        self.keys = []

        self.keys.append(Key(x, y, I_ON, I_OFF))
        self.keys.append(Key(x + 80, y, I_ON, I_OFF))
        self.keys.append(Key(x + 160, y, I_ON, I_OFF))
        self.keys.append(Key(x + 240, y, I_ON, I_OFF))
        self.keys.append(Key(x, y + 50, I_O_ON, I_O_OFF))
        self.keys.append(Key(x + 160, y + 50, I_O_ON, I_O_OFF))

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

        key = key + octave * 12 + (12 * 2)

        return key

    def noteIsDown(self):

        for i in range(0, 4):

            if(self.keys[i].state):

                return True

        return False

class Note:

    def __init__(self, name, soundFile):

        self.name = name
        self.soundFile = pygame.mixer.Sound(soundFile)

    def play(self):

        self.soundFile.play()

class Instrument:

    #Holds all notes
    #Handles modulation

    def __init__(self, mod, folder):

        self.modulation = mod
        self.notes = []

        for i in range(0, (12 * 5) + 1):

            self.notes.append(Note(NOTE_NAMES[(i - 1) % 12] + str(((i - 4) / 12) + 1),
                                   (str(folder) + "/" + str(i) + ".wav")))

    def play(self, key):

        self.notes[key + self.modulation].play()

    def getBack(self, note):

        for i in range(0, len(self.notes)):

            if self.notes[i].name + "\n" == note:

                return i#Needs +- mod
            
        return 0#a0

    def display(self, key):

        print(self.notes[key + self.modulation].name)

class Song:

    def __init__(self, font, zone, songFile):

        self.font = font
        self.zone = zone
        self.arr = []
        self.hits = []

        f = open(songFile, 'r')

        #Abstract maybe later
        self.controller = Controller(MODES[int(f.readline())])
        self.instrument = Instrument(int(f.readline()), "Piano")

        while True:

            line = f.readline()
            if not line:
                break

            self.arr.append(line)

        for i in range(0, len(self.arr)):

            self.hits.append(Hit(self.controller.mode.getBack(self.instrument.getBack(self.arr[i])), 140, 300 - (HIT_SPACE * i)))

        #self.hits[2].moveDown()#Test

    def override(self, mode, mod):

        self.controller.mode = mode
        self.instrument.modulation = mod

    def step(self, b1, b2, b3, b4, b5, b6):

        self.controller.setState([b1, b2, b3, b4, b5, b6])

        self.controller.render(self.font, self.zone)

        for i in range(0, len(self.hits)):

            self.hits[i].render(self.font, self.zone)

        output = self.controller.step()

        if(output != 0):

            self.instrument.display(output)
            self.instrument.play(output)

class Hit:

    def __init__(self, binNum, x, y):

        self.animTime = 0
        self.x = x
        self.y = y

        self.arr = []

        self.arr.append(binNum / 8)
        binNum = binNum % 8
        self.arr.append(binNum / 4)
        binNum = binNum % 4
        self.arr.append(binNum / 2)
        binNum = binNum % 2
        self.arr.append(binNum)

        self.keys = []

        self.keys.append(Key(x, y, I_HIT, I_INV))
        self.keys.append(Key(x + 80, y, I_HIT, I_INV))
        self.keys.append(Key(x + 160, y, I_HIT, I_INV))
        self.keys.append(Key(x + 240, y, I_HIT, I_INV))
        self.keys.append(Key(x, y + 50, I_O_HIT, I_INV))
        self.keys.append(Key(x + 160, y + 50, I_O_HIT, I_INV))

        for i in range(0, 4):

            self.keys[i].setState(self.arr[i])

    def render(self, font, screen):

        for i in range(0, 6):

            self.keys[i].updatePos(self.x, self.y - self.animTime)
            self.keys[i].render(font, screen)

        self.animTime -= 1

    def moveDown(self):

        self.animTime = HIT_SPACE
        self.y += HIT_SPACE


