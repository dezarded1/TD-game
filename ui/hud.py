# #lib
import pygame
import numpy
import pytmx
from settings import *

class HUD:
    def __init__(self):
        self.money=0
        self.health=0
        self.time_sec=0
        self.time_m=0


        self.hud_width=450
        self.hud_height=128

        self.panel_rect=pygame.Rect(0,0,self.hud_width,self.hud_height)

    def update_health(self,health):
        self.health=health
    
    def update_money(self,money):
        self.money=money

    def update_time(self,time):
        self.time_m=time//60
        self.time_sec=time%60
        

    
    def draw(self,screen):
        panel=pygame.Surface((self.hud_width,self.hud_height))
        panel.set_alpha(200)#прозрачность
        panel.fill(BLACK)
        screen.blit(panel,self.panel_rect)

        pygame.draw.line(screen,GREEN,(64,self.hud_height/5),(((self.hud_width-84)*(self.health/MAIN_HEALTH)+64),self.hud_height/5),10)



        self.health_text=FONT_VERY_SMALL.render(f"HP: {self.health}",True,GREEN)
        screen.blit(self.health_text,(1,self.hud_height/5-7))

        self.money_text = FONT_VERY_SMALL.render(f"COINS: {self.money}", True, YELLOW)
        screen.blit(self.money_text, (1, self.hud_height/3))

        self.time_text = FONT_VERY_SMALL.render(f"TIME: {self.time_m}:{self.time_sec}", True, WHITE)
        screen.blit(self.time_text, (1, self.hud_height/2))





