from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import pygame


class Pinky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.pinky_img_frames], maze_pos, case_size, game) 
    
    def tick_ai(self):        
        if self.mode == "chasing":
            if not self.is_moving:
                self.move_ai(self.shift_maze_pos_with_direction(self.game.maze.pacman.maze_pos, self.game.maze.pacman.moving_direction, 4))
        elif self.mode == "scattering":
            if not self.is_moving:
                self.move_ai(self.game.maze.ghosts_checkpoints["pinky_checkpoint"])
            if self.maze_pos == self.game.maze.ghosts_checkpoints["pinky_checkpoint"]:
                self.mode = "chasing"
