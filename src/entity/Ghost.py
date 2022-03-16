import pygame, random
from abc import abstractmethod
from ResourcesProvider import ResourcesProvider
from entity.MovingEntity import MovingEntity

class Ghost(MovingEntity):

    def __init__(self, texture, maze_pos, case_size, game):
        self.GHOST_TEXTURE = texture
        self.FEAR_GHOST_TEXTURE = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.fear_img_frames]
        super().__init__(self.GHOST_TEXTURE, maze_pos, 15, case_size, game, ticks_between_frame=30)
        self.mode = "scattering" # les modes : scattering, chasing, fear, eated        
        self.set_frame_min_max(min=0,max=2)
        self.fear_tick = 0

        # Cette valeur est utiliser seulement par clyde et quand les fantome sont en mode "peur"
        self.looking_direction = "up"

    @abstractmethod
    def tick_ai(self):
        pass

    def fear_ai(self):
        # Réduir le fear ai
        self.fear_tick -= 1
        if self.fear_tick == 0:
            self.mode = "chasing"
            self.change_max_sleep_tick(15)
            self.change_texture(self.GHOST_TEXTURE, True)
            self.rotate(self.looking_direction)

        
        # AI mouvement (les mouvement sont aléatoire)        
        avalaible_way = self.get_available_pathway()
        if len(avalaible_way) >= 3 or self.is_blocked():
            self.looking_direction = random.choice(avalaible_way)      
        if not self.is_moving and self.can_move():
            self.move(self.looking_direction)
            self.rotate(self.looking_direction)
        

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_animation()
        self.tick_movement_system(self)
        if self.fear_tick != 0:
            self.fear_ai()
        else:
            self.tick_ai()
    
    def rotate(self, direction):
        if not self.mode == "fear":
            if direction == "left":
                self.set_frame_min_max(min=6,max=7)
            if direction == "right":
                self.set_frame_min_max(min=0,max=1)
            if direction == "up":
                self.set_frame_min_max(min=4,max=5)
            if direction == "down":
                self.set_frame_min_max(min=2,max=3)

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
    
    def fear(self):
        """
        mettre les fantome en mode 'fear'
        """
        if self.mode == "scattering" or self.mode == "chasing":
            self.mode = "fear"
            self.fear_tick = 500
            self.change_max_sleep_tick(20)
            self.set_frame_min_max(min=0,max=1)
            self.change_texture(self.FEAR_GHOST_TEXTURE, True)


    

    # Fontion de mouvement aléatoire pour le mode fear (car quand le fantome à peur, et bas il se déplace aléatoirement)
    def is_blocked(self):
        return ((self.looking_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0") or
                (self.looking_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0") or
                (self.looking_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0") or
                (self.looking_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0"))

    def can_move(self):
        return ((self.looking_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) == "0") or
                (self.looking_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) == "0") or
                (self.looking_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) == "0") or
                (self.looking_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) == "0"))
    
    def get_available_pathway(self):
        final = ['up','down','left','right']
        final.remove(self.get_opposite_direction(self.looking_direction))
        for direction in final:
            if direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0":
                final.remove(direction)
            if direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0":
                final.remove(direction)
            if direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0":
                final.remove(direction)
            if direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0":
                final.remove(direction)
        return final
    
    
    def get_opposite_direction(self, direction):
        a = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        return a[direction]

    
