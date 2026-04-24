import pygame
from settings import *


class Level:
    def __init__(self):
        self.grid_size={
            "col":20,
            "row":15
        }
        self.cell_size=64
        self.grid=[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
        ]
        self.path_color=YELLOW
        self.ground_colour=GREEN

    def draw(self,screen):
        for row in range(self.grid_size['row']):
            for col in range(self.grid_size['col']):
                x= col*self.cell_size
                y=row*self.cell_size

                if self.grid[row][col]==1:
                    color=self.path_color
                else:
                    color=self.ground_colour

                cell_rect=pygame.Rect(x,y,self.cell_size,self.cell_size)
                pygame.draw.rect(screen,color,cell_rect)

                pygame.draw.rect(screen,DARK_GRAY,cell_rect,width=1)


