from tkinter import LEFT
import pygame

from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity
from entity.MovingEntity import MovingEntity

class Pacman(MovingEntity):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.pacman_eating_img_frames], maze_pos, 15, case_size, game, 5)
        self.direction_to_go = None
        self.__last_rotation = 0

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        if not self.direction_to_go is None:
            super().tick_animation()
        
        self.tick_movement_system(self)
        if self.is_moving and self.sleep_tick <= 1:
            self.game.maze.calcul_ai_grid(self.moving_to) 

        # IA (car render fait aussi office de ticking) #
        # MOUVEMENT : les touches
        if pygame.key.get_pressed()[pygame.K_LEFT] and self.game.maze.get_map_element((self.maze_pos[0]-1, self.maze_pos[1])) == "0":
            self.direction_to_go = "left"  
        elif pygame.key.get_pressed()[pygame.K_RIGHT] and self.game.maze.get_map_element((self.maze_pos[0]+1, self.maze_pos[1])) == "0":
            self.direction_to_go = "right"  
        elif pygame.key.get_pressed()[pygame.K_UP] and self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]-1)) == "0":
            self.direction_to_go = "up"          
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]+1)) == "0":
            self.direction_to_go = "down"  
        else:
            self.direction_to_go = self.moving_direction

        # MOUVEMENT : core
        if not self.is_moving:
            v = None
            if self.direction_to_go == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1, self.maze_pos[1])) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0]-1, self.maze_pos[1]))
            if self.direction_to_go == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1, self.maze_pos[1])) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0]+1, self.maze_pos[1]))
            if self.direction_to_go == "up" and self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]-1)) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]-1))
            if self.direction_to_go == "down" and self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]+1)) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]+1))
            if v == "0":
                self.move(self.direction_to_go)
                self.__rotate(self.direction_to_go)
            else:
                self.direction_to_go = None
        

    def __rotate(self, direction):
        rotate = lambda x : self.change_texture([pygame.transform.rotate(f, x) for f in self.textures])
        if direction == "left":
            rotate(180-self.__last_rotation)
            self.__last_rotation = 180
        if direction == "right":
            rotate(0-self.__last_rotation)
            self.__last_rotation = 0
        if direction == "up":
            rotate(90-self.__last_rotation)
            self.__last_rotation = 90
        if direction == "down":
            rotate(270-self.__last_rotation)
            self.__last_rotation = 270
