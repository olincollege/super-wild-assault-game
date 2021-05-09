# S.W.A.G. - Super Wild Assault Game
## Jacob Smilg and Melissa Kazazic
## Summary

S.W.A.G. is a simple, customizable platform fighter engine. Two players are spawned in at the start of the game, and they fight until one player's health bar is reduced to zero. The main inspiration for the customization is M.U.G.E.N. — it is designed such that new characters can be added with relative ease. Two existing characters, Olin Man and Catboy, are included as playable examples. More information on character customization can be found on the [website](https://olincollege.github.io/super-wild-assault-game/).

## How to use
### Dependencies
The only module needed to run S.W.A.G. is `pygame` version 2.0 or greater, which can be installed with `pip install pygame`. Alternatively, it can be installed with  `pip install -r requirements.txt` after cloning this repository to your computer.

### Running the game
The game can be opened by running `swag_game.py` with Python.

### Controls
Currently, the controls are very simple, as the included characters only have a few actions: move, jump, jab, and block. If a new move is added, it needs to be bound to a key by changing the dictionary `keybinds` in `swag_input_handler.py`. The default keybinds can be changed this way too.

Player 1:
* Arrow keys to move (up is jump)
* . to jab
* , to block

Player 2:
* WASD to move (W is jump)
* C to jab
* V to block
