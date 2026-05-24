import pygame
import numpy
import pytmx
from settings import *
from Level.Dollar import *

class Dollar_green():
    def __init__(self,waypoints):

        self.health=ENEMY_HEALTH
        self.percent_health=(self.health/ENEMY_HEALTH)
        self.speed=ENEMY_SPEED
        self.damage=ENEMY_DAMAGE
        self.slow_effect = False
        self.slow_duration = 0

        self.waypoints=waypoints.copy()
        #Позиция
        self.y=self.waypoints[0][0]
        self.x=self.waypoints[0][1]

        #Состояние
        self.alive=True
        self.reached_base=False

        self.size=30

        self.target_index=1

        self.target_index_max=len(self.waypoints)

        self.color=(0,255,0)
        

        


    def update(self):
        #Дошли ли мы до базы
        if self.target_index>= self.target_index_max:
            self.alive=False
            self.reached_base=True
            return
        if self.slow_effect:
            self.slow_duration-=1
            if self.slow_duration<=0:
                self.slow_effect=False
        else:

            self.target_x=self.waypoints[self.target_index][1]
            self.target_y=self.waypoints[self.target_index][0]

            #Расстояние
            self.dx = self.target_x-self.x
            self.dy = self.target_y-self.y
            self.distance= (self.dx**2+self.dy**2)**0.5

            #Расчёт дистанции(если растояние маленькое телепортируемся)
            if self.distance <= self.speed:
                self.x = self.target_x
                self.y = self.target_y
                self.target_index+=1
            else:
                self.x+=(self.dx/self.distance)*self.speed
                self.y+=(self.dy/self.distance)*self.speed



    def take_damage(self,amount):
        self.health-=amount
        
        if self.health<=0:
            self.health=0
            self.alive=False
        
        self.percent_health=(self.health/ENEMY_HEALTH)


    def draw(self,screen):

        self.money_font=FONT_MEDIUM
        if not self.slow_effect:
            self.color=(255*(1-self.percent_health),255*self.percent_health,0)
        else:
            self.color=CYAN
        
        self.text_surface= self.money_font.render("$",True,self.color)
        self.text_rect=self.text_surface.get_rect(center=(self.x,self.y))
        screen.blit(self.text_surface,self.text_rect)

