import pygame
from abc import ABC, abstractmethod

class Entity(ABC):

    def __init__(self, textures: list, pos, ticks_between_frame=0):
        self.textures = textures
        self.pos = pos
        self.frame = textures[0]
        self.frame_id = 0
        self.tick = 0
        self.TICKS_BETWEEN_FRAME = ticks_between_frame

    def _tick_animation(self):
        if not self.TICKS_BETWEEN_FRAME == 0:
            self.tick += 1 
            if self.tick >= self.TICKS_BETWEEN_FRAME:
                self.tick = 0
                self.frame_id += 1
                if self.frame_id >= len(self.textures):
                    self.frame_id = 0
                self.frame = self.textures[0]