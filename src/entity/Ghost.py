import pygame
from abc import abstractmethod
from ResourcesProvider import ResourcesProvider
from entity.MovingEntity import MovingEntity

class Ghost(MovingEntity):

    def __init__(self, ghost_type, maze_pos, case_size, game):
        if ghost_type == "blinky":
            images = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.blinky_img_frames]
        elif ghost_type == "clyde":
            images = None
        elif ghost_type == "inky":
            images = None
        elif ghost_type == "pinky":
            images = None
        super().__init__(images, maze_pos, 100, case_size, game, ticks_between_frame=30)
        self.mode = "chasing" # les modes : chasing, running_away, eated

    @abstractmethod
    def tick_ai(self):
        pass

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_animation()
    
    

    

    
