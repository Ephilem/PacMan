import pygame
from abc import abstractmethod
from entity.Entity import Entity

class Ghost(Entity):

    def __init__(self, ghost_type, pos, case_size):
        if ghost_type == "blinky":
            images = None
        super().__init__(images, pos, ticks_between_frame=30)
        self.mode = "chasing" # les modes : chasing, running_away, eated

    @abstractmethod
    def tick_ai(self):
        pass

    def render(self, surface):
        surface.blit(self.frame, self.pos)
