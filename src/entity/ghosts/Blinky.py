from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import pygame


class Blinky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.blinky_img_frames], maze_pos, case_size, game) 
            
    def tick_ai(self):
        if self.mode == "chasing":
            if not self.is_moving:
                self.move_ai(self.game.maze.pacman.maze_pos)
        elif self.mode == "scattering" :
            if not self.is_moving:
                self.move_ai(self.game.maze.ghosts_checkpoints["blinky_checkpoint"])
            if self.maze_pos == self.game.maze.ghosts_checkpoints["blinky_checkpoint"]:
                self.mode = "chasing"
           

            


        pass
    
    def get_ai_value(self, ai_grid, maze_pos):
        return ai_grid[maze_pos[1]][maze_pos[0]]