from entity.Ghost import Ghost
import random


class Clyde(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__("clyde", maze_pos, case_size, game) 
        self.looking_direction = "up"
    
    def tick_ai(self):
        avalaible_way = self.get_available_pathway()
        if len(avalaible_way) >= 3 or self.is_blocked():
            self.looking_direction = random.choice(avalaible_way)
        
        
        if not self.is_moving and self.can_move():
             self.move(self.looking_direction)
             self.rotate(self.looking_direction)

    def is_blocked(self):
        return ((self.looking_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0") or
                (self.looking_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0") or
                (self.looking_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0") or
                (self.looking_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0"))

    def can_move(self):
        return ((self.looking_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) == "0") or
                (self.looking_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) == "0") or
                (self.looking_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) == "0") or
                (self.looking_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) == "0"))
    
    def get_available_pathway(self):
        final = ['up','down','left','right']
        final.remove(self.get_opposite_direction(self.looking_direction))
        for direction in final:
            if direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0":
                final.remove(direction)
            if direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0":
                final.remove(direction)
            if direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0":
                final.remove(direction)
            if direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0":
                final.remove(direction)
        return final
    
    def get_opposite_direction(self, direction):
        a = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        return a[direction]