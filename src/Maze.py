from asyncio import to_thread
from xml.dom.minidom import parseString
import pygame
from entity.Entity import Entity
from entity.GhostHouseDoor import GhostHouseDoor
from entity.Pacgom import Pacgom
from entity.Pacman import Pacman
from entity.SuperPacgom import SuperPacgom
from entity.ghosts.Pinky import Pinky
from entity.ghosts.Clyde import Clyde
from entity.ghosts.Inky import Inky
from entity.ghosts.Blinky import Blinky
from tile.WallTile import *



class Maze:

    def __init__(self, game, pos, level):
        self.game = game
        self.game.render_registry.append(self)

        self.CASE_SIZE = 25

        # permet de savoir combien de temps dure la game et de actionner des évènement comme un fantome sort de la maison
        self.tick = 0

        WallTile(self.CASE_SIZE)
        
        self.level_data = self.read_level_file(1)
        self.width_height_px =  len(self.level_data[0])*self.CASE_SIZE,len(self.level_data)*self.CASE_SIZE 
        
        # Pour optimiser, on fait en sorte de calculer de créer la map en entier pour évité de la refaire (donc + de performance)
        self.map_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]))
        self.ai_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]))

        self.map_layout = [[None]*len(self.level_data[0]) for x in range(len(self.level_data))]     
        
        self.pacman = None   
        self.ghost_house_door = None

        self.ghost_registry = {}
        self.ghosts_checkpoints = {}
        self.pacgoms = []
        self.super_pacgoms = []
        # Nous allons faire une surface pour faire le rendue des pacgom qu'on va changer a chaque fois qu'on en enlève pour gagner des FPS (mais on laisse les superpacgom pour l'animation)
        self.pacgoms_surface = pygame.Surface(self.width_height_px, flags=pygame.SRCALPHA)
        # Il faut séparer les élément de la map (mur, point de tp, etc..) et les entité (pacgom, point de spawn fantom et pacman)
        self.load_map()
        # on render une première fois les pacgoms
        self.remove_pacgom()
                            
        self.ai_to_render = pygame.Surface((self.width_height_px[0], self.width_height_px[1]), flags=pygame.SRCALPHA) 

    def remove_pacgom(self, pacgom: Pacgom=None):
        """
        permet d'enveler une pacgom. si aucune pacgom n'est préciser, faire juste le render
        """
        if not pacgom is None:
            self.game.maze.pacgoms.remove(pacgom)
        self.pacgoms_surface = pygame.Surface(self.width_height_px, flags=pygame.SRCALPHA)
        for pacgom in self.pacgoms+self.super_pacgoms:
                pacgom.render(self.pacgoms_surface, (pacgom.maze_pos[0]*self.CASE_SIZE, pacgom.maze_pos[1]*self.CASE_SIZE))

    def read_level_file(self, level):
        with open("levels/"+str(level)+".txt") as f:
            contents = f.read()
            lines = contents.split("\n") 
        return [ [y for y in x] for x in lines]

    def render(self, surface, forcing=False):   
        if self.game.game_stat == "playing" or forcing:
            self.tick_event_sys()

            surface.blit(self.map_to_render, (0,0))
            self.verify_win()

            # appliquer la surface des pacgoms sur l'écran
            surface.blit(self.pacgoms_surface, (0,0))

            # rendue des super_pacgom
            for super_pacgom in self.super_pacgoms:
                super_pacgom.render(surface, (super_pacgom.maze_pos[0]*self.CASE_SIZE, super_pacgom.maze_pos[1]*self.CASE_SIZE))

            # rendue de la porte
            self.ghost_house_door.render(surface)

            # rendue des entités
            for entity in self.ghost_registry.values():
                entity.render(surface, (entity.maze_pos[0]*self.CASE_SIZE, entity.maze_pos[1]*self.CASE_SIZE))

            # rendue de pacman appart pour être sur qu'il soit au premier plan
            self.pacman.render(surface, (self.pacman.maze_pos[0]*self.CASE_SIZE, self.pacman.maze_pos[1]*self.CASE_SIZE))
    
    def tick_event_sys(self):
        self.tick += 1
        if self.tick == self.game.game_options["pinky_get_out_at"]:
            self.ghost_registry['pinky'].getting_out_ghost_house()
        if self.tick == self.game.game_options["inky_get_out_at"]:
            self.ghost_registry['inky'].getting_out_ghost_house()
        if self.tick == self.game.game_options["clyde_get_out_at"]:
            self.ghost_registry['clyde'].getting_out_ghost_house()
    
    def get_map_element(self, maze_pos):
        return self.map_layout[maze_pos[1]][maze_pos[0]] 
    
    def get_ai_value(self, maze_pos, ai_grid=None):
        if ai_grid is None:
            ai_grid = self.ai_grid
        return ai_grid[maze_pos[1]][maze_pos[0]] 
    
    def load_map(self):
        # Il faut séparer les élément de la map (mur, point de tp, etc..) et les entité (pacgom, point de spawn fantom et pacman)
        # On va stocker les position pour la ghost house door
        ghd_maze_pos_1 = (0,0)
        ghd_maze_pos_2 = (0,0)
        for y, lines in enumerate(self.level_data):
            for x, v in enumerate(lines): 
                if v in ["o","O","s","I","P","C","B","/","+","-","*","g","h"]:
                    self.map_layout[y][x] = '0'
                    if v == "o":                        
                        self.pacgoms.append(Pacgom((x, y), self.CASE_SIZE))
                    elif v == "O":
                        self.super_pacgoms.append(SuperPacgom((x, y), self.CASE_SIZE))
                    elif v == "s":
                        self.pacman = Pacman(self.game, (x, y), self.CASE_SIZE)
                    elif v == "P":
                        self.ghost_registry['pinky'] = Pinky(self.game, (x, y), self.CASE_SIZE)
                    elif v == "I":
                        self.ghost_registry['inky'] = Inky(self.game, (x, y), self.CASE_SIZE)
                    elif v == "B":
                        self.ghost_registry['blinky'] = Blinky(self.game, (x, y), self.CASE_SIZE)
                    elif v == "C":
                        self.ghost_registry['clyde'] = Clyde(self.game, (x, y), self.CASE_SIZE)
                    elif v == "/":
                        self.ghosts_checkpoints['pinky_checkpoint'] =  (x, y)
                    elif v == "+":
                        self.ghosts_checkpoints['inky_checkpoint'] = (x, y)
                    elif v == "-":
                        self.ghosts_checkpoints['blinky_checkpoint'] = (x, y)
                    elif v == "*":
                        self.ghosts_checkpoints['clyde_checkpoint'] = (x, y)
                    elif v == "g":
                        ghd_maze_pos_1 = (x, y)
                        self.map_layout[y][x] = 'g'
                    elif v == "h":
                        ghd_maze_pos_2 = (x, y)
                        self.map_layout[y][x] = 'h'
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
        # Création de la porte
        self.ghost_house_door = GhostHouseDoor(self.game, self.CASE_SIZE, ghd_maze_pos_1, ghd_maze_pos_2)
    
    def verify_win(self):
        if len(self.pacgoms) == 0 and len(self.super_pacgoms) == 0 and self.game.game_stat == "playing":
            self.game.game_stat = "winning"

    def set_ghosts_fear_mode(self):
        for ghost in self.ghost_registry.values():
            ghost.fear()

