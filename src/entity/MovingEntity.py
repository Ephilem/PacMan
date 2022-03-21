
from entity.Entity import Entity


class MovingEntity(Entity):

    def __init__(self, textures, maze_pos, sleep_tick, case_size, game, ticks_between_frame=0):
        super().__init__(textures, maze_pos, ticks_between_frame)
        self.sleep_tick = sleep_tick
        self.max_sleep_tick = sleep_tick
        self.case_size = case_size
        self.game = game

        self.is_moving = False
        self.moving_to = None
        self.moving_direction = None

        # sert pour l'ia des phatomes
        self.last_pos = None
    
    def move(self, direction):
        """
        permet de commencer un mouvement vers une case
        """
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
        """
        permet l'animation du mouvement. IL fait donc office aussi de vitesse de déplacement
        """
        if self.is_moving:
            self.sleep_tick -= 1
            if self.sleep_tick <= 0:
                self.sleep_tick = self.max_sleep_tick
                self.is_moving = False
                # On utilise maze_pos car il n'a pas officielement bouger, il est toujours dans l'ancienne case, mais pas visuellement
                self.last_pos = self.maze_pos
                self.change_maze_pos(self.moving_to, entity_ticked)
                self.moving_to = None


    def get_pos_to_render(self, old_pos):
        """
        permet d'obtenir la position à faire en rendue en prenant en compte l'animation de mouvement
        """
        if self.is_moving:
            new_pos = [i*self.case_size for i in self.moving_to]
            if self.moving_direction == "left":
                return (new_pos[0]+(old_pos[0]-new_pos[0])*(self.sleep_tick/self.max_sleep_tick), old_pos[1])
            if self.moving_direction == "right":
                return (new_pos[0]+(old_pos[0]-new_pos[0])*(self.sleep_tick/self.max_sleep_tick), old_pos[1])
            if self.moving_direction == "up":
                return (old_pos[0], new_pos[1]+(old_pos[1]-new_pos[1])*(self.sleep_tick/self.max_sleep_tick))
            if self.moving_direction == "down":
                return (old_pos[0], new_pos[1]+(old_pos[1]-new_pos[1])*(self.sleep_tick/self.max_sleep_tick))
        else:
            return old_pos
        
    def change_maze_pos(self, new_maze_pos, entity_to_move):
        self.maze_pos = new_maze_pos

    def change_max_sleep_tick(self, new_sleep_tick):
        self.max_sleep_tick = new_sleep_tick
        if self.max_sleep_tick < self.sleep_tick:
            self.sleep_tick = self.max_sleep_tick
