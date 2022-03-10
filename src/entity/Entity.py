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
                if self.frame_id > self.__frame_max:
                    self.frame_id = self.__frame_min
                self.frame = self.textures[self.frame_id]
    
    @abstractmethod
    def render(self, surface, pos_to_render):
        pass

    def change_texture(self, textures, go_to_the_first_frame=False):
        self.textures = textures
        if go_to_the_first_frame:
            self.frame = textures[self.__frame_min]        
            self.frame_id = self.__frame_min
        self.tick = 0
    
    def set_frame_min_max(self, min, max):
        if self.__frame_max != max and self.__frame_min != min:
            self.__frame_max = max
            self.__frame_min = min
            self.frame_id = min
            self.frame = self.textures[min]

    def get_frame_min_max(self):
        return self.__frame_min, self.__frame_max
        
