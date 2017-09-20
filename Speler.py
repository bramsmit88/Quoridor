# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 19:46:59 2017

@author: BSmit
"""
import pygame
import numpy as np

class Speler:
    def __init__(self,x,y,spel_config,kleur,r):
        self.x = x
        self.y = y
        self.spel_config = spel_config
        self.kleur  = kleur
        self.r = r
        self.keydownevents = 0
        
    def drawme(self,gameDisplay):
        kleur = self.kleur
        x_pixel, y_pixel = self.grid2pos(self.x,self.y,self.spel_config)
        pygame.draw.circle(gameDisplay,kleur,(np.int(x_pixel),np.int(y_pixel)),self.r)
    
    def grid2pos(self,x_grid,y_grid,spel_config):
        blokgrootte = spel_config['blokgrootte']
        lijndikte = spel_config['lijndikte']
        dx = spel_config['dx']
        dy = spel_config['dy']
        x_pos = dx + (x_grid-.5)*blokgrootte + (x_grid-1)*lijndikte
        y_pos = dy + (y_grid-.5)*blokgrootte + (y_grid-1)*lijndikte
        return x_pos, y_pos
    
    def move(self,event,keyup):
        finish = 0        
        if event.type == pygame.KEYDOWN:       
            # detecteer (nieuwe) keypress
            if keyup ==1: 
                keyup = 0
                self.keydownevents = self.keydownevents + 1
                if (event.key == pygame.K_UP and self.keydownevents == 1 and self.y > 1):
                    self.y = self.y - 1
                elif (event.key == pygame.K_DOWN and self.keydownevents == 1 and self.y <9):
                    self.y = self.y + 1
                elif (event.key == pygame.K_LEFT and self.keydownevents == 1 and self.x > 1):
                    self.x = self.x - 1
                elif (event.key == pygame.K_RIGHT and self.keydownevents == 1 and self.x <9):
                    self.x = self.x + 1
                elif event.key == pygame.K_SPACE and self.keydownevents == 1:
                    finish = 1
        elif event.type == pygame.KEYUP:
            self.keydownevents = 0
            keyup = 1
        return finish,keyup
