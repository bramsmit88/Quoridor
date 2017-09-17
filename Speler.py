# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 19:46:59 2017

@author: BSmit
"""
import pygame
import numpy as np

class Speler:
    def __init__(self,x,y,spel_config,kleur):
        self.x = x
        self.y = y
        self.spel_config = spel_config
        self.kleur  = kleur
        
    def drawme(self,gameDisplay):
        kleur = self.kleur
        r = 10
        x_pixel, y_pixel = self.grid2pos(self.x,self.y,self.spel_config)
        pygame.draw.circle(gameDisplay,kleur,(np.int(x_pixel),np.int(y_pixel)),r)
    
    def grid2pos(self,x_grid,y_grid,spel_config):
        blokgrootte = spel_config['blokgrootte']
        lijndikte = spel_config['lijndikte']
        dx = spel_config['dx']
        dy = spel_config['dy']
        x_pos = dx + (x_grid-.5)*blokgrootte + (x_grid-1)*lijndikte
        y_pos = dy + (y_grid-.5)*blokgrootte + (y_grid-1)*lijndikte
        return x_pos, y_pos
        
