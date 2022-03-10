from entity.Ghost import Ghost


class Inky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__("inky", maze_pos, case_size, game) 
    
    def tick_ai(self):
        ai_value = self.game.maze.get_ai_value(self.maze_pos)
        to_go = ai_value-1
        self.game.maze.pacman.direction_to_go 
        if not self.is_moving:
            if self.game.maze.get_ai_value((self.maze_pos[0]-1,self.maze_pos[1])) == to_go:
                self.move("left")
                self.rotate("left")
            if self.game.maze.get_ai_value((self.maze_pos[0]+1,self.maze_pos[1])) == to_go:
                self.move("right")
                self.rotate("right")
            if self.game.maze.get_ai_value((self.maze_pos[0],self.maze_pos[1]-1)) == to_go:
                self.move("up")
                self.rotate("up")
            if self.game.maze.get_ai_value((self.maze_pos[0],self.maze_pos[1]+1)) == to_go:
                self.move("down")
                self.rotate("down")
        pass
        