import pygame, os, sys

class ResourcesProvider:

    # Instance unique de la classe
    get = None

    def __init__(self):
        self.skin_id = 0
        ResourcesProvider.get = self

        # Charger toutes les images et les son de assets
        self.wall_tile_img = pygame.image.load(ResourcesProvider.__get_asset_path("wall.png"))
        # self.restart_button_img = pygame.image.load("assets/restart_button.png")
        # self.win_rond_img = pygame.image.load("assets/win_rond.png")
        # self.win_croix_img = pygame.image.load("assets/win_croix.png")
        # self.tie_img = pygame.image.load("assets/Tie.png")
        # self.icon_img = pygame.image.load("assets/logo.png")
        # self.button_skin_img = pygame.image.load("assets/button_skin.png")

        # self.less_go_sound = pygame.mixer.Sound('assets/less_go.mp3')
    
    def __get_asset_path(path):
        """
        Permet de récupéré le chemin vers la resource si le programme est éxécuter en .exe 
        :return: Soit un chemin spécial pour le .exe, soit le chemin simple pour une éxécution normal du code
        """
        try:
            base_path = sys._MEIPASS
            return os.path.join(base_path, "smg_assets\\"+str(path))
        except Exception:
            return "assets\\"+str(path)

