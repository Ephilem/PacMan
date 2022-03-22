import pygame

from ResourcesProvider import ResourcesProvider

class Scoreboard():



    def __init__(self, game, pos):
        self.score_value = 0
        self.game = game
        self.pos = pos

        self.game.render_registry.append(self)

        self.scoreboard_surface = pygame.Surface((300, self.game.maze.width_height_px[1]))
        
    
        pass

    def render(self, surface):
        self.scoreboard_surface.fill((255,255,255))
        surface_size = self.scoreboard_surface.get_size()
        
        score_value_text = ("0"*(10-len(str(self.score_value)))+str(self.score_value))
        score_value_to_render = ResourcesProvider.get.score_font.render(score_value_text, True, (0,0,0))
        score_value_text_size = score_value_to_render.get_size()
        self.scoreboard_surface.blit(score_value_to_render, (surface_size[0]//2-score_value_text_size[0]//2, 50))    

        score_text = ResourcesProvider.get.bungee_font.render("Score", True, (0, 0, 0))
        score_text_size = score_text.get_size()
        self.scoreboard_surface.blit(score_text, (surface_size[0]//2-score_text_size[0]//2, 10))

        leadboard_text = ResourcesProvider.get.bungee_font.render("Leadboard", True, (0, 0, 0))
        leadboard_text_size = leadboard_text.get_size()
        self.scoreboard_surface.blit(leadboard_text, (surface_size[0]//2-leadboard_text_size[0]//2, 100))

        surface.blit(self.scoreboard_surface, (self.game.maze.width_height_px[0],0))

        text = ResourcesProvider.get.users_font.render("Toto", True, (0, 0, 0))
        score_text_size = text.get_size()
        self.scoreboard_surface.blit(text, (surface_size[0]//2- score_text_size[1]//2, 150))

        surface.blit(self.scoreboard_surface, (self.game.maze.width_height_px[0],0))

        text = ResourcesProvider.get.users_font.render("Nathalia", True, (0, 0, 0))
        score_text_size = text.get_size()
        self.scoreboard_surface.blit(text, (325, 150))

        surface.blit(self.scoreboard_surface, (self.game.maze.width_height_px[0],0))

#Faire un tableau composé de rectangle et utiliser la système pygame qui permet de centrer le txt au milieu du rectangle(10 places au leaderboard)
#https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    
    
    
    def save_core(self, score_final):
        pass
            

    def add_score(self, v):
        self.score_value += v

    def reset(self):
        self.score_value = 0
    
    
