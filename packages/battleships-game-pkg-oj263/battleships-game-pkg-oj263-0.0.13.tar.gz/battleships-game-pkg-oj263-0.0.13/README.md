# Battleships Game

## Introduction
Welcome to the Battleships Game! This project is a Python-based implementation of the classic game Battleships, where players take turns to guess coordinates in order to sink the opponnets ships. 
The game supports single-player and multiplayer against an AI opponent.
To meet the assessment criteria I have:
 - Ensured fucntionality in single player, multiplayer and with the web interface
 - Tested my code using pytest and written aditional tests to cover all functions in components.py, game_engine.py and mp_game_engine.py
 - Used docstrings, comments, type hinting and suitable identifier names to ensure my code is easy to understand
 - Used pylint to check the styling of the code
To meet the stretch goals I have:
 - Added different options for placement algorithm in the place_battleships function. This includes a placement with random positions and orientations and a custom placement option that takes a json file as input.
 - Added options for difficulty in the generate attack function. This includes easy, medium and hard modes.
    - Easy: fires at a random location
    - Medium: If the last shot was a hit, it will attack a neighbour of the previous shot
    - Hard: looks through all previous shots that were a hit and checks if any of there neighbours have been hit, if they have then it works out the orientation and checks for valid neighbours of that orientation
 - Added a setup webpage to allow the user to select the difficulty and board size before being redirected to the placement page.
 - I have generated a detailed index.html file with Sphinx

## Prerequisites
Before you begin, ensure you have the following requirements:
- Python 3.11 or above. To install this, follow these steps:
    1. Go to this url: [https://www.python.org/downloads/windows/]
    2. Select downnload on the version of python you want to install
    3. Run the download installer.
- Flask 3.0. To install follow these steps:
    1. `pip install Flask`
- pytest 7.4. To install follow these steps:
    1. `pip install pytest`
    2. `pip install pytest-cov`
    3. `pip install pytest-depends`

## Installation
To install the Battleships Game, follow these steps:  
- `pip install battleships-game-pkg-oj263`

Or, if you have downloaded the source code:  
- `python setup.py install`

## Getting Started
To start playing the Battleships Game, run the following command within the battleships game directory:  
- `python game_engine.py`

For the version with an ai opponent, run this command:  
- `python mp_game_engine.py`

For the web based game with an ai opponent, run this command:

- `python main.py` then go to this url: <http://127.0.0.1:5000/setup>

Enter your difficulty and board size, then press submit and you will be redirected to the placement page.
Place your ships, then press send game and you will be directed to the main game page where you will play against the AI.
The first one to sink all the opponents ships is the winner.

## Testing
To run the tests for the Battleships Game, navigate to the project directory and run:  
- `pytest`

If this command doesn't work. Try this:
- `python -m pytest`

## Developer Documentation
The project package is seperated into four python modules:
1. components.py - this contains all the necessary features to be used in creating and setting up the game
2. game_engine.py - this contains the additional elements required to play a single player version of the game
3. mp_game_engine.py - this contains the additional elements required to play a multiplayer player version of the game
4. main.py - this contains the the functions that handle requests to and from the server for the web interface version of the game

## Details
- **Authors**: N/A
- **License**: This project is licensed under the MIT License - see the LICENSE file for details.
- **Acknowledgements**: A special thanks to Matt Collison and all Teaching Assistants for their help.

For more information and source code, please visit <https://github.com/ollyjohnson/battleships>.