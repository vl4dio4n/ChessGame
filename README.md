# 🚀 ChessGame
## About the Game
An online chess game created in python using the **_pygame_** package.  
In order to play this game, the players need to be connected to the same LAN as the server the game is being run on.

## Game Controls
The player who is to move must first select a chessman and then click on the position where he wants to go.
If the palyer wants to move another chessman than the one selected, he can undo the selection by simply clicking on any square of the board that is not highligted.
When a pawn reaches the opposite end of the board an options bar will appear on top of the game's window with the promotion possibilities. Just click on the one you wish.  

## Usage
Before playing, make sure you have the **_pygame_** package installed. </br>
In order to do this, just type in a terminal the following command: </br>
```bash
pip install pygame
```
After that, the server must be started on a machine. Type this in a terminal opened in the <a href = "OnlineChess"> **project's folder** </a>:
```bash
python server.py
```
Next, players can start to connect to the server by running this command also in a terminal opened in the <a href = "OnlineChess"> **project's folder** </a>:
```bash
python client.py
```
Note that after connecting to ther server the player must wait until an opponent is found.

## Sneek Peeks
- Chessboard at the beginning </br> <img width="600" alt="chessgame-start" src="https://user-images.githubusercontent.com/93842197/149680061-1c83d9cb-6404-44f3-abb9-b5041982bd49.png">
- Moving options highlighted </br> <img width="600" alt="chessgame-move-options" src="https://user-images.githubusercontent.com/93842197/149680074-9cf79c51-661f-4f31-b742-9b987fe0a649.png">
- Eating a chessman </br> <img width="600" alt="chessgame-eating" src="https://user-images.githubusercontent.com/93842197/149680082-41bd0469-9a20-4727-82fc-6213d01df649.png">
- Before castling </br> <img width="600" alt="chessgame-before-castling" src="https://user-images.githubusercontent.com/93842197/149680090-66c09725-61ad-4e48-a3bc-d8a8bd8e8ac8.png">
- After castling </br> <img width="600" alt="chessgame-after-castling" src="https://user-images.githubusercontent.com/93842197/149680097-fe6f3806-eabf-4e3f-bc84-0d84cc9fa7fd.png">
- Before promoting a pawn </br> <img width="600" alt="chessgame-before-promoting" src="https://user-images.githubusercontent.com/93842197/149680101-dbc641ff-4070-445c-a266-618dca44795d.png">
- After promoting a pawn </br> <img width="600" alt="chessgame-after-promoting" src="https://user-images.githubusercontent.com/93842197/149680108-11ac8395-8a4a-4da7-98ce-7ff0ecccbddd.png">
- Player wins </br> <img width="600" alt="chessgame-player-wins" src="https://user-images.githubusercontent.com/93842197/149680114-3fcaae62-59a2-40c0-9115-1f1b85386907.png">

***
<p align = "center"> (<a href = "#top">Back to Top</a>) </p> 
