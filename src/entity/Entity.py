import pygame
from abc import abstractmethod

class Entity:
 
    def __init__(self, textures, maze_pos, ticks_between_frame=0):
        self.textures = textures
        self.maze_pos = maze_pos
        self.frame = textures[0]
        self.frame_id = 0
        self.tick = 0
        self.TICKS_BETWEEN_FRAME = ticks_between_frame
        self.__frame_min = 0
        self.__frame_max = len(textures)-1

    def tick_animation(self):
        if not self.TICKS_BETWEEN_FRAME == 0:
            self.tick += 1 
            if self.tick >= self.TICKS_BETWEEN_FRAME:
                self.tick = 0
                self.frame_id += 1
                if self.frame_id >= self.__frame_max:
                    self.frame_id = self.__frame_min
                self.frame = self.textures[self.frame_id]
    
    @abstractmethod
    def render(self, surface, pos_to_render):
        pass

    def change_texture(self, textures):
        self.textures = textures
        self.frame = textures[0]
        self.frame_id = 0
        self.tick = 0
    
    def set_frame_min_max(self, min=None, max=None):
        if min is None:
            min = self.__frame_min
        if max is None:
            max = self.__frame_max
        if min >= max:
            raise "Error! cannot set a min superior or equal to the max"
        if not len(self.textures)-1 < max:
            self.__frame_max = len(self.textures)-1
        if not min < 0:
            self.__frame_min = min
        
