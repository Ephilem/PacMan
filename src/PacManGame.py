from telnetlib import GA
import pygame, time
from Maze import *
from Button import *
from ResourcesProvider import *


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
        
        self.maze = Maze(self, (0,0), 0)

        # Création de la fenêtre
        self.window_width = self.maze.width_height_px[0]
        self.window_height = self.maze.width_height_px[1]
        print(self.window_width,self.window_height)
        self.window = pygame.display.set_mode((self.window_width+200,self.window_height))
        pygame.display.set_caption("Super Pac Man GALAXY")
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
        self.window.blit(pygame.font.SysFont(None,48).render(str(round(self.clock.get_fps())), True, (255,255,255)), (self.maze.width_height_px[0]+10,0))
        pygame.display.flip()




if __name__ == "__main__":
    PacManGame()
