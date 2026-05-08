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

        self.waypoints=waypoints
        #Позиция
        self.y=waypoints[0][0]
        self.x=waypoints[0][1]

        #Состояние
        self.alive=True
        self.reached_base=False

        self.size=30

        self.target_index=1

        self.target_index_max=len(waypoints)


    def update(self):
        if self.target_index>= self.target_index_max:
            self.alive=False
            self.reached_base=True
            return

        target_x=self.waypoints[self.target_index][1]
        target_y=self.waypoints[self.target_index][0]
        #Расстояние
        dx = target_x-self.x
        dy = target_y-self.y
        distance= (dx**2+dy**2)**0.5

        if distance <= self.speed:
            self.x = target_x
            self.y = target_y
        else:
            self.x=(dx/distance)*self.speed
            self.y=(dy/distance)*self.speed


