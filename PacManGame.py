import pygame
from Maze import *
from Button import *
from ResourcesProviders import *

class PacManGame:
    """
    La classe qui représente le programme entier   
    """

    
    

    def __init__(self):

        # Initialiser le mixeur audio & le resource provider
        pygame.mixer.init()
        ResourcesProviders()    

        # Registre
        self.render_registry = []
        self.on_click_registry = []
        

        self.grid = Maze(self, (0,0), 0)


        # Création de la fenêtre
        self.window_width = self.grid.width_height_px[0]
        self.window_height = self.grid.width_height_px[1]
        self.window = pygame.display.set_mode((500,500))
        pygame.display.set_caption("Super Pac Man GALAXY")
        ## pygame.display.set_icon(ResourcesProviders.get.icon_img)

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
       
        pygame.quit()

    
    def on_key_press(self, event):
        # Quand on appuis sur entré, on recommence la partie
        if event.key == pygame.K_RETURN:
            self.grid.reset()
            

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
        """
        self.window.fill((0,0,0))
        for elem in self.render_registry:
            elem.render(self.window)
        pygame.display.flip()






if __name__ == "__main__":
    PacManGame()
