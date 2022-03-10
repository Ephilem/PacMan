import pygame
from abc import abstractmethod
from ResourcesProvider import ResourcesProvider
from entity.MovingEntity import MovingEntity

class Ghost(MovingEntity):

    def __init__(self, ghost_type, maze_pos, case_size, game):
        if ghost_type == "blinky":
            images = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.blinky_img_frames]
        elif ghost_type == "clyde":
            images = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.clyde_img_frames]
        elif ghost_type == "inky":
            images = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.inky_img_frames]
        elif ghost_type == "pinky":
            images = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.pinky_img_frames]
        super().__init__(images, maze_pos, 15, case_size, game, ticks_between_frame=30)
        self.mode = "scattering" # les modes : scattering, chasing, running_away, eated        
        self.set_frame_min_max(min=0,max=2)
        print(self.get_frame_min_max)

    @abstractmethod
    def tick_ai(self):
        pass

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_animation()
        self.tick_movement_system(self)
        self.tick_ai()
    
    def rotate(self, direction):
        if direction == "left":
            self.set_frame_min_max(min=6,max=7)
        if direction == "right":
            self.set_frame_min_max(min=0,max=1)
        if direction == "up":
            self.set_frame_min_max(min=4,max=5)
        if direction == "down":
            self.set_frame_min_max(min=2,max=3)
        pass

    def move_with_ai_grid(self, ai_grid):
        ai_value = self.get_ai_value(ai_grid, self.maze_pos)
        to_go = ai_value-1
        if self.get_ai_value(ai_grid, (self.maze_pos[0]-1,self.maze_pos[1])) == to_go:
            self.move("left")
            self.rotate("left")
        if self.get_ai_value(ai_grid, (self.maze_pos[0]+1,self.maze_pos[1])) == to_go:
            self.move("right")
            self.rotate("right")
        if self.get_ai_value(ai_grid, (self.maze_pos[0],self.maze_pos[1]-1)) == to_go:
            self.move("up")
            self.rotate("up")
        if self.get_ai_value(ai_grid, (self.maze_pos[0],self.maze_pos[1]+1)) == to_go:
            self.move("down")
            self.rotate("down")
            
    def get_ai_value(self, ai_grid, maze_pos):
        return ai_grid[maze_pos[1]][maze_pos[0]]
    

    

    

# a ok dsl, je pensait que t juste venue faire un call, j'avais pas vue ^^'
# tu veut quoi?


# hein? tkinter?
# c pas pour des jeu sa 
# wait vous utiliser tkinter??????????????????????????????
#nan tkt
#tes fantomes ils fonctionnes en vanilla genre avec juste python ou il faut pygame
# il faut déjà faire une grille d'ia, comme est expliquer sur la feuille (numéroter les case par rapport à la distance de pacman)
# ah oe flemme
