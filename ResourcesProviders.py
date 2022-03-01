import pygame

class ResourcesProviders :

    # Instance unique de la classe
    get = None

    def __init__(self):
        self.skin_id = 0
        ResourcesProviders.get = self

        # Charger les skins
        self.skins = (
            pygame. transform. scale(pygame.image.load("assets/0rond.png"),(190,190)),
            pygame. transform. scale(pygame.image.load("assets/0croix.png"),(190,190)),
            pygame. transform. scale(pygame.image.load("assets/1rond.png"),(190,190)),
            pygame. transform. scale(pygame.image.load("assets/1croix.png"),(190,190)),
        )

        # Charger les skin de base
        self.rond = self.skins[0]
        self.croix = self.skins[1]

        # Charger toutes les images et les son de assets
        self.restart_button_img = pygame.image.load("assets/restart_button.png")
        self.win_rond_img = pygame.image.load("assets/win_rond.png")
        self.win_croix_img = pygame.image.load("assets/win_croix.png")
        self.tie_img = pygame.image.load("assets/Tie.png")
        self.icon_img = pygame.image.load("assets/logo.png")
        self.button_skin_img = pygame.image.load("assets/button_skin.png")
        self.less_go_sound = pygame.mixer.Sound('assets/less_go.mp3')

