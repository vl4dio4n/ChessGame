import pygame
from pygame.math import Vector2
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen 
from king import King
import time

pygame.init()

class Game():
    def __init__(self, id, ready = False):
        self.game_config = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.value = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 10}

        self.white_deck = [Pawn(Vector2(0, 6), "white", self.game_config),
                            Pawn(Vector2(1, 6), "white", self.game_config),
                            Pawn(Vector2(2, 6), "white", self.game_config),
                            Pawn(Vector2(3, 6), "white", self.game_config),
                            Pawn(Vector2(4, 6), "white", self.game_config),
                            Pawn(Vector2(5, 6), "white", self.game_config),
                            Pawn(Vector2(6, 6), "white", self.game_config),
                            Pawn(Vector2(7, 6), "white", self.game_config),
                            Rook(Vector2(0, 7), "white", self.game_config),
                            Knight(Vector2(1, 7), "white", self.game_config),
                            Bishop(Vector2(2, 7), "white", self.game_config),
                            Queen(Vector2(3, 7), "white", self.game_config),
                            King(Vector2(4, 7), "white", self.game_config),
                            Bishop(Vector2(5, 7), "white", self.game_config),
                            Knight(Vector2(6, 7), "white", self.game_config),
                            Rook(Vector2(7, 7), "white", self.game_config)]
        self.white_captured = {'Q': 0, 'R': 0, 'N': 0, 'B': 0, 'P': 0}
        self.white_material = 40
        
        self.black_deck = [Pawn(Vector2(0, 1), "black", self.game_config),
                            Pawn(Vector2(1, 1), "black", self.game_config),
                            Pawn(Vector2(2, 1), "black", self.game_config),
                            Pawn(Vector2(3, 1), "black", self.game_config),
                            Pawn(Vector2(4, 1), "black", self.game_config),
                            Pawn(Vector2(5, 1), "black", self.game_config),
                            Pawn(Vector2(6, 1), "black", self.game_config),
                            Pawn(Vector2(7, 1), "black", self.game_config),
                            Rook(Vector2(0, 0), "black", self.game_config),
                            Knight(Vector2(1, 0), "black", self.game_config),
                            Bishop(Vector2(2, 0), "black", self.game_config),
                            Queen(Vector2(3, 0), "black", self.game_config),
                            King(Vector2(4, 0), "black", self.game_config),
                            Bishop(Vector2(5, 0), "black", self.game_config),
                            Knight(Vector2(6, 0), "black", self.game_config),
                            Rook(Vector2(7, 0), "black", self.game_config)]
        self.black_captured = {'Q': 0, 'R': 0, 'N': 0, 'B': 0, 'P': 0}
        self.black_material = 40
        self.ready = ready
        self.player_turn = 0
        self.id = id
        self.valid_pos_white()
        self.valid_pos_black()
        self.white_time = 900
        self.black_time = 900
        self.start_time = None 
        self.last_tick = None

    def find_danger_pos(self, deck):
        danger_pos = []
        for piece in deck:
            for pos in piece.attack_king():
               if pos not in danger_pos:
                   danger_pos.append(pos)
        return danger_pos
    
    def get_piece_index(self, deck, pos):
        for index, piece in enumerate(deck):
            if piece.pos == pos:
                return index
    
    def play(self, pos1, pos2):
        rocky = False
        color = 'w'
        if self.player_turn == 1:
            color = 'b'
        if self.game_config[int(pos2.y)][int(pos2.x)] != '':
            if self.game_config[int(pos2.y)][int(pos2.x)][0] == color:
                rocky = True

        if not rocky:
            x1 = int(pos1.x)
            y1 = int(pos1.y)
            x2 = int(pos2.x)
            y2 = int(pos2.y)

            if self.game_config[y2][x2] != '':
                if self.player_turn == 0:
                    index1 = self.get_piece_index(self.white_deck, pos1)
                    self.white_deck[index1].move(pos2)
                    self.white_captured[self.game_config[y2][x2][1]] += 1
                    self.black_material -= self.value[self.game_config[y2][x2][1]]
                    index2 = self.get_piece_index(self.black_deck, pos2)
                    self.black_deck.pop(index2)
                else:
                    index1 = self.get_piece_index(self.black_deck, pos1)
                    self.black_deck[index1].move(pos2)
                    self.black_captured[self.game_config[y2][x2][1]] += 1
                    self.white_material -= self.value[self.game_config[y2][x2][1]]
                    index2 = self.get_piece_index(self.white_deck, pos2)
                    self.white_deck.pop(index2)
            else:
                if self.player_turn == 0:
                    index1 = self.get_piece_index(self.white_deck, pos1)
                    self.white_deck[index1].move(pos2)
                else:
                    index1 = self.get_piece_index(self.black_deck, pos1)
                    self.black_deck[index1].move(pos2)
            self.game_config[y2][x2] = self.game_config[y1][x1]
            self.game_config[y1][x1] = ''
            if self.game_config[y2][x2][1] == 'P' and (y2 == 0 or y2 == 7):
                pass
            else:
                if self.player_turn == 0:
                    self.player_turn = 1
                else:
                    self.player_turn = 0
        else:
            _pos1 = Vector2((int(pos1.x) + int(pos2.x) + 1) // 2, pos1.y)
            _pos2 = Vector2((int(pos1.x) + int(pos2.x) + 1) // 2 + 1, pos1.y)
            if pos2.x == 7:
                _pos2 = Vector2((int(pos1.x) + int(pos2.x) + 1) // 2 - 1, pos1.y)
            if self.player_turn == 0:
                index1 = self.get_piece_index(self.white_deck, pos1)
                index2 = self.get_piece_index(self.white_deck, pos2)
                self.white_deck[index1].move(_pos1)
                self.white_deck[index2].move(_pos2)
            else:
                index1 = self.get_piece_index(self.black_deck, pos1)
                index2 = self.get_piece_index(self.black_deck, pos2)
                self.black_deck[index1].move(_pos1)
                self.black_deck[index2].move(_pos2)
            self.game_config[int(_pos1.y)][int(_pos1.x)] = self.game_config[int(pos1.y)][int(pos1.x)]
            self.game_config[int(pos1.y)][int(pos1.x)] = ''
            self.game_config[int(_pos2.y)][int(_pos2.x)] = self.game_config[int(pos2.y)][int(pos2.x)]
            self.game_config[int(pos2.y)][int(pos2.x)] = ''
            if self.player_turn == 0:
                self.player_turn = 1
            else:
                self.player_turn = 0
        
        for index in range(len(self.white_deck)):
            self.white_deck[index].update_pos(self.game_config)
        for index in range(len(self.black_deck)):
            self.black_deck[index].update_pos(self.game_config)
        
        self.valid_pos_white()
        self.valid_pos_black()

    def get_king_pos(self, deck):
        for piece in deck:
            if piece.char == 'K':
                return piece.pos

    def check_move_white(self, pos1, pos2):
        x1 = int(pos1.x)
        y1 = int(pos1.y)
        x2 = int(pos2.x)
        y2 = int(pos2.y)

        if self.game_config[y2][x2] != '':
            if self.game_config[y2][x2][1] == 'K':
                return False

        _game_config = []
        for item in self.game_config:
            _game_config.append(item.copy())

        _white_deck = []
        for item in self.white_deck:
            if item.char == 'P':
                _white_deck.append(Pawn(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'R':
                _white_deck.append(Rook(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'N':
                _white_deck.append(Knight(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'B':
                _white_deck.append(Bishop(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'Q':
                _white_deck.append(Queen(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'K':
                _white_deck.append(King(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
        
        _black_deck = []
        for item in self.black_deck:
            if item.char == 'P':
                _black_deck.append(Pawn(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'R':
                _black_deck.append(Rook(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'N':
                _black_deck.append(Knight(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'B':
                _black_deck.append(Bishop(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'Q':
                _black_deck.append(Queen(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'K':
                _black_deck.append(King(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
        
        if _game_config[y2][x2] != '':
            index1 = self.get_piece_index(_white_deck, pos1)
            _white_deck[index1].move(pos2)
            index2 = self.get_piece_index(_black_deck, pos2)
            _black_deck.pop(index2)
        else:
            index1 = self.get_piece_index(_white_deck, pos1)
            _white_deck[index1].move(pos2)
        _game_config[y2][x2] = _game_config[y1][x1]
        _game_config[y1][x1] = ''
        
        for index in range(len(_white_deck)):
            _white_deck[index].update_pos(_game_config)
        for index in range(len(_black_deck)):
            _black_deck[index].update_pos(_game_config)

        danger_for_white_king = self.find_danger_pos(_black_deck)
        king_pos = self.get_king_pos(_white_deck)
        return not(king_pos in danger_for_white_king)
    
    def check_small_rocky_white(self):
        if self.game_config[7][4] != 'wK' or self.game_config[7][7] != 'wR':
            return False
        k_index = self.get_piece_index(self.white_deck, Vector2(4, 7))
        r_index = self.get_piece_index(self.white_deck, Vector2(7, 7))
        if self.white_deck[k_index].moved or self.white_deck[r_index].moved:
            return False
        danger_for_white_king = self.find_danger_pos(self.black_deck)
        for col in range(4, 8):
            pos = Vector2(col, 7)
            if pos in danger_for_white_king:
                return False
            if self.game_config[7][col] != '' and 5 <= col <= 6:
                return False
        return True

    def check_big_rocky_white(self):
        if self.game_config[7][4] != 'wK' or self.game_config[7][0] != 'wR':
            return False
        k_index = self.get_piece_index(self.white_deck, Vector2(4, 7))
        r_index = self.get_piece_index(self.white_deck, Vector2(0, 7))
        if self.white_deck[k_index].moved or self.white_deck[r_index].moved:
            return False
        danger_for_white_king = self.find_danger_pos(self.black_deck)
        for col in range(0, 5):
            pos = Vector2(col, 7)
            if pos in danger_for_white_king:
                return False
            if self.game_config[7][col] != '' and 1 <= col <= 3:
                return False
        return True 

    def valid_pos_white(self):
        for index, piece in enumerate(self.white_deck):
            valid_moves = []
            for pos in piece.attacked_pos:
                if self.check_move_white(piece.pos, pos):
                    valid_moves.append(pos)
            
            if piece.char == 'K':
                if self.check_small_rocky_white():
                    valid_moves.append(Vector2(7, 7))
                if self.check_big_rocky_white():
                    valid_moves.append(Vector2(0, 7))
            
            self.white_deck[index].update_valid(valid_moves)

    def check_move_black(self, pos1, pos2):

        x1 = int(pos1.x)
        y1 = int(pos1.y)
        x2 = int(pos2.x)
        y2 = int(pos2.y)

        if self.game_config[y2][x2] != '':
            if self.game_config[y2][x2][1] == 'K':
                return False
        
        _game_config = []
        for item in self.game_config:
            _game_config.append(item.copy())

        _white_deck = []
        for item in self.white_deck:
            if item.char == 'P':
                _white_deck.append(Pawn(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'R':
                _white_deck.append(Rook(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'N':
                _white_deck.append(Knight(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'B':
                _white_deck.append(Bishop(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'Q':
                _white_deck.append(Queen(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
            elif item.char == 'K':
                _white_deck.append(King(Vector2(item.pos.x, item.pos.y), "white", self.game_config))
        
        _black_deck = []
        for item in self.black_deck:
            if item.char == 'P':
                _black_deck.append(Pawn(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'R':
                _black_deck.append(Rook(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'N':
                _black_deck.append(Knight(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'B':
                _black_deck.append(Bishop(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'Q':
                _black_deck.append(Queen(Vector2(item.pos.x, item.pos.y), "black", self.game_config))
            elif item.char == 'K':
                _black_deck.append(King(Vector2(item.pos.x, item.pos.y), "black", self.game_config))

        if _game_config[y2][x2] != '':
            index1 = self.get_piece_index(_black_deck, pos1)
            _black_deck[index1].move(pos2)
            index2 = self.get_piece_index(_white_deck, pos2)
            _white_deck.pop(index2)
        else:
            index1 = self.get_piece_index(_black_deck, pos1)
            _black_deck[index1].move(pos2)
        _game_config[y2][x2] = _game_config[y1][x1]
        _game_config[y1][x1] = ''

        for index in range(len(_white_deck)):
            _white_deck[index].update_pos(_game_config)
        for index in range(len(_black_deck)):
            _black_deck[index].update_pos(_game_config)

        danger_for_black_king = self.find_danger_pos(_white_deck)
        king_pos = self.get_king_pos(_black_deck)
        return not(king_pos in danger_for_black_king)
    
    def check_small_rocky_black(self):
        if self.game_config[0][4] != 'bK' or self.game_config[0][7] != 'bR':
            return False

        k_index = self.get_piece_index(self.black_deck, Vector2(4, 0))
        r_index = self.get_piece_index(self.black_deck, Vector2(7, 0))
        if self.black_deck[k_index].moved or self.black_deck[r_index].moved:
            return False

        danger_for_black_king = self.find_danger_pos(self.white_deck)
        for col in range(4, 8):
            pos = Vector2(col, 0)
            if pos in danger_for_black_king:
                return False
            if self.game_config[0][col] != '' and 5 <= col <= 6:
                return False

        return True

    def check_big_rocky_black(self):
        if self.game_config[0][4] != 'bK' or self.game_config[0][0] != 'bR':
            return False
        k_index = self.get_piece_index(self.black_deck, Vector2(4, 0))
        r_index = self.get_piece_index(self.black_deck, Vector2(0, 0))
        if self.black_deck[k_index].moved or self.black_deck[r_index].moved:
            return False
        danger_for_black_king = self.find_danger_pos(self.white_deck)
        for col in range(0, 5):
            pos = Vector2(col, 0)
            if pos in danger_for_black_king:
                return False
            if self.game_config[0][col] != '' and 1 <= col <= 3:
                return False
        return True    

    def valid_pos_black(self):
        for index, piece in enumerate(self.black_deck):
            valid_moves = []
            for pos in piece.attacked_pos:
                if self.check_move_black(piece.pos, pos):
                    valid_moves.append(pos)

            if piece.char == 'K':
                if self.check_small_rocky_black():
                    valid_moves.append(Vector2(7, 0))
                if self.check_big_rocky_black():
                    valid_moves.append(Vector2(0, 0))
            
            self.black_deck[index].update_valid(valid_moves)
            
    
    def checkmate_white(self):
        king_pos = self.get_king_pos(self.white_deck)
        king_index = self.get_piece_index(self.white_deck, king_pos)
        danger_for_white_king = self.find_danger_pos(self.black_deck)
        possible_moves = 0
        for piece in self.white_deck:
            possible_moves += len(piece.valid_moves) 
        return possible_moves == 0 and king_pos in danger_for_white_king 
    
    def pat_white(self):
        if self.player_turn == 1:
            return False
        king_pos = self.get_king_pos(self.white_deck)
        king_index = self.get_piece_index(self.white_deck, king_pos)
        danger_for_white_king = self.find_danger_pos(self.black_deck)
        possible_moves = 0
        for piece in self.white_deck:
            possible_moves += len(piece.valid_moves) 
        return len(self.white_deck[king_index].valid_moves) == 0 and king_pos not in danger_for_white_king and possible_moves == 0 
    
    def checkmate_black(self):
        king_pos = self.get_king_pos(self.black_deck)
        king_index = self.get_piece_index(self.black_deck, king_pos)
        danger_for_black_king = self.find_danger_pos(self.white_deck)
        possible_moves = 0
        for piece in self.black_deck:
            possible_moves += len(piece.valid_moves) 
        return possible_moves == 0 and king_pos in danger_for_black_king
    
    def pat_black(self):
        if self.player_turn == 0:
            return False
        king_pos = self.get_king_pos(self.black_deck)
        king_index = self.get_piece_index(self.black_deck, king_pos)
        danger_for_black_king = self.find_danger_pos(self.white_deck)
        possible_moves = 0
        for piece in self.black_deck:
            possible_moves += len(piece.valid_moves) 
        return len(self.black_deck[king_index].valid_moves) == 0 and king_pos not in danger_for_black_king and possible_moves == 0 
    
    def winner(self):
        winner = -2

        if self.white_time == 0:
            winner = 1
        elif self.black_time == 0:
            winner = 0

        if self.pat_white() or self.pat_black():
            winner = -1
        elif self.checkmate_white():
            winner = 1
        elif self.checkmate_black():
            winner = 0
        return winner

    def promote_white_pawn(self, pos, char):
        index = self.get_piece_index(self.white_deck, pos)
        self.game_config[int(pos.y)][int(pos.x)] = 'w' + char
        self.white_deck.pop(index)
        if char == 'P':
            self.white_deck.append(Pawn(pos, "white", self.game_config))
        elif char == 'R':
            self.white_deck.append(Rook(pos, "white", self.game_config))
        elif char == 'N':
            self.white_deck.append(Knight(pos, "white", self.game_config))
        elif char == 'B':
            self.white_deck.append(Bishop(pos, "white", self.game_config))
        elif char == 'Q':
            self.white_deck.append(Queen(pos, "white", self.game_config))
        self.player_turn = 1
        self.white_material += (self.value[char] - 1)
        for index in range(len(self.white_deck)):
            self.white_deck[index].update_pos(self.game_config)
        for index in range(len(self.black_deck)):
            self.black_deck[index].update_pos(self.game_config)
        
        self.valid_pos_white()
        self.valid_pos_black()
    
    def promote_black_pawn(self, pos, char):
        index = self.get_piece_index(self.black_deck, pos)
        self.game_config[int(pos.y)][int(pos.x)] = 'b' + char
        self.black_deck.pop(index)
        if char == 'P':
            self.black_deck.append(Pawn(pos, "black", self.game_config))
        elif char == 'R':
            self.black_deck.append(Rook(pos, "black", self.game_config))
        elif char == 'N':
            self.black_deck.append(Knight(pos, "black", self.game_config))
        elif char == 'B':
            self.black_deck.append(Bishop(pos, "black", self.game_config))
        elif char == 'Q':
            self.black_deck.append(Queen(pos, "black", self.game_config))
        self.black_material += (self.value[char] - 1)
        self.player_turn = 0

        for index in range(len(self.white_deck)):
            self.white_deck[index].update_pos(self.game_config)
        for index in range(len(self.black_deck)):
            self.black_deck[index].update_pos(self.game_config)
        
        self.valid_pos_white()
        self.valid_pos_black()
    
    def reset_game(self):
        self.game_config = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.value = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 10}

        self.white_deck = [Pawn(Vector2(0, 6), "white", self.game_config),
                            Pawn(Vector2(1, 6), "white", self.game_config),
                            Pawn(Vector2(2, 6), "white", self.game_config),
                            Pawn(Vector2(3, 6), "white", self.game_config),
                            Pawn(Vector2(4, 6), "white", self.game_config),
                            Pawn(Vector2(5, 6), "white", self.game_config),
                            Pawn(Vector2(6, 6), "white", self.game_config),
                            Pawn(Vector2(7, 6), "white", self.game_config),
                            Rook(Vector2(0, 7), "white", self.game_config),
                            Knight(Vector2(1, 7), "white", self.game_config),
                            Bishop(Vector2(2, 7), "white", self.game_config),
                            Queen(Vector2(3, 7), "white", self.game_config),
                            King(Vector2(4, 7), "white", self.game_config),
                            Bishop(Vector2(5, 7), "white", self.game_config),
                            Knight(Vector2(6, 7), "white", self.game_config),
                            Rook(Vector2(7, 7), "white", self.game_config)]
        self.white_captured = {'Q': 0, 'R': 0, 'N': 0, 'B': 0, 'P': 0}
        self.white_material = 40
        
        self.black_deck = [Pawn(Vector2(0, 1), "black", self.game_config),
                            Pawn(Vector2(1, 1), "black", self.game_config),
                            Pawn(Vector2(2, 1), "black", self.game_config),
                            Pawn(Vector2(3, 1), "black", self.game_config),
                            Pawn(Vector2(4, 1), "black", self.game_config),
                            Pawn(Vector2(5, 1), "black", self.game_config),
                            Pawn(Vector2(6, 1), "black", self.game_config),
                            Pawn(Vector2(7, 1), "black", self.game_config),
                            Rook(Vector2(0, 0), "black", self.game_config),
                            Knight(Vector2(1, 0), "black", self.game_config),
                            Bishop(Vector2(2, 0), "black", self.game_config),
                            Queen(Vector2(3, 0), "black", self.game_config),
                            King(Vector2(4, 0), "black", self.game_config),
                            Bishop(Vector2(5, 0), "black", self.game_config),
                            Knight(Vector2(6, 0), "black", self.game_config),
                            Rook(Vector2(7, 0), "black", self.game_config)]
        self.black_captured = {'Q': 0, 'R': 0, 'N': 0, 'B': 0, 'P': 0}
        self.black_material = 40
        self.ready = True
        self.player_turn = 0
        self.valid_pos_white()
        self.valid_pos_black()
        self.white_time = 900
        self.black_time = 900
        self.last_tick = time.time()

    def connected(self):
        return self.ready