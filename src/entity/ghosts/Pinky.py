from ResourcesProvider import ResourcesProvider
from entity.Ghost import Ghost
import pygame


class Pinky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.pinky_img_frames], maze_pos, case_size, game) 
    
    def tick_ai(self):        
        if self.mode == "chasing":
            p = self.shift_maze_pos_with_direction(self.game.maze.pacman.maze_pos, self.game.maze.pacman.moving_direction, 4)
            if not self.is_moving:
                self.move_ai(self.shift_maze_pos_with_direction(self.game.maze.pacman.maze_pos, self.game.maze.pacman.moving_direction, 4))
            pygame.draw.rect(self.game.window, (255,0,255), pygame.Rect(p[0]*self.case_size, p[1]*self.case_size, 12, 12))
        elif self.mode == "scattering":
            if not self.is_moving:
                self.move_ai(self.game.maze.ghosts_checkpoints["pinky_checkpoint"])
            if self.maze_pos == self.game.maze.ghosts_checkpoints["pinky_checkpoint"]:
                self.mode = "chasing"
    
    # def shift_maze_pos_with_direction(self, direction, shift, base_maze_pos):
    #     """
    #     Cette fonction permettera d'obtenir le maze_pos par rapport qui est devant pacman
    #     """
    #     if shift == 0:
    #         return base_maze_pos
    #     final = (0,0)
    #     if direction == "left":
    #         final[0] = base_maze_pos[0] - shift
    #         # Si on sort des limites du maze, on fait en sorte de réduire le shift
    #         if not (0 <= final[0] and final[0] < len(self.game.maze.map_layout[0][0])):
    #             return self.shift_maze_pos_with_direction(direction, shift-1, base_maze_pos)                
    #     if direction == "right":
    #         final[0] = base_maze_pos[0] + shift
    #         if not (0 <= final[0] and final[0] < len(self.game.maze.map_layout[0][0])):
    #             return self.shift_maze_pos_with_direction(direction, shift-1, base_maze_pos)          
    #     if direction == "up":
    #         final[1] = base_maze_pos[1] - shift
    #         if not (0 <= final[1] and final[1] < len(self.game.maze.map_layout[0])):
    #             return self.shift_maze_pos_with_direction(direction, shift-1, base_maze_pos)    
    #     if direction == "down":
    #         final[1] = base_maze_pos[1] + shift
    #         if not (0 <= final[1] and final[1] < len(self.game.maze.map_layout[0])):
    #             return self.shift_maze_pos_with_direction(direction, shift-1, base_maze_pos)
    #     return final
