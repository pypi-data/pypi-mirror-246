"""This module contains simple_game_loop(), which prompts the
player to attack an AI board until all ships are destroyed.
Additionally it contains attack() for processing an attack on
a board at a location, and cli_coords_input() which requests
coordinates from the user."""

from components import display_grid, display_hidden_grid, initialise_board, create_battleships, place_ai_battleships
from components import valid_letters
import time

def attack(coordinates, board, battleships):
    """takes coords as a tuple (x,y), board as array and battleships as a dict. Returns [if hit], the new board and new battleships."""

    assert len(coordinates) == 2
    # in the case the coordinates are a list they will be a tuple now.
    coordinates = tuple(coordinates)

    print("coordinates being attacked:")
    print(coordinates)

    # everything that is not one of these is a hit
    if board[coordinates[1]][coordinates[0]] not in [None, "hit", "miss"]:
        # reduce ship length by 1
        battleships[board[coordinates[1]][coordinates[0]]][0] -= 1
        # remove the cell that was hit from the target ship's cells
        battleships[board[coordinates[1]][coordinates[0]]][1].remove(coordinates[: : -1])
        # update grid
        board[coordinates[1]][coordinates[0]] = "hit"
        print("attack hit")

        return True, board, battleships
    # update grid otherwise
    board[coordinates[1]][coordinates[0]] = "miss"
    print("attack miss")
    return False, board, battleships


def cli_coordinates_input(grid):
    """takes a grid as a list of rows, displays it to the user and asks for the coordinates to attack. It returns a tuple of where to attack (x,y)."""
    valid = False

    while not valid:

        response = display_hidden_grid(grid, lines=["Input coordinates to attack", "", ""])
        # input validation that it is in the form like a0
        try:
            if len(response) == 2:
                if response[0] in valid_letters and int(response[1]) >= 0 and int(response[1]) <= 9:
                    valid = True
        except:
            pass

    # here we convert the string into two characters to return it
    return tuple([valid_letters[response[0]], int(response[1])])

def simple_game_loop():
    """This function runs a singleplayer game where a player attacks an AI board until all ships are destroyed."""

    # create the AI board and their ships
    ai_board = initialise_board()
    ai_ships = create_battleships("battleships_source\\battleships.txt")

    # place the AI ships on thier board
    ai_board, ai_ships = place_ai_battleships(board=ai_board, ships=ai_ships, algorithm="random")

    # welcome message
    display_hidden_grid(grid=ai_board, lines=["Welcome to battleships.", "Press enter to continue.", ""])

    game_over = False
    while not game_over:

        # count how much AI ship is left
        ai_cells_left = 0
        for ship in ai_ships:
            ai_cells_left += ai_ships[ship][0]

        # if the game is still going:
        if ai_cells_left > 0:
            # get where the player wants to attack and attack that cell.
            player_attack_location = cli_coordinates_input(ai_board)
            player_hit, ai_board, ai_ships = attack(coordinates=player_attack_location, board=ai_board, battleships=ai_ships)

            # tell the player if they hit
            if player_hit:
                display_hidden_grid(ai_board, ["You hit an enemy ship.", "", ""])
            else:
                display_hidden_grid(ai_board, ["Your attack missed.", "", ""])
        # if the game has ended
        else:
            game_over = True
            time.sleep(0.5)
            display_grid(ai_board, ["The game is over.", "All targets destroyed.", ""])


if __name__ == "__main__":
    simple_game_loop()
