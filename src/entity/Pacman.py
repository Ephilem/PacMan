import pygame

from ResourcesProvider import ResourcesProvider

class Pacman(Entity):

    def __init__(self, pos):
        super().__init__(ResourcesProvider.get.pacman_eating_img_frames, pos, 0)
        self.moving_to = "no" # possible : left, right, up, down, no
