import pygame
from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity

class Pacgom(Entity):

    def __init__(self, pos, case_size):
        super().__init__([ResourcesProvider.get.pacgom_img], pos)
        self.case_size = case_size

    def render(self, surface):
        surface.blit(pygame.transform.scale(self.frame, (self.case_size, self.case_size)) , self.pos)