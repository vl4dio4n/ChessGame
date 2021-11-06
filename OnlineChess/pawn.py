import pygame
from pygame.math import Vector2

pygame.init()

class Pawn():
    def __init__(self, pos, color, game_config):
        self.char = 'P'
        self.pos = pos
        self.color = color
        self.moved = False
        self.attacked_pos, self.defensed_pos = self.get_pos(game_config)
        self.valid_moves = []

    def opposite_color(self, color):
        if color[0] == 'w':
            return 'b'
        return 'w'

    def get_pos(self, game_config):
        attacked_pos = []
        defensed_pos = []
        if self.color == 'white':
            new_pos = self.pos + Vector2(0, -1)
        else:
            new_pos = self.pos + Vector2(0, 1)
        if 0 <= new_pos.x < 8 and 0 <= new_pos.y < 8:
            if game_config[int(new_pos.y)][int(new_pos.x)] == '':
                attacked_pos.append(new_pos)
            
        if not self.moved:
            if self.color == 'white':
                _pos = self.pos + Vector2(0, -1)
                new_pos = self.pos + Vector2(0, -2)
            else:
                _pos = self.pos + Vector2(0, 1)
                new_pos = self.pos + Vector2(0, 2)
            if 0 <= new_pos.x < 8 and 0 <= new_pos.y < 8:
                if game_config[int(new_pos.y)][int(new_pos.x)] == '' and game_config[int(_pos.y)][int(_pos.x)] == '':
                    attacked_pos.append(new_pos)
                
        if self.color == 'white':
            new_pos = self.pos + Vector2(1, -1)
        else:
            new_pos = self.pos + Vector2(1, 1)
        if 0 <= new_pos.x < 8 and 0 <= new_pos.y < 8:
            if game_config[int(new_pos.y)][int(new_pos.x)] != '': 
                if game_config[int(new_pos.y)][int(new_pos.x)][0] == self.opposite_color(self.color[0]):
                    attacked_pos.append(new_pos)
        defensed_pos.append(new_pos)
        

        if self.color == 'white':
            new_pos = self.pos + Vector2(-1, -1)
        else:
            new_pos = self.pos + Vector2(-1, 1)
        if 0 <= new_pos.x < 8 and 0 <= new_pos.y < 8:
            if game_config[int(new_pos.y)][int(new_pos.x)] != '':
                if game_config[int(new_pos.y)][int(new_pos.x)][0] == self.opposite_color(self.color[0]):
                    attacked_pos.append(new_pos)
        defensed_pos.append(new_pos)
        
        return attacked_pos, defensed_pos
    
    def attack_king(self):
        return self.defensed_pos
    
    def move(self, new_pos):
        self.pos = new_pos
        self.moved = True

    def update_pos(self, game_config):
        self.attacked_pos, self.defensed_pos = self.get_pos(game_config)
    
    def update_valid(self, valid_moves):
        self.valid_moves = valid_moves
