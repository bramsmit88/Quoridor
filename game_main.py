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
    schotje_select.drawme(gameDisplay)
    for i in range(len(schotjes)):
        (schotjes[i]).drawme(gameDisplay)

def checkmove_schotje():
    # mag niet over ander schotje
    # mag niet route afsluiten
    possiblemove = 1
    return possiblemove
       
def checkmove_speler(speler_id):
    zelfdeplek = 0
    if speler_id == 1:
        speler      = Speler1
        selector    = select1
        tegenspeler = Speler2
    else:
        speler      = Speler2
        selector    = select2
        tegenspeler = Speler1
    
    possiblemove = 0
    if not (selector.x == speler.x and selector.y == speler.y):
        if not (selector.x == tegenspeler.x and selector.y == tegenspeler.y):
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
    else: 
        zelfdeplek = 1
        possiblemove = 1
    return possiblemove, zelfdeplek

# spel configuratie
kleur_achtergrond   = (200,200,200)
kleur_lijnen        = (0,0,0)
kleur_speler1       = (0,100,0)
kleur_speler2       = (100,1,100)
kleur_select        = (255,255,0)
kleur_schotje       = (255,0,0)
spel_config = {'blokgrootte': 50, 'lijndikte':10, 'dx': 130, 'dy':40}
Speler1 = Speler.Speler(5,1,spel_config,kleur_speler1,10)
select1 = Speler.Speler(Speler1.x,Speler1.y,spel_config,kleur_select,0)
Speler2 = Speler.Speler(5,9,spel_config,kleur_speler2,10)
select2 = Speler.Speler(Speler2.x,Speler2.y,spel_config,kleur_select,0)
schotje_select = schotje.schotje(1,1,'h',spel_config,kleur_lijnen)
schotjes =[]

#MAIN 
# pygame settings:
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)
Display_width   = 800
Display_height  = 600
gameDisplay     = pygame.display.set_mode((Display_width,Display_height))
pygame.display.set_caption('Quoridor')
clock           = pygame.time.Clock()
#$ MAIN LOOP
gamemode = 1
keydownevents = 0
keyup = 1
done = False
while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
    if gamemode == 1:
        instructie = myfont.render("Speler 1, verzet (of niet) en sluit af met -spatie-!", False, (255,255,0))
        select1 = Speler.Speler(Speler1.x,Speler1.y,spel_config,kleur_select,5)
        gamemode = 2
    
    elif gamemode == 2:
        finish,keyup = select1.move(event,keyup)
        if finish == 1:
            possiblemove,zelfdeplek = checkmove_speler(1)
            if possiblemove:                
                #verplaats
                Speler1 = Speler.Speler(select1.x,select1.y,spel_config,kleur_speler1,10)
                select1 = Speler.Speler(Speler1.x,Speler1.y,spel_config,kleur_select,0)
                if zelfdeplek == 1:
                    gamemode = 3
                else:
                    gamemode = 4
            else:
                finish = 0
                instructie = myfont.render("Speler 1: zet niet mogelijk", False, (255,255,0))
    
    elif gamemode == 3: #speler1: schotje plaatsen
        instructie = myfont.render("Speler 1: verplaats schotje. Druk x om te draaien", False, (255,255,0))
#        schotjes.append(schotje.schotje(1,1,'h',spel_config))
        #verplaats...
        schotje_select.kleur = kleur_schotje
        finish,keyup = schotje_select.move(event,keyup)
        if finish == 1:
            possiblemove = checkmove_schotje()
            if possiblemove == 1:
                schotjes.append(schotje.schotje(schotje_select.x,schotje_select.y,schotje_select.orientatie,spel_config,kleur_schotje))
                gamemode = 4
            else:
                finish = 0
    
    elif gamemode == 4:
        instructie = myfont.render("Speler 2, verzet (of niet) en sluit af met -spatie-!", False, (255,255,0))
        select2 = Speler.Speler(Speler2.x,Speler2.y,spel_config,kleur_select,5)
        gamemode = 5    

    elif gamemode == 5:    
        finish,keyup = select2.move(event,keyup)
        if finish == 1:
            possiblemove, zelfdeplek = checkmove_speler(2)
            if possiblemove:
                Speler2 = Speler.Speler(select2.x,select2.y,spel_config,kleur_speler2,10)
                select2 = Speler.Speler(Speler2.x,Speler2.y,spel_config,kleur_select,0)    
                gamemode = 1
            else:
                finish = 0
                instructie = myfont.render("Speler 2: zet niet mogelijk", False, (255,255,0))
                
        


            
                
                

    drawall()  
    gameDisplay.blit(instructie, (10, 10))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
