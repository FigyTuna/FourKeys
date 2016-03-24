#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *
import RPi.GPIO as GPIO
import keys_classes as K


MINOR = K.Mode("Modes/minor.txt")
MAJOR = K.Mode("Modes/major.txt")
#17, 27, 22, 23, 24, 25
button = [24, 23, 17, 27, 25, 22]

GPIO.setmode(GPIO.BCM)

for i in range(0, 6):

    GPIO.setup(button[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

zone = pygame.display.set_mode((600,400))

time = 0

font = pygame.font.Font('freesansbold.ttf', 32)

c = K.Controller(MINOR)
p = K.Instrument(0, "Piano")

#---

clock = pygame.time.Clock()

while True:

    zone.fill((52, 154, 227))

    for event in pygame.event.get():
        
        keys = pygame.key.get_pressed()
        
        if event.type == QUIT or keys[pygame.K_z]:
            pygame.quit()
            sys.exit()

        #For keyboard input when GPIO not in use
        #c.setState([keys[pygame.K_q],
        #            keys[pygame.K_q],
        #            keys[pygame.K_q],
        #            keys[pygame.K_q],
        #            keys[pygame.K_q],
        #            keys[pygame.K_q])

    # + 1 % 2 for weird backwards inputs
    c.setState([(GPIO.input(button[0]) + 1) % 2,
                (GPIO.input(button[1]) + 1) % 2,
                GPIO.input(button[2]),
                GPIO.input(button[3]),
                (GPIO.input(button[4]) + 1) % 2,
                GPIO.input(button[5])])

    c.render(font, zone)

    output = c.step()

    if(output != 0):

        print(str(p.notes[output].name))
        p.play(output)
    
    pygame.display.update()

    clock.tick(60)
    time = time + 1
