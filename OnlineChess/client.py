import pygame
from pygame.math import Vector2
from network import Network
import time

pygame.init()
width = 650
height = 650
cell_width = 60
cell_height = 60
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pieces = {}
pieces['wR'] = pygame.image.load("Graphics\\white_rook.png")
pieces['wN'] = pygame.image.load("Graphics\\white_knight.png")
pieces['wB'] = pygame.image.load("Graphics\\white_bishop.png")
pieces['wQ'] = pygame.image.load("Graphics\\white_queen.png")
pieces['wK'] = pygame.image.load("Graphics\\white_king.png")
pieces['wP'] = pygame.image.load("Graphics\\white_pawn.png")

pieces['bR'] = pygame.image.load("Graphics\\black_rook.png")
pieces['bN'] = pygame.image.load("Graphics\\black_knight.png")
pieces['bB'] = pygame.image.load("Graphics\\black_bishop.png")
pieces['bQ'] = pygame.image.load("Graphics\\black_queen.png")
pieces['bK'] = pygame.image.load("Graphics\\black_king.png")
pieces['bP'] = pygame.image.load("Graphics\\black_pawn.png")

s = ['P', 'R', 'N', 'B', 'Q']

for key in pieces.keys():
    pieces[key] = pygame.transform.scale(pieces[key], (cell_width, cell_height))

class SpecialButton():
    def __init__(self, char, x , y):
        self.char = char
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

class Button():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.width = cell_width
        self.height = cell_height
        self.x = 85 + self.col * self.width
        self.y = 85 + self.row * self.height

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

def check_btn(btns, row, col):
    if btns != None:
        for btn in btns:
            if btn.row == row and btn.col == col:
                return True
    return False

