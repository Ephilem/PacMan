import pygame
from abc import abstractmethod
from entity.Entity import Entity

class Ghost(Entity):

    def __init__(self, ghost_type, maze_pos, case_size):
        if ghost_type == "blinky":
            images = None
        elif ghost_type == "clyde":
            images = None
        elif ghost_type == "inky":
            images = None
        elif ghost_type == "pinky":
            images = None
        super().__init__(images, maze_pos, ticks_between_frame=30)
        self.mode = "chasing" # les modes : chasing, running_away, eated

    @abstractmethod
    def tick_ai(self):
        pass

    def render(self, surface):
        surface.blit(self.frame, self.pos)
    
    

    

    
