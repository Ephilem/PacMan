import pygame

class Endscreen():

    def __init__(self, game, end_origin):
        game.render_registry.append(self)
        print("test")
        # On va prendre un "screen" du labyrinthe pour pouvoir ensuite supprimer l'instance labyrinthe
        self.screenshot = pygame.Surface((game.maze.width_height_px[0], game.maze.width_height_px[1]))
        game.maze.render(self.screenshot, forcing=True)

        end_text = "ooooo"
        if end_origin == "win":
            end_text = "Vous avez gagné!"
        elif end_origin == "loose":
            end_text = "L + ratio + tnul"
        # généré le texte
        end_text_font = pygame.font.SysFont(None,48)
        maze_size = game.maze.width_height_px
        self.screenshot.blit(end_text_font.render(end_text, True, (255,255,255)), (maze_size[0]//2-end_text_font.size(end_text)[0], maze_size[1]//2-end_text_font.size(end_text)[1]))

    def render(self, surface):
        surface.blit(self.screenshot, (0,0))