def redraw_window(win, game, player, btns, _btns):
    win.fill((0, 77, 26))
    if not game.connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", True, (255, 0 , 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        if player == 0:
            for row in range(8):
                for col in range(8):
                    if (row + col) % 2 == 0:
                        color = (255, 221, 153)
                    else:
                        color = (204, 68, 0)
                    cell_rect = (85 + col * cell_width, 85 + row * cell_height, cell_width, cell_height)
                    pygame.draw.rect(win, color, cell_rect)
            for piece in game.white_deck:
                cell_rect = (85 + piece.pos.x * cell_width, 85 + piece.pos.y * cell_height, cell_width, cell_height)
                win.blit(pieces[piece.color[0] + piece.char], cell_rect)
            for piece in game.black_deck:
                cell_rect = (85 + piece.pos.x * cell_width, 85 + piece.pos.y * cell_height, cell_width, cell_height)
                win.blit(pieces[piece.color[0] + piece.char], cell_rect)
            if btns != None:
                for btn in btns:
                    cell_rect = (btn.x, btn.y, btn.width, btn.height)
                    pygame.draw.rect(win, (0, 0, 0), cell_rect, 5)
            
            font = pygame.font.SysFont("comicsans", 15)
            for i in range(0, 8):
                text = font.render(str(8 - i), True, (77, 25, 0))
                win.blit(text, (60, 110 + i * 60))
                win.blit(text, (580, 110 + i * 60))
            for i, letter in enumerate("abcdefgh"):
                text = font.render(letter, True, (77, 25, 0))
                win.blit(text, (110 + i * 60, 60))
                win.blit(text, (110 + i * 60, 570))

            if _btns != None:
                for _btn in _btns:
                    cell_rect = (_btn.x, _btn.y, _btn.width, _btn.height)
                    pygame.draw.rect(win, (76, 230, 0), cell_rect)
                    win.blit(pygame.transform.scale(pieces[_btn.char], (_btn.width, _btn.height)), cell_rect)
                    pygame.draw.rect(win, (0, 0, 0), cell_rect, 3)

            index = 0
            for key in game.white_captured.keys():
                for _ in range(game.white_captured[key]):
                    cell_rect = (85 + index * 25, 585, 35, 35)
                    win.blit(pygame.transform.scale(pieces['b' + key], (35, 35)), cell_rect)
                    index += 1     
            font = pygame.font.SysFont("comicsans", 15)    
            if game.white_material > game.black_material:
                text = font.render('+' + str(game.white_material - game.black_material), True, (26, 13, 0))
                win.blit(text, (85 + index * 25 + 5, 595))
            index = 0
            for key in game.black_captured.keys():
                for _ in range(game.black_captured[key]):
                    cell_rect = (85 + index * 25, 25, 35, 35)
                    win.blit(pygame.transform.scale(pieces['w' + key], (35, 35)), cell_rect)
                    index += 1 
            if game.white_material < game.black_material:
                text = font.render('+' + str(game.black_material - game.white_material), True, (26, 13, 0))
                win.blit(text, (85 + index * 25 + 5, 35))

            #(x, y) = (600, 35)
            font = pygame.font.SysFont("comicsans", 20)
            white_mins = int(game.white_time // 60)
            white_secs = game.white_time % 60
            if white_secs >= 10:
                text = font.render(str(white_mins) + ':' + str(white_secs), True, (26, 13, 0))
            else:
                text = font.render(str(white_mins) + ':0' + str(white_secs), True, (26, 13, 0))
            win.blit(text, (550, 595)) 
    
            black_mins = int(game.black_time // 60)
            black_secs = game.black_time % 60
            if black_secs >= 10:
                text = font.render(str(black_mins) + ':' + str(black_secs), True, (26, 13, 0))
            else:
                text = font.render(str(black_mins) + ':0' + str(black_secs), True, (26, 13, 0))
            win.blit(text, (550, 35)) 
        
        else:
            for row in range(8):
                for col in range(8):
                    if (row + col) % 2 == 0:
                        color = (255, 221, 153)
                    else:
                        color = (204, 68, 0)
                    cell_rect = (85 + col * cell_width, 85 + row * cell_height, cell_width, cell_height)
                    pygame.draw.rect(win, color, cell_rect)
            for piece in game.white_deck:
                cell_rect = (85 + (7 - piece.pos.x) * cell_width, 85 + (7 - piece.pos.y) * cell_height, cell_width, cell_height)
                win.blit(pieces[piece.color[0] + piece.char], cell_rect)
            for piece in game.black_deck:
                cell_rect = (85 + (7 - piece.pos.x) * cell_width, 85 + (7 - piece.pos.y) * cell_height, cell_width, cell_height)
                win.blit(pieces[piece.color[0] + piece.char], cell_rect)
            if btns != None:
                for btn in btns:
                    cell_rect = (btn.x, btn.y, btn.width, btn.height)
                    pygame.draw.rect(win, (0, 0, 0), cell_rect, 5)
            
            font = pygame.font.SysFont("comicsans", 15)
            for i in range(0, 8):
                text = font.render(str(i + 1), True, (77, 25, 0))
                win.blit(text, (60, 110 + i * 60))
                win.blit(text, (580, 110 + i * 60))
            for i, letter in enumerate("abcdefgh"):
                text = font.render(letter, True, (77, 25, 0))
                win.blit(text, (110 + (7 - i) * 60, 60))
                win.blit(text, (110 + (7 - i) * 60, 570))

            if _btns != None:
                for _btn in _btns:
                    cell_rect = (_btn.x, _btn.y, _btn.width, _btn.height)
                    pygame.draw.rect(win, (76, 230, 0), cell_rect)
                    win.blit(pygame.transform.scale(pieces[_btn.char], (_btn.width, _btn.height)), cell_rect)
                    pygame.draw.rect(win, (0, 0, 0), cell_rect, 3)

            index = 0
            for key in game.white_captured.keys():
                for _ in range(game.white_captured[key]):
                    cell_rect = (85 + index * 25, 25, 35, 35)
                    win.blit(pygame.transform.scale(pieces['b' + key], (35, 35)), cell_rect)
                    index += 1     
            font = pygame.font.SysFont("comicsans", 15)    
            if game.white_material > game.black_material:
                text = font.render('+' + str(game.white_material - game.black_material), True, (26, 13, 0))
                win.blit(text, (85 + index * 25 + 5, 35))
            index = 0
            for key in game.black_captured.keys():
                for _ in range(game.black_captured[key]):
                    cell_rect = (85 + index * 25, 585, 35, 35)
                    win.blit(pygame.transform.scale(pieces['w' + key], (35, 35)), cell_rect)
                    index += 1 
            if game.white_material < game.black_material:
                text = font.render('+' + str(game.black_material - game.white_material), True, (26, 13, 0))
                win.blit(text, (85 + index * 25 + 5, 595))
            
            font = pygame.font.SysFont("comicsans", 20)
            white_mins = int(game.white_time // 60)
            white_secs = game.white_time % 60
            if white_secs >= 10:
                text = font.render(str(white_mins) + ':' + str(white_secs), True, (26, 13, 0))
            else:
                text = font.render(str(white_mins) + ':0' + str(white_secs), True, (26, 13, 0))
            win.blit(text, (550, 35)) 
    
            black_mins = int(game.black_time // 60)
            black_secs = game.black_time % 60
            if black_secs >= 10:
                text = font.render(str(black_mins) + ':' + str(black_secs), True, (26, 13, 0))
            else:
                text = font.render(str(black_mins) + ':0' + str(black_secs), True, (26, 13, 0))
            win.blit(text, (550, 595))
        

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_player())
    print("You are player ", player)
    
    btns = []
    _btns = []
    pos = None
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            #print('Hey ' + type(game))
        except:
            run = False
            print("Couldn't get game")
            break
        
        white_btns = []
        black_btns = []
        for piece in game.white_deck:
            white_btns.append(Button(piece.pos.y, piece.pos.x))
        for piece in game.black_deck:
            black_btns.append(Button(7 - piece.pos.y, 7 - piece.pos.x))
        
        if game.connected():
            redraw_window(win, game, player, btns, _btns)
            font = pygame.font.SysFont("comicsans", 90)
            winner = game.winner()
            if (winner == 1 and player == 1) or (winner == 0 and player == 0):
                text = font.render("You Won!", True, (255, 0, 0))
            elif winner == -1:
                text = font.render("Tie Game!", True, (255, 0, 0))
            elif (winner ==  1 and player == 0) or (winner == 0 and player == 1):
                text = font.render("You Lost...", True, (255, 0 , 0))
            else:
                text = None
            if text != None:
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(3000)
            
            if winner == -2: 
                try:
                    game = n.send("time")
                except:
                    run = False
                    print("Why I couldn't get the game?!")
                    break
            
            if winner != -2:
                try:
                    game = n.send("reset")
                    print(type(game))
                except:
                    run = False
                    print("Couldn't get game")
                    break
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.connected() and player == game.player_turn:
                    mouse_pos = pygame.mouse.get_pos()
                    found = False
                    if player == 0:
                        if _btns == []:
                            for btn in white_btns:
                                ok = True
                                for _btn in btns:
                                    if btn.row == _btn.row and btn.col == _btn.col:
                                        ok = False
                                redraw_window(win, game, player, btns, _btns)
                                if btn.click(mouse_pos) and ok:
                                    pos = Vector2(btn.col, btn.row)
                                    index = game.get_piece_index(game.white_deck, pos)
                                    piece = game.white_deck[index]
                                    found = True
                                    btns = []
                                    for valid_move in piece.valid_moves:
                                        btns.append(Button(valid_move.y, valid_move.x))
                            redraw_window(win , game, player, btns, _btns)
                            
                            for btn in btns:
                                redraw_window(win, game, player, btns, _btns)
                                if btn.click(mouse_pos):
                                    n.send((pos, Vector2(btn.col, btn.row)))
                                    if btn.row == 0 and game.game_config[int(pos.y)][int(pos.x)][1] == 'P':
                                        for index in range(5):
                                            _btns.append(SpecialButton('w' + s[index], width / 2 - 100 + index * 40, 60))
                                    btns = []
                                    break
                            
                            redraw_window(win, game, player, btns, _btns)
                            
                            if found == False:
                                btns = []
                                pos = None    
                        else:
                            redraw_window(win, game, player, btns, _btns)
                            for _btn in _btns:
                                if _btn.click(mouse_pos):
                                    n.send(_btn.char)
                                    _btns = [] 
                        
                    else:
                        if _btns == []:
                            for btn in black_btns:
                                ok = True
                                for _btn in btns:
                                    if btn.row == _btn.row and btn.col == _btn.col:
                                        ok = False
                                redraw_window(win, game, player, btns, _btns)
                                if btn.click(mouse_pos) and ok:
                                    pos = Vector2(7 - btn.col, 7 - btn.row)
                                    index = game.get_piece_index(game.black_deck, pos)
                                    piece = game.black_deck[index]
                                    found = True
                                    btns = []
                                    for valid_move in piece.valid_moves:
                                        btns.append(Button(7 - valid_move.y, 7 - valid_move.x))
                            redraw_window(win , game, player, btns, _btns)
                            
                            for btn in btns:
                                redraw_window(win, game, player, btns, _btns)
                                if btn.click(mouse_pos):
                                    n.send((pos, Vector2(7 - btn.col, 7 - btn.row)))
                                    if btn.row == 0 and game.game_config[int(pos.y)][int(pos.x)][1] == 'P':
                                        for index in range(5):
                                            _btns.append(SpecialButton('b' + s[index], width / 2 - 100 + index * 40, 60))
                                    btns = []
                                    break

                            redraw_window(win, game, player, btns, _btns)
                            
                            if found == False:
                                btns = []
                                pos = None
                        else:
                            redraw_window(win, game, player, btns, _btns)
                            for _btn in _btns:
                                if _btn.click(mouse_pos):
                                    n.send(_btn.char)
                                    _btns = [] 

        redraw_window(win, game, player, btns, _btns)

main()
