from asyncore import read
import pygame
from tile.WallTile import *


class Maze:
    """
        Créer la grille de morpion de 600x600 pixels à partir d'une position
    """

    def __init__(self, game, pos, level):
        game.render_registry.append(self)
        game.on_click_registry.append(self)

        self.CASE_SIZE = 15
        
        WallTile(self.CASE_SIZE)
        
        self.level_layout = self.read_level_file(1) 
        self.width_height_px =  len(self.level_layout[0])*self.CASE_SIZE,len(self.level_layout)*self.CASE_SIZE 


    def read_level_file(self, level):
        with open("levels/"+str(level)+".txt") as f:
            contents = f.read()
            lines = contents.split("\n") 
        return [ [y for y in x] for x in lines]


    def on_click(self, event):
        pass

    def render(self, surface):   
        for y, lines in enumerate(self.level_layout):
            for x, v in enumerate(lines): 
                orientation = None
                if v == "a":
                    orientation = "n_s"
                if v == "b":
                    orientation = "e_w"
                if v == "c":
                    orientation = "n_e"
                if v == "d":
                    orientation = "n_w"
                if v == "e":
                    orientation = "s_e"
                if v == "f":
                    orientation = "s_w"
                
                if not orientation is None:
                    surface.blit(WallTile.get_tile(orientation), (x*self.CASE_SIZE, y*self.CASE_SIZE))
                
                # pygame.draw.rect(surface, (0,255,0), pygame.Rect(
                #     x*self.CASE_SIZE, 
                #     y*self.CASE_SIZE, 
                #     self.CASE_SIZE, 
                #     self.CASE_SIZE
                # ),1)
                    
        pass