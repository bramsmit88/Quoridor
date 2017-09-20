# -*- coding: utf-8 -*-
import pygame
import numpy as np

class schotje:
    def __init__(self,x,y,orientatie,spel_config,kleur):
        self.kleur = kleur
        self.x=x
        self.y=y
        self.orientatie = orientatie
        self.x_pos, self.y_pos,self.l,self.b  = self.grid2pos(x,y,spel_config)    
        self.spel_config = spel_config
        self.keydownevents = 0
        
    def drawme(self,gameDisplay):
        x,y,l,b = self.grid2pos(self.x,self.y,self.spel_config)
        rect = pygame.Rect(np.int(x),np.int(y),l,b)
        pygame.draw.rect(gameDisplay, self.kleur, rect)
        
    def grid2pos(self,x_grid,y_grid,spel_config):
        blokgrootte = spel_config['blokgrootte']
        lijndikte = spel_config['lijndikte']
        dx = spel_config['dx']
        dy = spel_config['dy']
        if self.orientatie == 'h':
            l = blokgrootte
            b = lijndikte
            x_pos = dx + (x_grid-1)*(blokgrootte + lijndikte)
            y_pos = dy + y_grid*blokgrootte + (y_grid-1)*lijndikte
        else:
            b = blokgrootte
            l = lijndikte
            x_pos = dx + x_grid*blokgrootte + (x_grid-1)*lijndikte
            y_pos = dy + (y_grid-1)*(blokgrootte+lijndikte)          
        return x_pos, y_pos,l,b
    
    def move(self,event,keyup):
        finish = 0        
        if event.type == pygame.KEYDOWN:  
            # detecteer (nieuwe) keypress
            if keyup ==1: 
                keyup = 0
                self.keydownevents = self.keydownevents + 1
                if self.orientatie == 'h':
                    if (event.key == pygame.K_UP and self.keydownevents == 1 and self.y > 1):
                        self.y = self.y - 1
                    elif (event.key == pygame.K_DOWN and self.keydownevents == 1 and self.y <8):
                        self.y = self.y + 1
                    elif (event.key == pygame.K_LEFT and self.keydownevents == 1 and self.x > 1):
                        self.x = self.x - 1
                    elif (event.key == pygame.K_RIGHT and self.keydownevents == 1 and self.x <9):
                        self.x = self.x + 1
                    elif  (event.key == pygame.K_x and self.keydownevents == 1 ):
                            self.orientatie = 'v'
                    elif event.key == pygame.K_SPACE and self.keydownevents == 1:
                        finish = 1
                else:
                    if (event.key == pygame.K_UP and self.keydownevents == 1 and self.y > 1):
                        self.y = self.y - 1
                    elif (event.key == pygame.K_DOWN and self.keydownevents == 1 and self.y <9):
                        self.y = self.y + 1
                    elif (event.key == pygame.K_LEFT and self.keydownevents == 1 and self.x > 1):
                        self.x = self.x - 1
                    elif (event.key == pygame.K_RIGHT and self.keydownevents == 1 and self.x <8):
                        self.x = self.x + 1
                    elif  (event.key == pygame.K_x and self.keydownevents == 1 ):
                            self.orientatie = 'h'
                    elif event.key == pygame.K_SPACE and self.keydownevents == 1:
                        finish = 1                    
        elif event.type == pygame.KEYUP:
            self.keydownevents = 0
            keyup = 1
        return finish,keyup