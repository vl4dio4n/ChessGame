import pygame
from pygame.math import Vector2

pygame.init()

class Queen():
    def __init__(self, pos, color, game_config):
        self.char = 'Q'
        self.pos = pos #Vector2
        self.color = color
        self.attacked_pos, self.defensed_pos = self.get_pos(game_config)
        self.valid_moves = []

    def opposite_color(self, color):
        if color[0] == 'w':
            return 'b'
        return 'w'

    def get_pos(self, game_config):
        attacked_pos = []
        defensed_pos = [] 
        row = int(self.pos.y)
        for col in range(int(self.pos.x) + 1, 8):
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
        col = int(self.pos.x) - 1
        while col >= 0:
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
            col -= 1

        col = int(self.pos.x)
        for row in range(int(self.pos.y) + 1, 8):
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
        row = int(self.pos.y) - 1
        while row >= 0:
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
            row -= 1

        col = int(self.pos.x) - 1
        row = int(self.pos.y) - 1
        while col >= 0 and row >= 0:
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
            col -= 1
            row -= 1
        col = int(self.pos.x) + 1
        row = int(self.pos.y) - 1
        while col < 8 and row >= 0:
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
            col += 1
            row -= 1

        col = int(self.pos.x) - 1
        row = int(self.pos.y) + 1
        while col >= 0 and row < 8:
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
            col -= 1
            row += 1

        col = int(self.pos.x) + 1
        row = int(self.pos.y) + 1
        while col < 8 and row < 8:
            if game_config[row][col] == '':
                attacked_pos.append(Vector2(col, row))
            else:
                if game_config[row][col][0] == self.opposite_color(self.color):
                    attacked_pos.append(Vector2(col, row))
                if game_config[row][col][0] == self.color[0]:
                    defensed_pos.append(Vector2(col, row))
                break
            col += 1
            row += 1

        return attacked_pos, defensed_pos
    
    def attack_king(self):
        return self.attacked_pos + self.defensed_pos

    def update_pos(self, game_config):
        self.attacked_pos, self.defensed_pos = self.get_pos(game_config)

    def move(self, new_pos):
        self.pos = new_pos

    def update_valid(self, valid_moves):
        self.valid_moves = valid_moves
