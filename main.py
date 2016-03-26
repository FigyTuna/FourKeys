#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *
import RPi.GPIO as GPIO
import keys_classes as K


#17, 27, 22, 23, 24, 25
button = K.readFile("settings.txt", 0, 6)

reverse = K.readFile("settings.txt", 6, 7)

if 1 == reverse[0]:
    for i in range(0, 2):
        temp = button[i]
        button[i] = button[3 - i]
        button[3 - i] = temp

    temp = button[4]
    button[4]= button[5]
    button[5] = temp

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

        if keys[pygame.K_f]:
            s.moveDown()

        #For keyboard input when GPIO not in use
        #s.step(keys[pygame.K_q],
        #       keys[pygame.K_w],
        #       keys[pygame.K_o],
        #       keys[pygame.K_p],
        #       keys[pygame.K_s],
        #       keys[pygame.K_l])

    # + 1 % 2 for weird backwards inputs
    s.step(GPIO.input(button[0]),
           GPIO.input(button[1]),
           GPIO.input(button[2]),
           GPIO.input(button[3]),
           (GPIO.input(button[4]) + 1) % 2,
           (GPIO.input(button[5]) + 1) % 2)
    
    pygame.display.update()

    clock.tick(60)
    time = time + 1
