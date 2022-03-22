from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import random, pygame


class Clyde(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.clyde_img_frames], maze_pos, case_size, game) 
    
    def tick_ai(self):        
        if self.mode == "chasing":     
            if not self.is_moving:
                self.move_ai_rand()
        elif self.mode == "scattering" :
            if not self.is_moving:
                self.move_ai(self.game.maze.ghosts_checkpoints["clyde_checkpoint"])
            if self.maze_pos == self.game.maze.ghosts_checkpoints["clyde_checkpoint"]:
                self.mode = "chasing"