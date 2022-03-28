from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import pygame


class Blinky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.blinky_img_frames], maze_pos, case_size, game, "blinky", not_spawning_in_the_ghost_house=True) 
            
    def chasing_ai(self):
        if not self.is_moving:
            self.move_ai(self.game.maze.pacman.maze_pos)