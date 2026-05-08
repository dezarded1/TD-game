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

