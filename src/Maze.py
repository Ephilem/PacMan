from asyncore import read
import pygame
from entity.Entity import Entity
from entity.Pacgom import Pacgom
from entity.Pacman import Pacman
from entity.SuperPacgom import SuperPacgom
from tile.WallTile import *


class Maze:
    """
        Créer la grille de morpion de 600x600 pixels à partir d'une position
    """

    def __init__(self, game, pos, level):
        self.game = game
        self.game.render_registry.append(self)
        self.game.on_click_registry.append(self)

        self.CASE_SIZE = 25
        
        WallTile(self.CASE_SIZE)
        
        level_data = self.read_level_file(1)
        self.width_height_px =  len(level_data[0])*self.CASE_SIZE,len(level_data)*self.CASE_SIZE 

        self.map_layout = [[None]*len(level_data[0]) for x in range(len(level_data))]        
        self.entity_registry = [[None]*len(level_data[0]) for x in range(len(level_data))]
        # Il faut séparer les élément de la map (mur, point de tp, etc..) et les entité (pacgom, point de spawn fantom et pacman)
        for y, lines in enumerate(level_data):
            for x, v in enumerate(lines): 
                if v in ["o","O","s"]:
                    if v == "o":                        
                        self.entity_registry[y][x] = Pacgom((x, y), self.CASE_SIZE)
                    elif v == "O":
                        self.entity_registry[y][x] = SuperPacgom((x, y), self.CASE_SIZE)
                    elif v == "s":
                        self.entity_registry[y][x] = Pacman(self.game, (x, y), self.CASE_SIZE)
                        self.map_layout[y][x] = "0"

                    self.map_layout[y][x] = '0'
                else:
                    self.map_layout[y][x] = v
                    



    def read_level_file(self, level):
        with open("levels/"+str(level)+".txt") as f:
            contents = f.read()
            lines = contents.split("\n") 
        return [ [y for y in x] for x in lines]

    def on_click(self, event):
        pass

    def render(self, surface):   
        for y, lines in enumerate(self.map_layout):
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
        
        # rendue des entités
        for y, lines in enumerate(self.entity_registry):
            for x, v in enumerate(lines): 
                if not v is None:
                    v.render(surface, (x*self.CASE_SIZE, y*self.CASE_SIZE))
                    
        pass
    
    def get_map_element(self, maze_pos):
        return self.map_layout[maze_pos[1]][maze_pos[0]] 