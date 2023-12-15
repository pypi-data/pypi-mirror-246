"""This module contains various components of the game.
It contains the dictionaries valid_letters, numbers_to_letters and orientation_resolution.
It contains the subroutines:
display_grid
display_hidden_grid
validate_ship_position
initialise_board
create_battleships
place_battleships
place_player_battleships
place_ai_battleships"""

import random
import copy

valid_letters = {
    # the letters on the grid and the indexes they are associated with.
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9
}

numbers_to_letters = {
    # the inverse of valid_letters, used to convert integers to letters
    0:"a", 1:"b", 2:"C", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"j"
}

orientation_resolution = {
    # this is a dictionary that maps user orientation inputs to a list of the relative positions
    # of the cells a ship will take up relative to its origin, given one of these options.
    # it supports ships of up to length 7.
    "w": [(0,0), (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0)],
    "a": [(0,0), (0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6)],
    "s": [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)],
    "d": [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0.6)]
}

def display_grid(grid, lines):
    """given a grid (a list of rows) and an array of 3 lines to print next,
    it will display the grid and those lines. It will return user input."""

    # maps grid elements to symbols
    symbol_keys = {
        None: "~",
        "ship": "■",
        "hit": "#",
        "miss": "x",
        "marker": "□"
    }

    # print some whitespace to the terminal just because it looks neater
    for i in range(50):
        print("")

    # top row above the grid
    print("@ a b c d e f g h i j")
    i = 0
    # for every item in the grid
    for row in grid:
        print(str(i), end="")
        for column in row:
            # If the value is not in the dictionary, it must be a ship.
            if column in symbol_keys:
                print("|" + symbol_keys[column], end="")
            else:
                print("|" + symbol_keys["ship"], end="")
        print("|")
        i += 1

    # print all but the last line, which will be used as input instead
    for line in lines[:-1]:
        print(line)
    user_input = input(lines[-1:][0])
    return user_input

def display_hidden_grid(grid, lines):
    """given a grid (a list of rows) and an array of 3 lines to print next, it will display the grid 
    and those lines. It will return user input. Ships will be hidden."""

    # maps grid elements to symbols
    symbol_keys = {
        None: "~",
        "ship": "~",
        "hit": "#",
        "miss": "x",
        "marker": "□"
    }

    # print some whitespace to the terminal just because it looks neater
    for i in range(50):
        print("")

    # top row above the grid
    print("@ a b c d e f g h i j")
    i = 0
    # for every item in the grid
    for row in grid:
        print(str(i), end="")
        for column in row:
            # If the value is not in the dictionary, it must be a ship.
            if column in symbol_keys:
                print("|" + symbol_keys[column], end="")
            else:
                print("|" + symbol_keys["ship"], end="")
        print("|")
        i += 1

    # print all but the last line, which will be used as input instead
    for line in lines[:-1]:
        print(line)
    user_input = input(lines[-1:][0])
    return user_input

def validate_ship_position(board, position, orientation, ship, ships):
    """takes position as (x,y), orientation as a character and ship as a ship name. returns whether
    or not the location is valid and updates the grid and the ship's cells if it is. Returns 
    valid (bool), board (array of rows), ships (dictionary)"""
    valid = True
    try:
        # for every cell the ship will occupy
        for i in range(ships[ship][0]):
            row = position[0] + orientation_resolution[orientation][i][0]
            column = position[1] + orientation_resolution[orientation][i][1]

            # validation that each cell is empty and in the grid
            if not (0 <= row <= 9 and 0 <= column <= 9):
                valid = False
            if board[row][column] not in [None, "marker"]:
                valid = False

        if valid:
            # update the board to ■ for every cell the ship will occupy
            for i in range(ships[ship][0]):
                row = position[0] + orientation_resolution[orientation][i][0]
                column = position[1] + orientation_resolution[orientation][i][1]
                board[row][column] = ship
                ships[ship][1].append((row, column))
        return valid, board, ships

    except:
        return False, board, ships

def initialise_board(size=10):
    """set up and return an n*n grid for the player. The grid is a list of rows."""
    grid = []
    row = []
    for i in range(size):
        row.append(None)
    for i in range(size):
        grid.append(row[:])
    return grid

def create_battleships(filepath):
    """loads ships from the specified text file. the ships are returned
    in a dictionary with the form {ship_name: [length, cells occupied]}"""

    ships = {}

    with open(filepath, "r") as ship_file:
        for line in ship_file:
            ship_name, ship_length = line.strip().split(', ')
            ships.update({ship_name : [int(ship_length) , []]})
    return ships

