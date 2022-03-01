import pygame
from PacManGame import *


class Grid:
    """
        Créer la grille de morpion de 600x600 pixels à partir d'une position
    """

    def __init__(self, pos):
        # A qui le tour (0 = rond, 1 = croix) / Aléatoire à la création de la grille
        PacManGame.render_registry.append(self)
        PacManGame.on_click_registry.appand(self)
                     

    def on_click(self, event):
        pass

    def render(self, surface):
        pass