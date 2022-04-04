from operator import itemgetter
from Button import Button
from Highscore import Highscore
import pygame

from ResourcesProvider import ResourcesProvider

class Scoreboard():



    def __init__(self, game, pos):
        self.score_value = 0
        self.game = game
        self.pos = pos

        self.game.render_registry.append(self)

        self.scoreboard_surface = pygame.Surface((300, self.game.maze.width_height_px[1]))
        self.update_render = True

        # Stocke tout les boutons pour supprimer des scores
        self.delete_scores_buttons = []
        
    
        pass

    def render(self, surface):
        if self.update_render:
            self.scoreboard_surface.fill((255,255,255))
            surface_size = self.scoreboard_surface.get_size()
            
            score_value_text = ("0"*(10-len(str(self.score_value)))+str(self.score_value))
            score_value_to_render = ResourcesProvider.get.score_font.render(score_value_text, True, (0,0,0))
            score_value_text_size = score_value_to_render.get_size()
            self.scoreboard_surface.blit(score_value_to_render, (surface_size[0]//2-score_value_text_size[0]//2, 50))    

            score_text = ResourcesProvider.get.bungee_font.render("Score", True, (0, 0, 0))
            score_text_size = score_text.get_size()
            self.scoreboard_surface.blit(score_text, (surface_size[0]//2-score_text_size[0]//2, 10))

            self.render_leaderboard()
            self.update_render = False

        surface.blit(self.scoreboard_surface, (self.game.maze.width_height_px[0],0))  

    def add_score(self, v):
        self.score_value += v
        self.update_render()

    def reset(self):
        self.score_value = 0
        self.update_render()
    
    def update_render(self):
        self.update_render = True
    
    def render_leaderboard(self): 
        # Avant de refaire le leadboard, on reset tout les boutons
        for b in self.delete_scores_buttons:
            b.unregister() 

        surface_size = self.scoreboard_surface.get_size()
        whp = self.game.maze.width_height_px
        leadboard_text = ResourcesProvider.get.bungee_font.render("Leadboard", True, (0, 0, 0))
        leadboard_text_size = leadboard_text.get_size()
        self.scoreboard_surface.blit(leadboard_text, (surface_size[0]//2-leadboard_text_size[0]//2, 100))
        
        for index, score in enumerate(sorted(Highscore.get(self.game.maze.level), key=itemgetter(1), reverse=True)):
            username_text = ResourcesProvider.get.users_font.render(score[0], True, (0, 0, 0))
            username_text_size = username_text.get_size()
            self.scoreboard_surface.blit(username_text, (surface_size[0]//4-username_text_size[0]//2, 150+index*35))

            record_text = ResourcesProvider.get.highscore_font.render(str(score[1]), True, (0, 0, 0))
            record_text_size = record_text.get_size()
            self.scoreboard_surface.blit(record_text, ((surface_size[0]*3/4)-record_text_size[0]//2, 150+index*35))

            self.delete_scores_buttons.append(Button(self.game, (surface_size[0]-10+whp[0], 150+index*35), (10,10), "X", self.update_render, (221, 44, 0), (163, 0, 0), (255,255,255)))


    
