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

class Mode:

    def __init__(self, modeFile):

        self.arr = []

        f = open(modeFile, 'r')

        for i in range(0, 16):

            self.arr.append(int(f.readline()))

    def get(self, key):

        return self.arr[key]

    def getBack(self, note):

        for i in range(0, 16):

            if(self.arr[i] % 12 == note % 12):

                return i

        return 0


MODES = [Mode("Modes/minor.txt"),
         Mode("Modes/major.txt")]

class Key:

    def __init__(self, x, y, octave):

        self.xPos = x
        self.yPos = y
        self.octave = octave
        self.state = False

    def setState(self, state):

        self.state = state

    def render(self, font, screen):

        text = font.render(str(self.state), True, (0, 0, 255))#Temporary test stuff

        display = I_OFF

        if self.octave:
            display = I_O_OFF
        
        if self.state and not self.octave:
            display = I_ON
            
        if self.state and self.octave:
            display = I_O_ON
            
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

        self.keys.append(Key(x, y, False))
        self.keys.append(Key(x + 80, y, False))
        self.keys.append(Key(x + 160, y, False))
        self.keys.append(Key(x + 240, y, False))
        self.keys.append(Key(x, y + 50, True))
        self.keys.append(Key(x + 160, y + 50, True))

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

                return i
            
        return 0#a0

    def display(self, key):

        print(self.notes[key + self.modulation].name)

class Song:

    def __init__(self, font, zone, songFile):

        self.font = font
        self.zone = zone
        self.arr = []

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

            print(str(self.controller.mode.getBack(self.instrument.getBack(self.arr[i]))))

    def override(self, mode, mod):

        self.controller.mode = mode
        self.instrument.modulation = mod

    def step(self, b1, b2, b3, b4, b5, b6):

        self.controller.setState([b1, b2, b3, b4, b5, b6])

        self.controller.render(self.font, self.zone)

        output = self.controller.step()

        if(output != 0):

            self.instrument.display(output)
            self.instrument.play(output)

        





