import pygame
from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity

class SuperPacgom(Entity):

    def __init__(self, pos, case_size):
        super().__init__(
            [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.super_pacgom_img_frames], 
            pos, 10)
        self.case_size = case_size

    def render(self, surface, pos_to_render):
        surface.blit(self.frame , pos_to_render)
        super().tick_animation()