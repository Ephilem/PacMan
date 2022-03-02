import pygame
from ResourcesProvider import *

class WallTile:

    tiles = {
        's_e': {'tile': None, 'tile_img_slot':0},
        'n_w': {'tile': None, 'tile_img_slot':1},
        's_w': {'tile': None, 'tile_img_slot':2},
        'n_e': {'tile': None, 'tile_img_slot':3},
        'n_s': {'tile': None, 'tile_img_slot':4},
        'e_w': {'tile': None, 'tile_img_slot':5},
    }

    
    def __init__(self, case_size):
        
        self.tiles = []
        
        tile_size = (32,32)

        x0 = y0 = 0
        rect = ResourcesProvider.get.wall_tile_img.get_rect()
        w, h = rect.size
        dx = tile_size[0] + 0
        dy = tile_size[1] + 0
        print(w, h)

        reader_slot = 0
        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                key_in_tiles_dict = WallTile._finding_key_with_slot(reader_slot)
                if not key_in_tiles_dict is None:
                    tile = pygame.Surface(tile_size)
                    tile.blit(ResourcesProvider.get.wall_tile_img, (0,0), (x, y, *tile_size))   
                    pygame.transform.scale(tile, (case_size, case_size))      
                    WallTile.tiles[key_in_tiles_dict]['tile'] = tile       
                reader_slot += 1
        
        print(self.tiles)
    
    def _finding_key_with_slot(reader_slot):
        for k, v in WallTile.tiles.items():
            if v['tile_img_slot'] == reader_slot:
                return k
        return None 
    
    def get_tile(orientation):
        return WallTile.tiles[orientation]['tile']
