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

    # def is_blocked(self):
    #     return ((self.looking_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0") or
    #             (self.looking_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0") or
    #             (self.looking_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0") or
    #             (self.looking_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0"))

    # def can_move(self):
    #     return ((self.looking_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) == "0") or
    #             (self.looking_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) == "0") or
    #             (self.looking_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) == "0") or
    #             (self.looking_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) == "0"))
    
    # def get_available_pathway(self):
    #     final = ['up','down','left','right']
    #     final.remove(self.get_opposite_direction(self.looking_direction))
    #     for direction in final:
    #         if direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0":
    #             final.remove(direction)
    #         if direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0":
    #             final.remove(direction)
    #         if direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0":
    #             final.remove(direction)
    #         if direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0":
    #             final.remove(direction)
    #     return final
    
    # def get_opposite_direction(self, direction):
    #     a = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    #     return a[direction]