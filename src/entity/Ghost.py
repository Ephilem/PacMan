import pygame, random, math
from abc import abstractmethod
from ResourcesProvider import ResourcesProvider
from entity.MovingEntity import MovingEntity

class Ghost(MovingEntity):

    def __init__(self, texture, maze_pos, case_size, game, ghost_name, not_spawning_in_the_ghost_house=False):
        self.GHOST_TEXTURE = texture
        self.GHOST_NAME = ghost_name
        self.FEAR_GHOST_TEXTURE = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.fear_img_frames]
        self.EATED_GHOST_TEXTURE = [pygame.transform.scale(frame, (case_size, case_size)) for frame in ResourcesProvider.get.eated_img_frames]
        super().__init__(self.GHOST_TEXTURE, maze_pos, 15, case_size, game, ticks_between_frame=30)
        self.mode = "waiting" # les modes : scattering, chasing, fear, eated, getting_out_ghost_house, waiting
        self.set_frame_min_max(min=0,max=2)
        self.fear_tick = 0
        self.scattering_tick = 0

        if not_spawning_in_the_ghost_house:
            self.mode = "scattering"
            self.scattering_tick = 700

        ## Cela permet de controller la sortie/l'entrer du fantome
        self.ghost_house_tick = 0
        self.ghost_house_step = "nothing" # valeur possible : goto, passing
        self.ghost_house_passing_side = None

    def render(self, surface, pos_to_render):
        surface.blit(self.frame, self.get_pos_to_render(pos_to_render))
        self.tick_animation()
        if not self.mode == "waiting":
            self.tick_movement_system(self)
            if self.fear_tick != 0:
                self.fear_ai()
            elif self.mode == "scattering":
                self.scattering_ai()
            elif self.mode == "getting_out_ghost_house":
                self.getting_out_of_the_ghost_house_ai()
            elif self.mode == "eated":
                self.eated_ai()
            else:
                self.chasing_ai()
            
    
    ####################################################
    #### Les fontion AI qui sont appeller en boucle ####
    ####################################################
    @abstractmethod
    def chasing_ai(self):
        pass

    def fear_ai(self):
        # Réduir le fear ai
        self.fear_tick -= 1
        if self.fear_tick == 0 and self.mode == "fear":
            self.mode = "chasing"
            self.change_max_sleep_tick(15)
            self.change_texture(self.GHOST_TEXTURE, True)
            self.rotate(self.moving_direction)
        
        # AI mouvement (les mouvements sont aléatoire)        
        self.move_ai_rand()  
        
    def getting_out_of_the_ghost_house_ai(self):
        ghd = self.game.maze.ghost_house_door

        if self.ghost_house_step == "goto":
            if self.maze_pos == ghd.interior_left_side_maze_pos or self.maze_pos == ghd.interior_right_side_maze_pos:
                self.ghost_house_step = "passing"
            elif not self.is_moving:           
                # le faire bouger toujours vers le côter gauche de la porte. Si il passe du côter droit, il sera pris directement
                self.move_ai(ghd.interior_left_side_maze_pos)
        elif self.ghost_house_step == "passing":
            if self.maze_pos == ghd.exterior_right_side_maze_pos or self.maze_pos == ghd.exterior_left_side_maze_pos:
                self.ghost_house_step = None
                # quand il sorte de la maison, qu'il passe en scattering
                self.scattering()  
            elif not self.is_moving:           
                self.forcing_movement_to("up")  
    
    def eated_ai(self):
        """
        On poourrai l'appeller aussi getting_in_the_ghost_house_ai, car sa revient à la même chose (en étant manger, il doit rentrer dans la maison)
        """
        ghd = self.game.maze.ghost_house_door

        if self.ghost_house_step == "goto":
            if self.maze_pos == ghd.exterior_left_side_maze_pos or self.maze_pos == ghd.exterior_right_side_maze_pos:
                self.ghost_house_step = "passing"
                self.change_max_sleep_tick(15)
            elif not self.is_moving:           
                # le faire bouger toujours vers le côter gauche de la porte. Si il passe du côter droit, il sera pris directement
                self.move_ai(ghd.exterior_left_side_maze_pos)
        elif self.ghost_house_step == "passing":
            if self.maze_pos == ghd.interior_right_side_maze_pos or self.maze_pos == ghd.interior_left_side_maze_pos:
                self.ghost_house_step = None
                # quand il rentre dans la maison, qu'il passe en normal et qui sorte de la maison    
                self.change_texture(self.GHOST_TEXTURE, True)
                self.getting_out_ghost_house()  
            elif not self.is_moving:           
                self.forcing_movement_to("down")  

    def scattering_ai(self):
        self.scattering_tick -= 1
        #print(self.GHOST_NAME, self.scattering_tick, self.mode)
        if self.scattering_tick <= 0:
            self.mode = "chasing"
        
        # Par rapport au fantome, on le fait tourner dans un coins
        if self.GHOST_NAME == "blinky":
            self.move_ai([x//self.case_size+5 for x in self.game.maze.width_height_px])
        elif self.GHOST_NAME == "pinky":
            self.move_ai([-5,-5])
        elif self.GHOST_NAME == "inky":
            corner = [x//self.case_size+5 for x in self.game.maze.width_height_px]
            corner[0] = -5 
            self.move_ai(corner)
        elif self.GHOST_NAME == "clyde":
            corner = [x//self.case_size+5 for x in self.game.maze.width_height_px]
            corner[1] = -5 
            self.move_ai(corner)



    ##############################################
    #### Permet de changer le mode du fantome ####
    ##############################################
    def fear(self):
        """
        mettre le fantome en mode 'fear'
        """
        if self.mode == "scattering" or self.mode == "chasing":
            self.mode = "fear"
            self.fear_tick = self.game.game_options['ghost_fear_time']
            self.change_max_sleep_tick(20)
            self.set_frame_min_max(min=0,max=1)
            self.change_texture(self.FEAR_GHOST_TEXTURE, True) 
            self.moving_direction = self.get_opposite_direction(self.moving_direction)
            self.moving_to = self.maze_pos
    
    def eated(self):
        """
        mettre le fantome en mode 'eated'
        """
        if self.mode == "fear":
            self.mode = "eated"
            self.fear_tick = 0
            self.ghost_house_step = "goto"
            self.change_max_sleep_tick(8)
            self.set_frame_min_max(min=0,max=2)
            self.change_texture(self.EATED_GHOST_TEXTURE, True)
    
    def scattering(self):
        """
        mettre le fantome en mode 'scattering'
        """
        if self.mode == "chasing" or self.mode == "getting_in_ghost_house" or self.mode == "getting_out_ghost_house" or self.mode == "waiting":
            self.mode = "scattering"
            self.scattering_tick = self.game.game_options[self.GHOST_NAME+"_scattering_time"]

    def getting_out_ghost_house(self):
        self.mode = "getting_out_ghost_house"
        self.ghost_house_step = "goto"


    ###################################################
    #### Fonction permettant les ia de fonctionner ####
    ###################################################
    def move_ai(self, target_maze_pos, rotate=True):
        """
        permet de bouger vers un point
        """
        available_direction = self.get_available_pathway()
        # On vérifie que si il n'y a aucune direction valide, alors on vire 
        if len(available_direction) == 0:
            return
        best_direction_and_distance = (None, 999) # couple direction-distance
        for direction in available_direction:
            distance = self.get_distance_between_two_point(self.shift_maze_pos_with_direction(self.maze_pos, direction), target_maze_pos)
            if distance < best_direction_and_distance[1]:
                best_direction_and_distance = (direction, distance)

        self.move(best_direction_and_distance[0])
        if rotate:
            self.rotate(best_direction_and_distance[0])
    
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
        
    def forcing_movement_to(self, direction):
        """
        une fonction permettant de ce dépacer sans faire attention au obstacle
        """
        self.move(direction)
        self.rotate(direction)

    def move_ai_rand(self, rotate=True):
        """
        permet de bouger de façon aléatoire. utiliser par clyde et les phantome en mode 'fear'
        """
        avalaible_way = self.get_available_pathway()
        self.moving_direction = random.choice(avalaible_way) 
        self.move(self.moving_direction)
        if rotate:
            self.rotate(self.moving_direction)
    
    def get_available_pathway(self):
        """
        retourne les chemin possible qui sont tous sauf d'où il vient et bloquer par quelque chose (comme un mur)
        """
        # l'ordre les direction dans cette liste est importante car ces cette ordre qui va départir les égalité
        final = ['up','right','down','left']

        # on fait une copie de final
        for direction in [x for x in final]:
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

    
