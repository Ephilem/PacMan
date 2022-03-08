import pygame
from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity

class Pacgom(Entity):

    def __init__(self, pos, case_size):
        super().__init__([pygame.transform.scale(ResourcesProvider.get.pacgom_img, (case_size, case_size))], pos)

    def render(self, surface, pos_to_render):
        surface.blit(self.frame , pos_to_render)