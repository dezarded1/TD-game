# #lib
import pygame
import numpy
import pytmx
from settings import *

class HUD:
    def __init__(self):
        self.money=5
        self.health=MAIN_HEALTH
        self.wave=5
        self.hud_width=450
        self.hud_height=150

        self.panel_rect=pygame.Rect(0,0,self.hud_width,self.hud_height)

    def update(self):
        self.money=5
        self.health=MAIN_HEALTH
        self.wave=5
    
    def draw(self,screen):
        panel=pygame.Surface((self.hud_width,self.hud_height))
        panel.set_alpha(200)#прозрачность
        panel.fill(BLACK)
        screen.blit(panel,self.panel_rect)

        pygame.draw.line(screen,GREEN,(64,self.hud_height/5),(((self.hud_width-84)*(self.health/MAIN_HEALTH)+64),self.hud_height/5),10)



        health_text=FONT_VERY_SMALL.render(f"HP: {self.health}",True,GREEN)
        screen.blit(health_text,(1,23))


