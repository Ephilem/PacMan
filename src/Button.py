#classe spécifique pour le boutton "rejouer"
import pygame

class Button:
    #permet de récupérer les valeurs "pos","image", ainsi que "act"
    def __init__(self,pos,image,act):
        self.pos = pos
        self.image = image
        self.act = act
        Button.render_registry.append(self)
        Button.on_click_registry.append(self)
    
    def on_click(self, event):
        #vérification du click
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] and mouse_pos[0] < self.pos[0]+self.image.get_width():
            if self.pos[1] < mouse_pos[1] and mouse_pos[1] < self.pos[1]+self.image.get_height():
                self.act()

    #afficher le bouton
    def render(self, surface):        
        surface.blit(self.image, self.pos)

