import pygame, random, math
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
            self.rotate(self.moving_direction)

        
        # AI mouvement (les mouvement sont aléatoire)        
        avalaible_way = self.get_available_pathway()
        if len(avalaible_way) >= 3 or self.is_blocked():
            self.moving_direction = random.choice(avalaible_way)      
        if not self.is_moving and self.can_move():
            self.move(self.moving_direction)
            self.rotate(self.moving_direction)
        

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_animation()
        self.tick_movement_system(self)
        if self.fear_tick != 0:
            self.fear_ai()
        else:
            self.tick_ai()
        
        if not self.last_pos is None:
            pygame.draw.rect(self.game.window, (0,255,255), pygame.Rect(self.last_pos[0]*self.case_size, self.last_pos[1]*self.case_size, self.case_size-10, self.case_size-10))
        for a in self.get_available_pathway():
            pygame.draw.rect(self.game.window, (255,255,0), pygame.Rect(self.shift_maze_pos_with_direction(self.maze_pos, a)[0]*self.case_size,self.shift_maze_pos_with_direction(self.maze_pos, a)[1]*self.case_size, self.case_size, self.case_size))
    
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


    

    # Fonction permettant les déplacement et de l'ia
    def is_blocked(self):
        return ((self.moving_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0") or
                (self.moving_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0") or
                (self.moving_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0") or
                (self.moving_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0"))

    def can_move(self):
        return ((self.moving_direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) == "0") or
                (self.moving_direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) == "0") or
                (self.moving_direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) == "0") or
                (self.moving_direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) == "0"))
    
    def get_available_pathway(self):
        """
        retourne les chemin possible qui sont tous sauf d'où il vient et bloquer par quelque chose (comme un mur)
        """
        final = ['up','down','left','right']
        # final.remove(self.get_opposite_direction(self.moving_direction))
        # on fait une copie de final
        for direction in [x for x in final]:
            print(self.last_pos, self.shift_maze_pos_with_direction(self.maze_pos, direction), direction, self.last_pos != self.shift_maze_pos_with_direction(self.maze_pos, direction))
            if self.last_pos != self.shift_maze_pos_with_direction(self.maze_pos, direction):
                if direction == "left" and self.game.maze.get_map_element((self.maze_pos[0]-1,self.maze_pos[1])) != "0":
                    final.remove(direction)
                if direction == "right" and self.game.maze.get_map_element((self.maze_pos[0]+1,self.maze_pos[1])) != "0":
                    final.remove(direction)
                if direction == "up" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]-1)) != "0":
                    final.remove(direction)
                if direction == "down" and self.game.maze.get_map_element((self.maze_pos[0],self.maze_pos[1]+1)) != "0":
                    final.remove(direction)
            else:
                final.remove(direction)
        return final
    
    def shift_maze_pos_with_direction(self, maze_pos, direction, shift=1):
        if direction == "left":
            return maze_pos[0]-shift,maze_pos[1]
        if direction == "right":
            return maze_pos[0]+shift,maze_pos[1]
        if direction == "up":
            return maze_pos[0],maze_pos[1]-shift
        if direction == "down":
            return maze_pos[0],maze_pos[1]+shift
    
    def get_distance_between_two_point(self, mp1, mp2):
        return math.sqrt((mp2[0]-mp1[0])**2+(mp2[1]-mp1[1])**2)
    
    def get_opposite_direction(self, direction):
        a = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        return a[direction]

    
