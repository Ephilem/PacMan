from asyncio import to_thread
import pygame
from entity.Entity import Entity
from entity.Pacgom import Pacgom
from entity.Pacman import Pacman
from entity.SuperPacgom import SuperPacgom
from entity.ghosts.Pinky import Pinky
from entity.ghosts.Clyde import Clyde
from entity.ghosts.Inky import Inky
from entity.ghosts.Blinky import Blinky
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
        
        self.pacman = None
        # Pour optimiser, on fait en sorte de calculer de créer la map en entier pour évité de la refaire (donc + de performance)
        self.map_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]))
        self.ai_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]))

        self.map_layout = [[None]*len(level_data[0]) for x in range(len(level_data))]        
        self.entity_layout = [[None]*len(level_data[0]) for x in range(len(level_data))]
        self.ghost_layout = [[None]*len(level_data[0]) for x in range(len(level_data))]
        # Il faut séparer les élément de la map (mur, point de tp, etc..) et les entité (pacgom, point de spawn fantom et pacman)
        for y, lines in enumerate(level_data):
            for x, v in enumerate(lines): 
                if v in ["o","O","s"]:
                    if v == "o":                        
                        self.entity_layout[y][x] = Pacgom((x, y), self.CASE_SIZE)
                    elif v == "O":
                        self.entity_layout[y][x] = SuperPacgom((x, y), self.CASE_SIZE)
                    elif v == "s":
                        self.pacman = Pacman(self.game, (x, y), self.CASE_SIZE)
                        self.entity_layout[y][x] = self.pacman
                    # elif v == "P":
                    #     self.ghost_layout[y][x] = Pinky(self.game, (x, y), self.CASE_SIZE)
                    # elif v == "I":
                    #     self.ghost_layout[y][x] = Inky(self.game, (x, y), self.CASE_SIZE)
                    # elif v == "B":
                    #     self.ghost_layout[y][x] = Blinky(self.game, (x, y), self.CASE_SIZE)
                    # elif v == "C":
                    #     self.ghost_layout[y][x] = Clyde(self.game, (x, y), self.CASE_SIZE)
                    self.map_layout[y][x] = '0'
                else:
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
                        self.map_to_render.blit(WallTile.get_tile(orientation), (x*self.CASE_SIZE, y*self.CASE_SIZE))
                    self.map_layout[y][x] = v
                         
        self.EMPTY_AI_GRID = [[999]*len(level_data[0]) for x in range(len(level_data))]       
        self.calcul_ai_grid()


    def read_level_file(self, level):
        with open("levels/"+str(level)+".txt") as f:
            contents = f.read()
            lines = contents.split("\n") 
        return [ [y for y in x] for x in lines]

    def on_click(self, event):
        pass

    def render(self, surface):   
        surface.blit(self.map_to_render, (0,0))
        
        # rendue des entités
        for y, lines in enumerate(self.entity_layout):
            for x, v in enumerate(lines): 
                if not v is None:
                    v.render(surface, (x*self.CASE_SIZE, y*self.CASE_SIZE))
        
        # DEBUG affichage des valeur ia pour chaque case
        for y, lines in enumerate(self.ai_grid):
            for x, v in enumerate(lines): 
                if v < 999:                    
                    surface.blit(pygame.font.SysFont(None,15).render(str(v), True, (255,255,255)), (x*self.CASE_SIZE+10, y*self.CASE_SIZE+10))
                
        

                    
        pass
    
    def get_map_element(self, maze_pos):
        return self.map_layout[maze_pos[1]][maze_pos[0]] 
    
    def get_ai_value(self, maze_pos):
        return self.ai_grid[maze_pos[1]][maze_pos[0]] 
    
    def calcul_ai_grid(self):
        self.ai_grid = self.EMPTY_AI_GRID
        maze_pos = self.pacman.maze_pos
        self.ai_grid[maze_pos[0]][maze_pos[1]] = 0
        i = 1
        to_treat = [maze_pos]
        for p in to_treat:
            # gauche
            if self.get_map_element((p[0]-1,p[1])) == "0" and self.get_ai_value((p[0]-1,p[1])) >= 999:
                to_treat.append((p[0]-1,p[1]))
                self.ai_grid[p[1]][p[0]-1] = i
            if self.get_map_element((p[0]-1,p[1])) == "0" and self.get_ai_value((p[0]-1,p[1])) >= 999:
                to_treat.append((p[0]-1,p[1]))
                self.ai_grid[p[1]][p[0]-1] = i
            if self.get_map_element((p[0]-1,p[1])) == "0" and self.get_ai_value((p[0]-1,p[1])) >= 999:
                to_treat.append((p[0]-1,p[1]))
                self.ai_grid[p[1]][p[0]-1] = i
            if self.get_map_element((p[0]-1,p[1])) == "0" and self.get_ai_value((p[0]-1,p[1])) >= 999:
                to_treat.append((p[0]-1,p[1]))
                self.ai_grid[p[1]][p[0]-1] = i
            del to_treat[to_treat.index(p)]
            i += 1


        