def place_battleships(board, ships, algorithm="simple"):
    """this will take a board and a dictionary of ships and iterate through it, 
    placing each according to the specified algorithm (simple or random.) The 
    board and dictionary of ships will be returned."""
    # place them from the top left down sequentially
    if algorithm == "simple":
        i=0
        for ship in ships:
            valid, board, ships = validate_ship_position((i,0), "d", board, ship, ships)
            i+=1

    #place them randomly
    if algorithm == "random":
        for ship in ships:
            ship_successfully_placed = False

            # try random positions and orientations until a valid location is found
            while not ship_successfully_placed:
                coordinates = (random.randint(0, 9), random.randint(0, 9))
                orientation_options = list(orientation_resolution.keys())
                orientation = orientation_options[random.randint(0, 3)]
                # check if this location is valid. the while loop will repeat if this does not work
                ship_successfully_placed, board, ships = validate_ship_position(board, coordinates, orientation, ship, ships)
    return board, ships

def place_player_battleships(board, ships):
    """this will take a board and a dictionary of ships and iterate through it, prompting the player
    to place and orient each one. It will return the updated board and dictionary of ships."""
    lines = ["", "", ""]

    for ship in ships:
        reset_grid = copy.deepcopy(board)
        valid_position = False

        # keep trying until the ship is properly placed
        while not valid_position:

            # display the grid and prompt for user input
            board = copy.deepcopy(reset_grid)
            lines[0] = "now placing " + ship + ", length " + str(ships[ship][0])
            lines[1] = "enter coordinates in the form like a5"
            ship_coords = display_grid(board, lines)

            # confirm and validate the given position / orientation
            try:
                if ship_coords[0] in valid_letters and (int(ship_coords[1]) >= 0 and int(ship_coords[1]) <= 9):
                    # place a marker so the player can see where they're placing it
                    board[int(ship_coords[1])][valid_letters[ship_coords[0]]] = "marker"
                    lines[1] = "enter w, a, s or d to determine the orientation of the ship"
                    ship_orientation = display_grid(board, lines)
                    valid_position, board, ships = validate_ship_position(board, [int(ship_coords[1]), valid_letters[ship_coords[0]]], ship_orientation, ship, ships)

                    if valid_position:
                        # the position and orientation are valid, inform the user the placement was successful.
                        lines[0] = ship + " successfully placed"
                        lines[1] = ""
                        display_grid(board, lines)
                    else:
                        # the ship orientation given is invalid, so reset the
                        # changes to the board and inform the user
                        lines[0] = ship + " placement failed"
                        lines[1] = "invalid orientation"
                        board = copy.deepcopy(reset_grid)
                        display_grid(reset_grid, lines)
                else:
                    # the ship coords given are invalid, so reset the
                    # changes to the board and inform the user
                    lines[0] = ship + " placement failed"
                    lines[1] = "coordinates outside grid"
                    board = copy.deepcopy(reset_grid)
                    display_grid(reset_grid, lines)
            except:
                # the user's input threw an exception, so reset the changes
                # to the board and inform the user
                lines[0] = ship + " placement failed"
                lines[1] = "invalid input"
                board = copy.deepcopy(reset_grid)
                display_grid(reset_grid, lines)
    assert len(board) == 10
    return board, ships

def place_ai_battleships(board, ships, algorithm="simple"):
    # this is identical to place_battleships, this one just has a better name.
    """this will take a board and a dictionary of ships and iterate through it, placing each according to the
    specified algorithm (simple or random.) The board and dictionary of ships will be returned."""
    # place them from the top left down sequentially
    if algorithm == "simple":
        i=0
        for ship in ships:
            valid, board, ships = validate_ship_position(board, (i,0), "d", ship, ships)
            i+=1

    #place them randomly
    if algorithm == "random":
        for ship in ships:
            ship_successfully_placed = False

            # try random positions and orientations until a valid location is found
            while not ship_successfully_placed:
                coordinates = (random.randint(0, 9), random.randint(0, 9))
                orientation_options = list(orientation_resolution.keys())
                orientation = orientation_options[random.randint(0, 3)]
                # check if this location is valid. the while loop will repeat if this does not work
                ship_successfully_placed, board, ships = validate_ship_position(board, coordinates, orientation, ship, ships)
    return board, ships
