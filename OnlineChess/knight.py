import pygame
from pygame.math import Vector2

pygame.init()

class Knight():
    def __init__(self, pos, color, game_config):
        self.char = 'N'
        self.pos = pos
        self.color = color
        self.dir = [Vector2(1, -2), Vector2(2, -1), Vector2(2, 1), Vector2(1, 2), Vector2(-1, 2), Vector2(-2, 1), Vector2(-2, -1), Vector2(-1, -2)]
        self.attacked_pos, self.defensed_pos = self.get_pos(game_config)
        self.valid_moves = []

    def opposite_color(self, color):
        if color[0] == 'w':
            return 'b'
        return 'w'

    def get_pos(self, game_config):
        attacked_pos = []
        defensed_pos = []
        for d in self.dir:
            new_pos = self.pos + d
            if 0 <= new_pos.x < 8 and 0 <= new_pos.y < 8:
                if game_config[int(new_pos.y)][int(new_pos.x)] == '':
                    attacked_pos.append(new_pos)
                else:
                    if game_config[int(new_pos.y)][int(new_pos.x)][0] == self.opposite_color(self.color):
                        attacked_pos.append(new_pos)
                    if game_config[int(new_pos.y)][int(new_pos.x)][0] == self.color[0]:
                        defensed_pos.append(new_pos)
                        
        return attacked_pos, defensed_pos
    
    def attack_king(self):
        return self.attacked_pos + self.defensed_pos

    def move(self, new_pos):
        self.pos = new_pos

    def update_valid(self, valid_moves):
        self.valid_moves = valid_moves
    
    def update_pos(self, game_config):
        self.attacked_pos, self.defensed_pos = self.get_pos(game_config)