from asyncore import read
import pygame


class Maze:
    """
        Créer la grille de morpion de 600x600 pixels à partir d'une position
    """

    def __init__(self, game, pos, level):
        game.render_registry.append(self)
        game.on_click_registry.append(self)

        self.CASE_SIZE = 15
        
        self.level_layout = self.read_level_file(0) 
        self.width_height_px =  len(self.level_layout)*self.CASE_SIZE,len(self.level_layout[0])*self.CASE_SIZE  
        print(self.level_layout)
        for i in self.level_layout:
            for j in i:
                print(j, end=" ")
            print("")
        # Retourner la taille du labirynthe généré

    def read_level_file(self, level):
        with open("levels/"+str(level)+".txt") as f:
            contents = f.read()
            lines = contents.split("\n") 
        return [ [y for y in x] for x in lines]


    def on_click(self, event):
        pass

    def render(self, surface):   
        for y, lines in enumerate(self.level_layout):
            for x, v in enumerate(lines): 
                color = (0,0,0)
                if v == "m":
                    color = (255,0,0)
                elif v == " ":
                    color = (255,255,255)
                pygame.draw.rect(surface, color, pygame.Rect(
                    x*self.CASE_SIZE, 
                    y*self.CASE_SIZE, 
                    self.CASE_SIZE, 
                    self.CASE_SIZE
                ))
                pygame.draw.rect(surface, (0,255,0), pygame.Rect(
                    x*self.CASE_SIZE, 
                    y*self.CASE_SIZE, 
                    self.CASE_SIZE, 
                    self.CASE_SIZE
                ),2)
                    
        pass