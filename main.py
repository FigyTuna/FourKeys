#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *
import RPi.GPIO as GPIO
import keys_classes as K
import keys_settings

if len(sys.argv) > 1:
    if "settings" == sys.argv[1]:

        keys_settings.settings()
        sys.exit()
                

#17, 27, 22, 23, 24, 25
button = keys_settings.readFile("settings.txt", 0, 6)

GPIO.setmode(GPIO.BCM)

for i in range(0, 6):

    GPIO.setup(button[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

zone = pygame.display.set_mode((600,400))

time = 0

font = pygame.font.Font('freesansbold.ttf', 32)

if len(sys.argv) >= 2:
    s = K.Song(font, zone, "Songs/" + str(sys.argv[1]) + ".txt")
else:
    s = K.Song(font, zone, "Songs/free.txt")

if len(sys.argv) == 4:
    s.override(K.Mode("Modes/" + str(sys.argv[2]) + ".txt"), int(sys.argv[3]))

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
        #s.step(keys[pygame.K_q],
        #       keys[pygame.K_w],
        #       keys[pygame.K_o],
        #       keys[pygame.K_p],
        #       keys[pygame.K_s],
        #       keys[pygame.K_l])

    # + 1 % 2 for weird backwards inputs
    s.step((GPIO.input(button[0]) + 1) % 2,
           (GPIO.input(button[1]) + 1) % 2,
           GPIO.input(button[2]),
           GPIO.input(button[3]),
           (GPIO.input(button[4]) + 1) % 2,
           GPIO.input(button[5]))
    
    pygame.display.update()

    clock.tick(60)
    time = time + 1
