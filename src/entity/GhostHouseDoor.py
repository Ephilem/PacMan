import pygame

from ResourcesProvider import ResourcesProvider

class GhostHouseDoor:
    """
    permet de faire la séparation entre l'intérieur et l'extérieur de la ghosthouse
    l'intérieur est situé en dessous de la porte
    l'extérieur est situé au dessus de la porte

    particularité: elle fait deux de largeur, donc c'est un peu bizarre
    """

    def __init__(self, game, case_size,  left_maze_pos, right_maze_pos):
        self.game = game
        self.case_size = case_size
        self.texture = pygame.transform.scale(ResourcesProvider.get.ghost_house_door_img, (self.case_size, self.case_size))
        
        self.left_maze_pos = left_maze_pos
        self.right_maze_pos = right_maze_pos
        self.left_pos = [a*self.case_size for a in left_maze_pos]
        self.right_pos = [a*self.case_size for a in right_maze_pos]

        pass

    def render(self, surface):
        surface.blit(self.texture, self.left_pos)
        surface.blit(self.texture, self.right_pos)

    