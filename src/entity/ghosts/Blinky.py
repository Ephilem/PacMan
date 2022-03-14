from entity.Ghost import Ghost


class Blinky(Ghost):

    def __init__(self, game, maze_pos, case_size):
        super().__init__("blinky", maze_pos, case_size, game) 
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
           

            


        pass
    
    def get_ai_value(self, ai_grid, maze_pos):
        return ai_grid[maze_pos[1]][maze_pos[0]]