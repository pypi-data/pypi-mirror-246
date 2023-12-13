# ECM1400 Battleships

## Introduction
A python application to simulate a Battleships game against an AI in both a command line interface and a Flask GUI.

## Coursework Self assessment
All features required by specification are complete (including testing & logging)
### Additional 
#### Entry Screen
The user can select the game settings (size, difficulty) on an Entry page.
Game screen has a return to menu button so games can be replayed
#### Storm Mode
When this is turned on The board will shift 1 space each turn in a predetermined direction
#### HTML Template Sunken ships
If a ship has been sunk, the main.py script sends a list of sunk positions for
either the AI or Player to the HTML code, and it colours those tiles green
#### Other Frontend modifications
In the placement HTML file originally allowed users to place fewer than required number of ships. This was fixed.
#### Storm mode
To make it a more challenging if you select storm mode the player's board will shift one space each turn. Since the HTML
grid isn't persistent this had to be coded in javascript
#### AI attacking
There are 5 AI difficulties [code here](battleships/advanced_ai.py)
0. Pure Random Guessing
1. Random but it won't guess same space twice
2. Guessing a random position around unsunk hits
3. Trying to guess in a line around unsunk hits
4. Guesses in a line if there are unsunk hits, if none it calculates the probability of a ship being in any 
unguessed tile and guesses there

Wrote [a script](battleships/ai_comparison.py) to test AI's against each other

<img src="Images/AI scoring 2.png" alt="drawing" width="500"/>
<img src="Images/AI scoring image.png" alt="drawing" width="500"/> 

## Prerequisites
- Flask must be installed ```pip install Flask```
- numpy must be installed ```pip install numpy```
- For testing pytest must be installed ```pip install pytest``` 
- Pytest plugins must be installed```pip install pytest-depends``` ```pip install pytest-cov```
- Python version must be ≥ 3.10 due to ```|``` symbol in typehinting

_Version used in running = Python 3.11.4_

## Developer Documentation
All documentation for source code [can be found here](docs/_build/html/index.html)

In general
- [Components.py](battleships/components.py): Contains the basic functions for creating Battleships games
- [game_engine.py](battleships/game_engine.py): Contains functions to run a single player game and to run a single player game
- [mp_game_engine.py](battleships/mp_game_engine.py): Contains functions needed for multiplayer games (against AI)
- [main.py](battleships/main.py): Contains the framework needed for a Flask GUI game
- [advanced_ai.py](battleships/advanced_ai.py): Contains the functions needed for the extension 5 versions of AI
- [ai_comparison.py](battleships/ai_comparison.py): Contains functions to compare different versions of AI difficulties

## Testing
If pytest & plugins are installed then you can test in 2 ways.

_Note scripts like game_engine.py, mp_game_engine and main.py don't have full coverage as some functions require input statements which
my unittests were not intended to mock_
1. Use an IDE like PyCharm to run the tests manually
2. Navigate to the tests folder in the project (from the root directory it would be
```cd tests``` then run ```pytest``` )

## Details
#### License
MIT License: [found here](LICENSE)

#### Authors
- Student 730003140

#### Source
Code hosted (may be public or private depending on time of reading) at https://github.com/edf1101/Battleships/
