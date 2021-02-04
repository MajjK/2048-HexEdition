# 2048-HexEdition
## General Info
The project is a hexagonal version of popular "2048" game. It's an expanded continuation of my university project. 
The game offers singleplayer mode(versus AI based on min-max algorithm), hot-seat mode for two players and multiplayer mode which offers possibility to play by LAN.

## Screenshots
![Menu_Screenshot](./img/menu.png?style=centerme) <br/>
![In-game_Screenshot](./img/in_game.png?style=centerme) <br/>
![In-game_Screenshot](./img/in_game_2.png?style=centerme) <br/>

## Technologies used
* Python 3.6 - Main language.
* PySide2 - Python module which provides access to the complete Qt 5.12+ framework. Used for GUI design and threading.
* socket - Python module for LAN networking interface.

## Features
* Singleplayer versus AI
* Hot-seat mode
* Scoreboards
* Saving/Loading game instance to/from .xml file - live replay
* Save your port/address configuration to a .json file

To do:
* Multiplayer mode - in progress
* Movement animation
* Layout improvement 

## Setup
Clone the repo, then install all required dependiences (You can do it by pip). Then just start "2048-HexEdition.py" 
