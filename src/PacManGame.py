from telnetlib import GA
import pygame, time
from EndScreen import Endscreen
from Highscore import Highscore
from Maze import *
from Button import *
from ResourcesProvider import *
from Scoreboard import Scoreboard


class PacManGame():
    """
    La classe qui représente le programme entier   
    """    


    def __init__(self):
        # Initialiser le mixeur audio & le resource provider
        pygame.mixer.init()
        pygame.font.init()
        ResourcesProvider()    

        # Registre
        self.render_registry = []
        self.on_click_registry = []
        self.on_key_press_registry = []

        self.clock = pygame.time.Clock()
        
        self.maze = Maze(self, (0,0), '1')
        self.game_stat = "playing"

        # les options de la partie (les scattering time n'est pas utiliser par blinky au début)
        self.game_options = {
            'ghost_fear_time': 700,
            'pinky_get_out_at': 500,
            'clyde_get_out_at': 1000,
            'inky_get_out_at': 1500,
            'blinky_scattering_time': 800,
            'clyde_scattering_time': 800,
            'inky_scattering_time': 500,
            'pinky_scattering_time': 500,
        }
        

        self.scoreboard = Scoreboard(self, (self.maze.width_height_px[0],0))

        # Création de la fenêtre
        self.window_width = self.maze.width_height_px[0]
        self.window_height = self.maze.width_height_px[1]
        self.window = pygame.display.set_mode((self.window_width+300,self.window_height))
        pygame.display.set_caption("PacMan Ghost's Slayer")
        ## pygame.display.set_icon(ResourcesProviders.get.icon_img)

        GAME_INSTANCE = self

        # Boucle principal 
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    self.on_key_press(event)
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)
            
            if self.game_stat == "winning":
                self.game_stat = "win"
                Endscreen(self, "win")
            elif self.game_stat == "losing":
                self.game_stat = "loose"
                Endscreen(self, "loose")
            self.render()        
            self.clock.tick(100)    
       
        pygame.quit()

    
    def on_key_press(self, event):
        for elem in self.on_key_press_registry:
            elem.on_key_press(event)      

    def on_click(self, event):
        """
        Call les on_click de tout les élément dans le registre
        """
        if pygame.mouse.get_pressed() == (1,0,0) :
            for object in self.on_click_registry:
                object.on_click(event)
    

    def render(self):
        """
        Call les render de tout les élément dans le registre
        Render fait aussi service de ticking
        """
        self.window.fill((0,0,0))
        for elem in self.render_registry:
            elem.render(self.window)
        self.render_fps()
        pygame.display.flip()

    def restart_game(self):
        self.maze = Maze(self, (0,0), '1')
        self.game_stat = "playing"
        self.scoreboard.reset()
    
    def render_fps(self):
        font = ResourcesProvider.get.debug_font
        fps_text = "FPS:"+str(round(self.clock.get_fps()))
        tick_text = "TICK:"+str(round(self.clock.get_time()))
        fps_size = font.size(fps_text)
        tick_size = font.size(tick_text)
        self.window.blit(font.render(fps_text, True, (0,0,0)), (self.maze.width_height_px[0],self.maze.width_height_px[1]-fps_size[1]))
        self.window.blit(font.render(tick_text, True, (0,0,0)), (self.maze.width_height_px[0]+80-tick_size[0],self.maze.width_height_px[1]-tick_size[1]))




if __name__ == "__main__":
    PacManGame()
