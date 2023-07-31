from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import pygame


class Blinky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.blinky_img_frames], maze_pos, case_size, game) 
        self.ai_grid_values_to_checkpoint = None
    
    def tick_ai(self):
        if self.mode == "chasing":
            if not self.is_moving:
                self.move_with_ai_grid(self.game.maze.ai_grid)
        elif self.mode == "scattering" :
            if self.ai_grid_values_to_checkpoint is None:
                self.ai_grid_values_to_checkpoint =  self.game.maze.create_ai_grid_values_to(self.game.maze.ghosts_checkpoints["blinky_checkpoint"])
            if not self.is_moving:
                self.move_with_ai_grid(self.ai_grid_values_to_checkpoint)
            if self.maze_pos == self.game.maze.ghosts_checkpoints["blinky_checkpoint"]:
                self.mode = "chasing"

    def eated_ai(self):
        self.move_with_ai_grid(self.game.maze.blinky_spawn_ai_grid)
        if self.maze_pos == self.game.maze.ghosts_spawn["blinky_spawn"]:
            self.mode = "chasing"
            self.is_eated = False
            self.change_max_sleep_tick(15)
            self.change_texture(self.GHOST_TEXTURE, True)
            self.rotate(self.looking_direction)
    
    def get_ai_value(self, ai_grid, maze_pos):
        return ai_grid[maze_pos[1]][maze_pos[0]]