Battleships Coursework

This package contains several modules.

game_engine.py runs a one-player terminal based game of battleships where a player attacks a hidden enemy grid until all ships are destroyed.
mp_game_engine.py runs a two-player terminal based game of battleships where a player and an AI opponent attack each other until only one has ships remaining.
main.py runs an app on the localhost, allowing the user to play the game via a web interface in a similar fasion to mp_game_engine.

components.py contains many components used by other modules.

To run these modules, open the command prompt at the project's directory and run:
python Battleships\main.py
python Battleships\game_engine.py
python Battleships\mp_game_engine.py

main.py should be accessed on http://127.0.0.1:5000/placement

Users must install Flask with "pip install flask" before attempting to run main.py