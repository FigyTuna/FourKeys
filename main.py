#! /usr/bin/env python

import pygame
import sys
from pygame.locals import *
import keys_classes as k


MINOR = k.Mode("Modes/minor.txt")

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

note1 = k.Note("beep1", beep1)
note2 = k.Note("beep2", beep2)

c = k.Controller(MINOR)

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

    c.render(font, zone)

    output = c.step()

    if(output != 0):

        print(str(output))
    
    pygame.display.update()

    clock.tick(60)
    time = time + 1
