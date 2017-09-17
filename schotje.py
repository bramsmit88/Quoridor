# -*- coding: utf-8 -*-
import pygame
import numpy as np

class schotje:
    def __init__(self,x,y,orientatie,spel_config):
        self.orientatie = orientatie
        self.x, self.y,self.l,self.b  = self.grid2pos(x,y,spel_config)    

    def drawme(self,gameDisplay):
        kleur = (250,250,0)
        rect = pygame.Rect(np.int(self.x),np.int(self.y),self.l,self.b)
        pygame.draw.rect(gameDisplay, kleur, rect)
        
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