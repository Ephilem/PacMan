import pygame

from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity
from entity.MovingEntity import MovingEntity

class Pacman(MovingEntity):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.pacman_eating_img_frames], maze_pos, 50,  10)
        print(ResourcesProvider.get.pacman_eating_img_frames)
        game.on_key_press_registry.append(self)
    
    def on_key_press(self, event):
        self.move_direction("left")
        pass

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_movement_system()
        if not self.moving_direction is None:
            super().tick_animation()
