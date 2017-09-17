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
    select1.drawme(gameDisplay)
    Speler2.drawme(gameDisplay)
    select2.drawme(gameDisplay)
    for i in range(len(schotjes)):
        (schotjes[i]).drawme(gameDisplay)

def checkmove(speler_id):
    if speler_id == 1:
        speler      = Speler1
        selector    = select1
        tegenspeler = Speler2
    else:
        speler      = Speler2
        selector    = select2
        tegenspeler = Speler1
    
    possiblemove = 0
    if not ((selector.x == speler.x and selector.y == speler.y) or (selector.x == tegenspeler.x and selector.y == tegenspeler.y) ):
        if abs(speler.x - selector.x) == 1:
            if abs(speler.y - selector.y) == 0:
                possiblemove = 1
            elif abs(speler.y - selector.y) == 1:
                # mag alleen als er naast de tegenspeler een verticaal schotje staat
                possiblemove = 1 # AANPASSEN!
        elif abs(speler.x - selector.x) == 2:
            if speler.x + 0.5*(selector.x-speler.x) == tegenspeler.x and abs(selector.y-speler.y)==0:
                possiblemove = 1
        if abs(speler.y - selector.y) == 1:
            if abs(speler.x - selector.x) == 0:
                possiblemove = 1
            elif abs(speler.x - selector.x) == 1:
                # mag alleen als er onder/boven de tegenspeler een horizontaal schotje staat
                possiblemove = 1 # AANPASSEN!   
        elif abs(speler.y - selector.y) == 2:
            if speler.y + 0.5*(selector.y-speler.y) == tegenspeler.y and abs(selector.x-speler.x)==0:
                possiblemove = 1
    return possiblemove

# spel configuratie
kleur_achtergrond   = (200,200,200)
kleur_lijnen        = (0,0,0)
kleur_speler1       = (0,100,0)
kleur_speler2       = (100,1,100)
kleur_select        = (255,255,0)
spel_config = {'blokgrootte': 50, 'lijndikte':10, 'dx': 130, 'dy':40}
Speler1 = Speler.Speler(5,1,spel_config,kleur_speler1,10)
select1 = Speler.Speler(Speler1.x,Speler1.y,spel_config,kleur_select,0)
Speler2 = Speler.Speler(5,9,spel_config,kleur_speler2,10)
select2 = Speler.Speler(Speler2.x,Speler2.y,spel_config,kleur_select,0)
schotjes =[]

#schotjes.append(schotje.schotje(1,3,'h',spel_config))
#schotjes.append(schotje.schotje(3,3,'h',spel_config))

#MAIN 
# pygame settings:
pygame.init()
Display_width   = 800
Display_height  = 600
gameDisplay     = pygame.display.set_mode((Display_width,Display_height))
pygame.display.set_caption('Quoridor')
clock           = pygame.time.Clock()
#$ MAIN LOOP
gamemode = 1
keydownevents = 0
done = False
while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
    if gamemode == 1:
        select1 = Speler.Speler(Speler1.x,Speler1.y,spel_config,kleur_select,5)
        gamemode = 2
    
    elif gamemode == 2:
        finish = select1.move(event)
        if finish == 1:
            possiblemove = checkmove(1)
            if possiblemove:                
                #verplaats
                Speler1 = Speler.Speler(select1.x,select1.y,spel_config,kleur_speler1,10)
                select1 = Speler.Speler(Speler1.x,Speler1.y,spel_config,kleur_select,0)
                gamemode = 3
            else:
                finish = 0
    elif gamemode == 3:
        select2 = Speler.Speler(Speler2.x,Speler2.y,spel_config,kleur_select,5)
        gamemode = 4    

    elif gamemode == 4:    
        finish = select2.move(event)
        if finish == 1:
            possiblemove = checkmove(2)
            if possiblemove:
                Speler2 = Speler.Speler(select2.x,select2.y,spel_config,kleur_speler2,10)
                select2 = Speler.Speler(Speler2.x,Speler2.y,spel_config,kleur_select,0)    
                gamemode = 1
            else:
                finish = 0
        


            
                
                

    drawall()    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
