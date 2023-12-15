"""This module runs a web interface for a battleships game against
an AI opponent using Flask. It will be ran on the local host when
this module is the entry point.
functions:
initialise_new_game()
convert_board_to_frontend()
convert_ships_to_frontend()
convert_ships_to_backend()
add_ship_to_board()
placement_interface()
root()
process_attack()"""
import os
from flask import Flask
from flask import request, jsonify
from flask import render_template
from components import initialise_board, create_battleships, place_ai_battleships
from game_engine import attack
from mp_game_engine import generate_attack

def initialise_new_game():
    """reset all serverside variables for a new game to begin.
    Returns original_ships, player_ships, player_board, AI_ships, AI_board, AI_memory."""

    original_ships_dict = create_battleships("battleships_source\\battleships.txt")
    # current ships is a copy rather than a reference
    player_ships_dict = original_ships_dict.copy()
    ai_ships_dict = original_ships_dict.copy()

    player_board_arr = initialise_board()
    ai_board_arr = initialise_board()
    ai_board_arr, ai_ships_dict = place_ai_battleships(ai_board_arr, ai_ships_dict, "random")
    ai_memory_arr = []
    return original_ships_dict, player_ships_dict, player_board_arr, ai_ships_dict, ai_board_arr, ai_memory_arr

def convert_board_to_frontend(board):
    """converts a board to (row, column) rather than (column, row). Returns the new board."""
    new_board = []
    for i in range(len(board)):
        new_board.append([])

    for row in board:
        i=0
        for item in row:
            new_board[i].append(item)
            i+=1
    return new_board

def convert_ships_to_frontend(ships):
    """takes ships in the form (ship = name: [length, [cells]])
    and converts and returns it in (ship = name: length)"""

    frontend_ships = {}
    for ship in ships:
        frontend_ships.update({ship:ships[ship][0]})
    return frontend_ships

def convert_ships_to_backend(ships):
    """takes (ship = name:[x,y,rotation]) and converts and returns it to
    (ship = name: [length, [cells]])"""

    backend_ships = {}
    for ship in ships:
        ship_cells = []
        ship_length = original_ships[ship][0]
        for i in range(ship_length): # for every cell that must be in the ship
            if ships[ship][2] == "h":
                # if it is horizontal, add the cells of (x+i, y) for each i in the ship length
                ship_cells.append((int(ships[ship][0])+i, int(ships[ship][1])))
            if ships[ship][2] == "v":
                # if it is vertical, add the cells of (x, y+i) for each i in the ship length
                ship_cells.append((int(ships[ship][0]), int(ships[ship][1])+i))
        backend_ships.update({ship:[ship_length, ship_cells]})
    return backend_ships

def add_ship_to_board(board, ship):
    """expects a board and a ship in the form ship = name : [length, [cells]]"""
    for cell in player_ships[ship][1]:
        # set the cell value to the ship's name for each cell
        board[cell[0]][cell[1]] = ship
    return board

def count_cells_left(dictionary):
    """This function returns how many cells are alive in a dictionary of ships."""
    cells_left = 0
    for ship in dictionary:
        cells_left += dictionary[ship][0]
    return cells_left

app = Flask(__name__)

@app.route("/placement", methods=["GET", "POST"])
def placement_interface():
    """Returns the template placement.html to the frontend with all other relevant info.
    Initialises a new game when /placement is visited.
    Stores data about ship positions from the frontend on a POST request"""

    global original_ships, player_ships, player_board, ai_ships, ai_board, ai_memory

    if request.method == "GET": # send the template and ships to the frontend

        # initialise the game again in, so the server does not need to be re launched for the player to start a new game
        original_ships, player_ships, player_board, ai_ships, ai_board, ai_memory = initialise_new_game()

        return render_template("placement.html", ships=convert_ships_to_frontend(original_ships), board_size=10)

    if request.method == "POST": # retrieve the board data from the front end

        ships_json = request.get_json()

        # get the ships into the backend
        player_ships = convert_ships_to_backend(ships_json)
        for ship in player_ships:
            player_board = add_ship_to_board(player_board, ship)


        return jsonify("data recieved")

    return jsonify("unknown method")


@app.route("/", methods=["GET"])
def root():
    """return the render template for the main game to the server"""
    if request.method == "GET":
        return render_template("main.html", player_board=convert_board_to_frontend(player_board), AI_board=convert_board_to_frontend(ai_board))
    return jsonify("unknown method")

@app.route("/attack", methods=["GET"])
def process_attack():
    """fetches where the player is attacking from the server
    attacks the AI board accordingly
    checks if the AI is still in the game
    if it is, generate an attack for the AI and attack the player
    checks if the player is still in the game
    tell the frontend if the game is over, where the AI attacked and if the player hit, where applicable"""

    if request.method == "GET":

        # so we can access these.
        global player_board, player_ships, ai_board, ai_ships, ai_memory

        player_cells_left = count_cells_left(player_ships)
        ai_cells_left = count_cells_left(ai_ships)

        # if the game is already over, we should not allow any attacks to go through
        if ai_cells_left <= 0 or player_cells_left <=0:
            raise RuntimeError("The game is over so further action is denied.")


        # fetch where the player is attacking
        y_coord = int(request.args.get("x"))
        x_coord = int(request.args.get("y"))

        # attack the AI board and track whether or not we hit
        print("player attacks AI")
        hit, ai_board, ai_ships = attack((x_coord, y_coord), ai_board, ai_ships)

        # count how much AI ship is left
        ai_cells_left = count_cells_left(ai_ships)

        # if the AI is still in the game:
        if ai_cells_left > 0:
            # generate the AI's attack and hit the player
            print("AI attacks player")
            ai_coords, ai_memory = generate_attack(player_board, ai_memory)
            frontend_ai_coords = (ai_coords[1], ai_coords[0])
            ai_hit, player_board, player_ships = attack(ai_coords, player_board, player_ships)
        else:
            print("AI is dead")

        # count how much player ship is left
        player_cells_left = count_cells_left(player_ships)

        # print to the console
        print("player cells remaining")
        print(player_cells_left)
        print("AI cells remaining")
        print(ai_cells_left)

        # if the game is still going:
        if player_cells_left > 0 and ai_cells_left > 0:
            finished = False
        else:
            # tell the player what happened
            if player_cells_left < 1:
                finished = "You loose. Return to /placement to start a new game."
            else:
                finished = "You win. Return to /placement to start a new game."

        # tell the frontend if the player hit the AI, where the AI attacked
        # and whether or not the game is over

        # if the AI is still in the game and so attacked:
        if ai_cells_left > 0:
            response = {"hit": hit,
                        "AI_Turn": frontend_ai_coords,
                        "finished": finished}
        else:
            # if the player is still in the game and so could have attacked:
            if player_cells_left > 0:
                response = {"hit": hit,
                            "finished": finished}
            # if both players are dead. Both hits are denied
            else:
                response = {"finished": finished}

        return jsonify(response)
    return jsonify("unknown method")



if __name__ == "__main__":
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.template_folder = templates_path
    original_ships, player_ships, player_board, ai_ships, ai_board, ai_memory = initialise_new_game()
    app.run()
