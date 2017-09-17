# -*- coding: utf-8 -*-
import pygame
import numpy as np

import Speler # eigen class
import schotje


#fucnties
def drawall():
    gameDisplay.fill(kleur_lijnen) 
    # grid
    blokgrootte = spel_config['blokgrootte']
    lijndikte = spel_config['lijndikte']
    dx = spel_config['dx']
    dy = spel_config['dy']
    for y in range(0,9):
        for x in range(0,9):
            rect = pygame.Rect(dx+x*(blokgrootte+lijndikte), dy+y*(blokgrootte+lijndikte), blokgrootte, blokgrootte)
            pygame.draw.rect(gameDisplay, kleur_achtergrond, rect)            
    # pionnen
    Speler1.drawme(gameDisplay)
    Speler2.drawme(gameDisplay)
    #bloktest.drawme(gameDisplay)
    for i in range(len(schottestrij)):
        (schottestrij[i]).drawme(gameDisplay)




## initialisatie
# pygame settings:
pygame.init()
Display_width   = 800
Display_height  = 600
gameDisplay     = pygame.display.set_mode((Display_width,Display_height))
pygame.display.set_caption('Quoridor')
clock           = pygame.time.Clock()

# spel configuratie
kleur_achtergrond   = (200,200,200)
kleur_lijnen        = (0,0,0)
kleur_speler1       = (0,100,0)
kleur_speler2       = (100,1,100)
kleur_select        = (255,255,0)
spel_config = {'blokgrootte': 50, 'lijndikte':10, 'dx': 130, 'dy':40}
Speler1 = Speler.Speler(5,1,spel_config,kleur_speler1)
Speler2 = Speler.Speler(5,9,spel_config,kleur_speler2)

schottestrij =[]
schottestrij.append(schotje.schotje(1,3,'h',spel_config))
schottestrij.append(schotje.schotje(3,3,'h',spel_config))
#
quitrequested = 0
while not quitrequested:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #als op kruisje wordt gedrukt
            quitrequested = True
   
    #main game loop:    
    drawall()
    
    
    pygame.display.update()
    clock.tick(50) #in fps
pygame.quit()


