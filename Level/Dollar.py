import pygame
from settings import *


class Level:
    def __init__(self):
        self.grid_size={
            "x": 20,
            "y": 15
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
        self.waypoints=[]
        self.start_position={
            "x":18,
            "y":14
        }
        self.waypoints = []
        self.end_position = {
            "x": 0,
            "y": 3
        }
        self.position=self.start_position.copy()
        self.visited={
            "x": None,
            "y": None
        }

        # self.waypoints=self.calculate_path()




        self.path_color=YELLOW
        self.ground_colour=GREEN


    def is_within_bounds(self,y,x):
        return 0 <= y < self.grid_size['y'] and 0 <= x < self.grid_size['x'] and x != self.visited['x'] and y != self.visited['y']


    # def calculate_path(self):
        # waypoints=[(self.start_position['y'],self.start_position['x'])]
        #
        # while self.position!=self.end_position:
        #     if self.is_within_bounds(self.position['y']+1,self.position['x'])  and self.grid[self.position['y']+1][self.position['x']]==1:
        #         self.visited=self.position.copy()
        #         self.position['y']+=1
        #
        #     elif self.is_within_bounds(self.position['y'],self.position['x']-1)  and self.grid[self.position['y']][self.position['x']-1]==1:
        #         self.visited = self.position.copy()
        #         self.position['x']-=1
        #     elif self.is_within_bounds(self.position['y']-1,self.position['x'])  and self.grid[self.position['y']-1][self.position['x']]==1:
        #         self.visited = self.position.copy()
        #         self.position['y']-=1
        #
        #
        #     waypoints.append((self.position['y'], self.position['x']))
        #     print(waypoints)
        #
        # return waypoints




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


