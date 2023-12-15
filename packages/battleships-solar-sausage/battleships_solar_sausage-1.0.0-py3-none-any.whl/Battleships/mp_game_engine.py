from components import create_battleships, initialise_board, place_AI_battleships, place_player_battleships, display_grid, display_hidden_grid, numbers_to_letters
from game_engine import attack, cli_coordinates_input
import random, time

def generate_attack(board, memory):
    """given a board (list of rows) and a memory of locations previously hit, return new coordinates as a tuple and memory as an array"""
    valid_coords = False
    attempts = 0

    # keep guessing locations until we find a valid one. If the attempts becomes extremely high then we have a problem.
    while not valid_coords:
        attempts += 1
        x_coord = random.randint(0, len(board)-1)
        y_coord = random.randint(0, len(board)-1)
        coordinates = (x_coord,y_coord)

        if coordinates not in memory:
            valid_coords = True
            memory.append(coordinates)

        if attempts > 100000:
            raise Exception("Attempts exhausted. Likely no attack locations remaining.")

    if valid_coords:        
        return coordinates, memory
    else:
        raise Exception("Could not find a valid attack location.")


def AI_opponent_game_loop():
    """Runs a two player game in the terminal where the player plays against an AI"""

    players = {}

    # create the player board and their ships
    player_board = initialise_board()
    player_ships = create_battleships("Battleships//battleships.txt")

    # create the AI board and their ships
    AI_board = initialise_board()
    AI_ships = create_battleships("Battleships//battleships.txt")

    # place their ships
    player_board, player_ships = place_player_battleships(board=player_board, ships=player_ships)
    AI_board, AI_ships = place_AI_battleships(board=AI_board, ships=AI_ships, algorithm="random")

    # add both players into the game
    players.update({"human":[player_board, player_ships]})
    players.update({"AI":[AI_board, AI_ships]})

    # welcome message
    display_grid(grid=player_board, lines=["Welcome to battleships.", "Press enter to continue.", ""])

    # so the AI remembers where it has fired
    AI_memory = []

    game_over = False
    while not game_over:

        # count how much player ship is left
        player_cells_left = 0
        for ship in player_ships:
            player_cells_left += player_ships[ship][0]

        # count how much AI ship is left
        AI_cells_left = 0
        for ship in AI_ships:
            AI_cells_left += AI_ships[ship][0]

        # if the game is still going:
        if player_cells_left > 0 and AI_cells_left > 0:
            # get where the player wants to attack and attack that cell.
            player_attack_location = cli_coordinates_input(AI_board)
            player_hit, AI_board, AI_ships = attack(coordinates=player_attack_location, board=AI_board, battleships=AI_ships)

            # tell the player if they hit
            if player_hit:
                display_hidden_grid(AI_board, ["You hit an enemy ship.", "", ""])
            else: 
                display_hidden_grid(AI_board, ["Your attack missed.", "", ""])

            # generate AI attack location, inform the player, and show the result
            AI_attack_location, AI_memory = generate_attack(board=player_board, memory=AI_memory)
            display_grid(player_board, ["The AI is attacking you at:", str(numbers_to_letters[AI_attack_location[0]]) + str(AI_attack_location[1]), ""])
            AI_hit, player_board, player_ships = attack(coordinates=AI_attack_location, board=player_board, battleships=player_ships)

            if AI_hit:
                display_grid(player_board, ["The enemy has hit your ship.", "Fiddle de dee.", ""])
            else:
                display_grid(player_board, ["The enemy missed.", "", ""])
        
        # if the game has ended
        else:
            game_over = True
            time.sleep(0.5)
            # if the player has won
            if player_cells_left > 0:
                display_grid(AI_board, ["You have won.", "I hope you feel good about yourself.", ""])
            # if the AI has won
            else:
                display_grid(player_board, ["You have lost.", "You should be ashamed of yourself.", ""])


if __name__ == "__main__":
    AI_opponent_game_loop()


