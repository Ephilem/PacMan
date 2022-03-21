from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import pygame


class Inky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.inky_img_frames], maze_pos, case_size, game) 
    
    def tick_ai(self):
        if self.mode == "chasing":
            p = self.shift_maze_pos_with_direction(self.game.maze.pacman.maze_pos, self.get_opposite_direction(self.game.maze.pacman.moving_direction), 4)
            if not self.is_moving:
                self.move_ai(self.shift_maze_pos_with_direction(self.game.maze.pacman.maze_pos, self.get_opposite_direction(self.game.maze.pacman.moving_direction), 4))
            pygame.draw.rect(self.game.window, (255,0,100), pygame.Rect(p[0]*self.case_size, p[1]*self.case_size, 12, 12))
        elif self.mode == "scattering":
            if not self.is_moving:
                self.move_ai(self.game.maze.ghosts_checkpoints["inky_checkpoint"])
            if self.maze_pos == self.game.maze.ghosts_checkpoints["inky_checkpoint"]:
                self.mode = "chasing"
        