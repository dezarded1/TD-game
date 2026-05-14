import pygame
import numpy
import pytmx
from settings import *
from Level.Dollar import *

class Dollar_green():
    def __init__(self,waypoints):

        self.health=ENEMY_HEALTH
        self.speed=ENEMY_SPEED
        self.damage=ENEMY_DAMAGE

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


    def update(self):
        #Дошли ли мы до базы
        if self.target_index>= self.target_index_max:
            self.alive=False
            self.reached_base=True
            return


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


    def draw(self,screen):

        self.money_font=FONT_MEDIUM
        self.text_surface= self.money_font.render("$",True,BLACK)
        self.text_rect=self.text_surface.get_rect(center=(self.x,self.y))
        screen.blit(self.text_surface,self.text_rect)

