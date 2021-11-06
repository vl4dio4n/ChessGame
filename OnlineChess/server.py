import socket
import pickle
import sys
from _thread import *
from game import Game
import time

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection. Sever Started")

connected = set()
games = {}
id_count = 0

def threaded_client(conn, p, game_id):
    conn.send(str.encode(str(p)))
    reply = ""
    pos = None
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 2))
            if game_id in games:
                game = games[game_id]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_game()
                    elif data == "time":
                        if game.player_turn == 0:     
                            game.white_time -= (int(time.time()) - int(game.last_tick)) 
                        else:
                            game.black_time -= (int(time.time()) - int(game.last_tick))
                        game.last_tick = time.time()
                    elif data != "get":
                        if game.player_turn == 0:     
                            game.white_time -= (int(time.time()) - int(game.last_tick)) 
                        else:
                            game.black_time -= (int(time.time()) - int(game.last_tick))
                        game.last_tick = time.time()
                        if type(data) == tuple:
                            print(f"Move {game.game_config[int(data[0].y)][int(data[0].x)]} from ({int(data[0].y)}, {int(data[0].x)}) at ({int(data[1].y)}, {int(data[1].x)})")
                            game.play(data[0], data[1])
                            pos = data[1]
                        else:
                            if data[0] == 'w':
                                game.promote_white_pawn(pos, data[1])
                            else:
                                game.promote_black_pawn(pos, data[1])
                    reply = game
                    try:
                        str_data = pickle.dumps(reply)
                    except Exception:
                        exc_type, value, traceback = sys.exc_info()
                        print("Failed with exception [%s]" % exc_type.__name__)
                    conn.sendall(str_data)
                    games[game_id] = game
            else:
                break
        except:
            break
    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game: ", game_id)
    except:
        pass
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        games[game_id].last_tick = time.time()
        p = 1
    
    start_new_thread(threaded_client, (conn, p, game_id))

