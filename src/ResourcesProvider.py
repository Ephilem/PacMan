import pygame, os, sys

class ResourcesProvider:

    # Instance unique de la classe
    get = None

    def __init__(self):
        self.skin_id = 0
        ResourcesProvider.get = self

        # Charger toutes les images et les son de assets
        self.wall_tile_img = pygame.image.load(ResourcesProvider.__get_asset_path("wall.png"))
        self.pacgom_img = pygame.image.load(ResourcesProvider.__get_asset_path("pacgom.png"))
        self.super_pacgom_img_frames = ResourcesProvider.img_to_animation_frames(pygame.image.load(ResourcesProvider.__get_asset_path("super_pacgom.png")), 16)
        self.pacman_eating_img_frames = ResourcesProvider.img_to_animation_frames(pygame.image.load(ResourcesProvider.__get_asset_path("pacman_eating.png")), 15)

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
    
    def img_to_animation_frames(image, frame_height):
        frames = []

        y0 = 0
        rect = image.get_rect()
        w, h = rect.size
        frames_size = (w, frame_height)
        dx = frames_size[0] + 0
        dy = frames_size[1] + 0

        for y in range(y0, h, dy):
            frame = pygame.Surface(frames_size)
            frame.blit(image, (0,0), (0, y, *frames_size))    
            frames.append(frame)
        return frames


