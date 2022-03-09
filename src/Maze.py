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
        
        self.level_data = self.read_level_file(1)
        self.width_height_px =  len(self.level_data[0])*self.CASE_SIZE,len(self.level_data)*self.CASE_SIZE 
        
        # Pour optimiser, on fait en sorte de calculer de créer la map en entier pour évité de la refaire (donc + de performance)
        self.map_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]))
        self.ai_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]))

        self.map_layout = [[None]*len(self.level_data[0]) for x in range(len(self.level_data))]     
        
        self.pacman = None   
        self.entity_registry = []
        # Il faut séparer les élément de la map (mur, point de tp, etc..) et les entité (pacgom, point de spawn fantom et pacman)
        for y, lines in enumerate(self.level_data):
            for x, v in enumerate(lines): 
                if v in ["o","O","s","I","P","C","B"]:
                    if v == "o":                        
                        self.entity_registry.append(Pacgom((x, y), self.CASE_SIZE))
                    elif v == "O":
                        self.entity_registry.append(SuperPacgom((x, y), self.CASE_SIZE))
                    elif v == "s":
                        self.pacman = Pacman(self.game, (x, y), self.CASE_SIZE)
                    elif v == "P":
                        self.entity_registry.append(Pinky(self.game, (x, y), self.CASE_SIZE))
                    elif v == "I":
                        self.entity_registry.append(Inky(self.game, (x, y), self.CASE_SIZE))
                    elif v == "B":
                        self.entity_registry.append(Blinky(self.game, (x, y), self.CASE_SIZE))
                    elif v == "C":
                        self.entity_registry.append(Clyde(self.game, (x, y), self.CASE_SIZE))
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
                            
        self.ai_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]), flags=pygame.SRCALPHA) 
        self.calcul_ai_grid(self.pacman.maze_pos)


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
        for entity in self.entity_registry:
            entity.render(surface, (entity.maze_pos[0]*self.CASE_SIZE, entity.maze_pos[1]*self.CASE_SIZE))

        # rendue de pacman appart pour être sur qu'il soit au premier plan
        self.pacman.render(surface, (self.pacman.maze_pos[0]*self.CASE_SIZE, self.pacman.maze_pos[1]*self.CASE_SIZE))

        surface.blit(self.ai_to_render, (0,0))
    
    def get_map_element(self, maze_pos):
        return self.map_layout[maze_pos[1]][maze_pos[0]] 
    
    def get_ai_value(self, maze_pos):
        return self.ai_grid[maze_pos[1]][maze_pos[0]] 
    
    def calcul_ai_grid(self, maze_pos):
        self.ai_grid = [[999]*(len(self.level_data[0])+5) for x in range(len(self.level_data)+5)]  
        #self.ai_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]), flags=pygame.SRCALPHA)
        #self.ai_to_render.fill((0,0,0,0))
        i = 1
        to_treat = [[maze_pos],[]]
        for targets in to_treat:
            if len(targets) != 0:
                for p in targets:
                    if self.get_map_element((p[0]-1,p[1])) == "0" and self.get_ai_value((p[0]-1,p[1])) >= 999:
                        to_treat[i].append((p[0]-1,p[1]))
                        self.ai_grid[p[1]][p[0]-1] = i
                        #self.ai_to_render.blit(pygame.font.SysFont(None,18).render(str(i), True, (255,255,0)), ((p[0]-1)*self.CASE_SIZE+2, (p[1])*self.CASE_SIZE+2))
                    # droite
                    if self.get_map_element((p[0]+1,p[1])) == "0" and self.get_ai_value((p[0]+1,p[1])) >= 999:
                        to_treat[i].append((p[0]+1,p[1]))
                        self.ai_grid[p[1]][p[0]+1] = i
                        #self.ai_to_render.blit(pygame.font.SysFont(None,18).render(str(i), True, (255,255,0)), ((p[0]+1)*self.CASE_SIZE+2, (p[1])*self.CASE_SIZE+2))
                    # haut
                    if self.get_map_element((p[0],p[1]-1)) == "0" and self.get_ai_value((p[0],p[1]-1)) >= 999:
                        to_treat[i].append((p[0],p[1]-1))
                        self.ai_grid[p[1]-1][p[0]] = i
                        #self.ai_to_render.blit(pygame.font.SysFont(None,18).render(str(i), True, (255,255,0)), ((p[0])*self.CASE_SIZE+2, (p[1]-1)*self.CASE_SIZE+2))
                    # bas
                    if self.get_map_element((p[0],p[1]+1)) == "0" and self.get_ai_value((p[0],p[1]+1)) >= 999:
                        to_treat[i].append((p[0],p[1]+1))
                        self.ai_grid[p[1]+1][p[0]] = i
                        #self.ai_to_render.blit(pygame.font.SysFont(None,18).render(str(i), True, (255,255,0)), ((p[0])*self.CASE_SIZE+2, (p[1]+1)*self.CASE_SIZE+2))
                to_treat.append([])                    
                i += 1
        self.ai_grid[maze_pos[1]][maze_pos[0]] = 0    
        #self.ai_to_render.blit(pygame.font.SysFont(None,18).render(str(0), True, (255,255,0)), ((maze_pos[0])*self.CASE_SIZE+2, (maze_pos[1])*self.CASE_SIZE+2))


        

