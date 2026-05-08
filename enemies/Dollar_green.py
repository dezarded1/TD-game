import pygame
import numpy
import pytmx
from settings import *
from Level.Dollar import *

class Dollar_green:
    def __init__(self,waypoints):
        self.level=Level()

        self.health=ENEMY_HEALTH
        self.speed=ENEMY_SPEED
        self.damage=ENEMY_DAMAGE



        self.y=0
        self.x=0

        print()