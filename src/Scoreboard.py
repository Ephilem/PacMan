import pygame

class Scoreboard():



    def __init__(self, game, pos):
        self.score_value = 0
        self.game = game
        self.pos = pos

        self.game.render_registry.append(self)

        self.score_font = pygame.font.SysFont(None,48)
        pass

    def render(self, surface):
        surface.blit(self.score_font.render(str(self.score_value), True, (255,255,255)), self.pos)

    def add_score(self, v):
        self.score_value += v
    def reset(self):
        self.score_value = 0

pass