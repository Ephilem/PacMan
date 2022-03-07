import pygame
from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity

class SuperPacgom(Entity):

    def __init__(self, pos, case_size):
        super().__init__(
            [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.super_pacgom_img_frames], 
            pos, 25)
        self.case_size = case_size

    def render(self, surface):
        surface.blit(pygame.transform.scale(self.frame, (self.case_size, self.case_size)) , self.pos)
        super().tick_animation()