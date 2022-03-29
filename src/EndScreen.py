import pygame

class Endscreen():

    def __init__(self, game, end_origin):
        self.game = game
        self.end_origin = end_origin
        game.render_registry.append(self)
        game.on_click_registry.append(self)
        game.on_key_press_registry.append(self)
        # On va prendre un "screen" du labyrinthe pour pouvoir ensuite supprimer l'instance labyrinthe
        self.screenshot = pygame.Surface((game.maze.width_height_px[0], game.maze.width_height_px[1]))
        game.maze.render(self.screenshot, forcing=True)
        
        # on enlève le labyrinthe du render registry  
        game.render_registry.remove(game.maze)

        self.username = ''

    def on_click(self, event):
        self.game.render_registry.remove(self)
        self.game.on_click_registry.remove(self)
        self.game.on_key_press_registry.remove(self)
        self.game.restart_game()
    
    def on_key_press(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def render(self, surface):
        surface.blit(self.screenshot, (0,0))

        #### Rendue du texte de fin ####
        end_text = "ooooo"
        if self.end_origin == "win":
            end_text = "Vous avez gagné!"
        elif self.end_origin == "loose":
            end_text = "L + ratio + tnul"
        # généré le texte
        end_title_text_font = pygame.font.SysFont(None,48)
        maze_size = self.game.maze.width_height_px
        surface.blit(end_title_text_font.render(end_text, True, (255,255,255)), ((maze_size[0]//2)-end_title_text_font.size(end_text)[0]//2, (maze_size[1]//2)-end_title_text_font.size(end_text)[1]))

        #### Rendue du pseudo input ####
        end_text_font = pygame.font.SysFont(None, 24)
        end_text_font_size = end_text_font.size("Entre ton pseudo si tu sauvegarde ton score")
        surface.blit(end_title_text_font.render("Entre ton pseudo si tu sauvegarde ton score", True, (255,255,255)), ((maze_size[0]//2)-end_text_font_size[0]//2, maze_size[1]//2))
        
        username_text_font = pygame.font.SysFont(None, 32)


