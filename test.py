#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *


print('A test. Use q and w to test sounds.')
pygame.init()

zone = pygame.display.set_mode((600,400))

time = 0

font = pygame.font.Font('freesansbold.ttf', 32)

beep1 = pygame.mixer.Sound('beep1.ogg')
beep1.play()
beep2 = pygame.mixer.Sound('beep2.ogg')
beep2.play()
beep3 = pygame.mixer.Sound('beep3.ogg')
beep3.play()
beep4 = pygame.mixer.Sound('beep4.ogg')
beep4.play()

note1 = 0
note2 = 0
note3 = 0    

clock = pygame.time.Clock()

while True:

    zone.fill((100, 200, 0))
    text = font.render(str(time), True, (0, 0, 255))
    zone.blit(text, (10, 50))

    for event in pygame.event.get():
        
        keys = pygame.key.get_pressed()
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_q] and keys[pygame.K_w]:
            note1 = time
            beep1.play()
        elif keys[pygame.K_q]:
            note2 = time
            beep2.play()
        elif keys[pygame.K_w]:
            note3 = time
            beep3.play()

    text1 = font.render(str(note1), True, (0, 0, 255))
    zone.blit(text1, (10, 80))
    text2 = font.render(str(note2), True, (0, 0, 255))
    zone.blit(text2, (10, 110))
    text3 = font.render(str(note3), True, (0, 0, 255))
    zone.blit(text3, (10, 140))


    pygame.display.update()

    clock.tick(60)
    time = time + 1
