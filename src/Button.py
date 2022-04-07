import pygame

class Button:
    #permet de récupérer les valeurs "pos","image", ainsi que "act"
    def __init__(self, game, pos, size, text, act, background_color, dark_background_color, text_color):
        self.game = game
        self.pos = pos
        self.size = size
        self.text = text
        self.act = act
        self.background_color = background_color
        self.dark_background_color = dark_background_color
        self.text_color = text_color
        game.render_registry.append(self)
        game.on_click_registry.append(self)
    
    def on_click(self, event):
        #vérification du click
        mouse_pos = pygame.mouse.get_pos()

        if pygame.Rect(self.pos[0], self.pos[1]-5, self.size[0], self.size[1]).collidepoint(mouse_pos):
            self.act()

    #afficher le bouton
    def render(self, surface):       
        button_surface = pygame.Surface((self.size[0],self.size[1]+5))
        button_surface.fill(self.background_color)
        
        render_pos = list(self.pos)
        button_surface_size = button_surface.get_size()
        font = pygame.font.SysFont(None, 24)
        text_size = font.size(self.text)

        # faire l'ombre
        render_pos[1] -= 5        
        pygame.draw.rect(button_surface, self.dark_background_color, pygame.Rect(0, button_surface_size[1]-5, button_surface_size[0], 5))

        button_surface.blit(font.render(self.text, True, self.text_color), (button_surface_size[0]//2-text_size[0]//2,button_surface_size[1]//2-text_size[1]//2))

        surface.blit(button_surface, render_pos)
    
    def unregister(self):
        self.game.render_registry.remove(self)
        self.game.on_click_registry.remove(self)
    