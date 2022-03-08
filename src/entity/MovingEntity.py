
from entity.Entity import Entity


class MovingEntity(Entity):

    def __init__(self, textures, maze_pos, sleep_tick, case_size, game, ticks_between_frame=0):
        super().__init__(textures, maze_pos, ticks_between_frame)
        self.sleep_tick = sleep_tick
        self.DEFAULT_SLEEP_TICK = sleep_tick
        self.case_size = case_size
        self.game = game

        self.is_moving = False
        self.moving_to = None
        self.moving_direction = None
    
    def move(self, direction):
        if not self.is_moving and not direction is None:
            if direction == "left":
                self.moving_to = (self.maze_pos[0]-1,self.maze_pos[1])
            if direction == "right":
                self.moving_to = (self.maze_pos[0]+1,self.maze_pos[1])
            if direction == "up":
                self.moving_to = (self.maze_pos[0],self.maze_pos[1]-1)
            if direction == "down":
                self.moving_to = (self.maze_pos[0],self.maze_pos[1]+1)
            self.is_moving = True
            self.moving_direction = direction
    
    def tick_movement_system(self, entity_ticked):
        if self.is_moving:
            self.sleep_tick -= 1
            if self.sleep_tick == 0:
                self.sleep_tick = self.DEFAULT_SLEEP_TICK
                self.is_moving = False
                self.change_maze_pos(self.moving_to, entity_ticked)
                self.moving_to = None


    def get_pos_to_render(self, old_pos):
        if self.is_moving:
            new_pos = [i*self.case_size for i in self.moving_to]
            if self.moving_direction == "left":
                return (new_pos[0]+(old_pos[0]-new_pos[0])*(self.sleep_tick/self.DEFAULT_SLEEP_TICK), old_pos[1])
            if self.moving_direction == "right":
                return (new_pos[0]+(old_pos[0]-new_pos[0])*(self.sleep_tick/self.DEFAULT_SLEEP_TICK), old_pos[1])
            if self.moving_direction == "up":
                return (old_pos[0], new_pos[1]+(old_pos[1]-new_pos[1])*(self.sleep_tick/self.DEFAULT_SLEEP_TICK))
            if self.moving_direction == "down":
                return (old_pos[0], new_pos[1]+(old_pos[1]-new_pos[1])*(self.sleep_tick/self.DEFAULT_SLEEP_TICK))
        else:
            return old_pos
        
    
    def change_maze_pos(self, new_maze_pos, entity_to_move):
        self.game.maze.entity_registry[self.maze_pos[1]][self.maze_pos[0]] = None
        self.maze_pos = new_maze_pos
        self.game.maze.entity_registry[self.maze_pos[1]][self.maze_pos[0]] = entity_to_move
