import math
from Button import Button
from Highscore import Highscore
from ResourcesProvider import ResourcesProvider
import pygame, re

class Endscreen():

    def __init__(self, game, end_origin):
        self.game = game
        self.end_origin = end_origin
        game.render_registry.append(self)
        game.on_key_press_registry.append(self)
        # On va prendre un "screen" du labyrinthe pour pouvoir ensuite supprimer l'instance labyrinthe
        self.screenshot = pygame.Surface((game.maze.width_height_px[0], game.maze.width_height_px[1]))
        game.maze.render(self.screenshot, forcing=True)
        
        # on enlève le labyrinthe du render registry  
        game.render_registry.remove(game.maze)
        maze_size = self.game.maze.width_height_px
        self.button_continue = Button(self.game, (maze_size[0]//2-150//2,maze_size[1]-200), (150,40), "Continuer", self.on_score_button_clicked, (104, 159, 56), (54, 111, 0), (0,0,0))
        

        self.username = ''
        self.cursor_blinking_tick = 0

        self.highscore = False
        self.highscore_animation_tick = 0

    def on_score_button_clicked(self):
        if not len(self.username) == 0:
            Highscore.set_highscore(self.username, self.game.scoreboard.score_value, self.game.maze.level)
            self.game.scoreboard.update_render()
        self.game.render_registry.remove(self)
        self.button_continue.unregister()
        self.game.on_key_press_registry.remove(self)
        self.game.restart_game()
    
    
    def on_key_press(self, event):
        if event.type == pygame.KEYDOWN:
            # vérifier si il y a eu un changement
            username_changed = False
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
                username_changed = True
            else:
                if re.match("\A[A-Z0-9]\Z", event.unicode.upper()) and len(self.username) < 10:
                    self.username += event.unicode.upper()
                    username_changed = True
            if username_changed:
                self.highscore = Highscore.is_highscore(self.username, self.game.scoreboard.score_value, self.game.maze.level)
            

    def render(self, surface):
        surface.blit(self.screenshot, (0,0))

        #### Rendue du texte de fin ####
        end_text = "ooooo"
        if self.end_origin == "win":
            end_text = "Vous avez gagné!"
        elif self.end_origin == "loose":
            end_text = "L + ratio + tnul"

        maze_size = self.game.maze.width_height_px

        # généré le font
        background_surface = pygame.Surface((400, maze_size[1]), flags=pygame.SRCALPHA)
        background_surface.fill((255,255,255,150))
        surface.blit(background_surface, (maze_size[0]//2-200, 0))

        # généré le texte
        end_title_text_font = pygame.font.SysFont(None,48)
        surface.blit(end_title_text_font.render(end_text, True, (0,0,0)), ((maze_size[0]//2)-end_title_text_font.size(end_text)[0]//2, (maze_size[1]//2)-end_title_text_font.size(end_text)[1]))

       
        end_text_font = pygame.font.SysFont(None, 24)
        end_text_font_size = end_text_font.size("Entre ton pseudo si tu sauvegarde ton score")
        surface.blit(end_text_font.render("Entre ton pseudo si tu sauvegarde ton score", True, (0,0,0)), ((maze_size[0]//2)-end_text_font_size[0]//2, maze_size[1]//2))
        
         #### Rendue du username input ####
        username_text_font = ResourcesProvider.get.user_input_box_font
        username_text_to_render = self.username+"_" if self.cursor_blinking_tick < 25 else self.username+" "
        username_text_font_size = username_text_font.size(username_text_to_render)
        surface.blit(username_text_font.render(username_text_to_render, True, (0,0,0)), ((maze_size[0]//2)-username_text_font_size[0]//2, maze_size[1]//2+50))
        self.cursor_blinking_tick += 1 
        if self.cursor_blinking_tick > 50:
            self.cursor_blinking_tick = 0
        
        ### Rendue de l'highscore ###
        if self.highscore:
            self.highscore_animation_tick += 1
            to_scale = round(math.cos(self.highscore_animation_tick*(1/25))*10+10)
            image_size = (250,67)
            surface.blit(pygame.transform.scale(ResourcesProvider.get.highscore_img, (to_scale+image_size[0], to_scale+image_size[1])), (maze_size[0]//2-image_size[0]//2-to_scale//2,maze_size[1]//4-image_size[1]//2-to_scale//2))

