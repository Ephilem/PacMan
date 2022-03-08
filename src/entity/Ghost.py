import pygame
from abc import abstractmethod
from entity.MovingEntity import MovingEntity

class Ghost(MovingEntity):

    def __init__(self, ghost_type, maze_pos, case_size, game):
        if ghost_type == "blinky":
            images = None
        elif ghost_type == "clyde":
            images = None
        elif ghost_type == "inky":
            images = None
        elif ghost_type == "pinky":
            images = None
        super().__init__(images, maze_pos, 20, case_size, game, ticks_between_frame=30)
        self.mode = "chasing" # les modes : chasing, running_away, eated

    @abstractmethod
    def tick_ai(self):
        pass

    def render(self, surface):
        surface.blit(self.frame, self.pos)
    
    

    

    
