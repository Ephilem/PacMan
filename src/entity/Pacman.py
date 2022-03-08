from tkinter import LEFT
import pygame

from ResourcesProvider import ResourcesProvider
from entity.Entity import Entity
from entity.MovingEntity import MovingEntity

class Pacman(MovingEntity):

    def __init__(self, game, maze_pos, case_size):
        super().__init__([pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.pacman_eating_img_frames], maze_pos, 20, case_size, game,  20)
        print(ResourcesProvider.get.pacman_eating_img_frames)
        game.on_key_press_registry.append(self)
        self.direction_to_go = None

    
    def on_key_press(self, event):
        if event.key == pygame.K_LEFT :
            self.direction_to_go = "left"           
        if event.key == pygame.K_RIGHT :
            self.direction_to_go = "right"           
        if event.key == pygame.K_UP :
            self.direction_to_go = "up"           
        if event.key == pygame.K_DOWN :
            self.direction_to_go = "down"
        pass

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_movement_system(self)
        if not self.direction_to_go is None:
            super().tick_animation()

        # IA (car render fait aussi office de ticking)
        if not self.is_moving:
            v = None
            if self.direction_to_go == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1, self.maze_pos[1])) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0]-1, self.maze_pos[1]))
            if self.direction_to_go == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1, self.maze_pos[1])) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0]+1, self.maze_pos[1]))
            if self.direction_to_go == "up" and self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]-1)) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]-1))
            if self.direction_to_go == "down" and self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]+1)) == "0":
                v = self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]+1))
            if v == "0":
                self.move(self.direction_to_go)
            else:
                self.direction_to_go = None
        #print(f"\nDirection to go : {self.direction_to_go}\nMaze_pos : {self.maze_pos}\nMap zoning:\n {self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]-1))}\n{self.game.maze.get_map_element((self.maze_pos[0]-1, self.maze_pos[1]))}@{self.game.maze.get_map_element((self.maze_pos[0]+1, self.maze_pos[1]))}\n {self.game.maze.get_map_element((self.maze_pos[0], self.maze_pos[1]+1))}")
