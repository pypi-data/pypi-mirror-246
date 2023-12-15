from flask import Flask
from flask import request, jsonify
from flask import render_template
import json
from components import initialise_board, display_grid, create_battleships, validate_ship_position, place_battleships, place_AI_battleships
from game_engine import attack
from mp_game_engine import generate_attack
import os


def initialise_new_game():
    """reset all serverside variables for a new game to begin. Returns original_ships, player_ships, player_board, AI_ships, AI_board, AI_memory."""

    original_ships = create_battleships("battleships.txt")

    # current ships is a copy rather than a reference
    player_ships = original_ships.copy()
    AI_ships = original_ships.copy()

    player_board = initialise_board()
    AI_board = initialise_board()
    AI_board, AI_ships = place_AI_battleships(board=AI_board, ships=AI_ships, algorithm="random")
    AI_memory = []
    return original_ships, player_ships, player_board, AI_ships, AI_board, AI_memory

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
    """takes ships in the form (ship = name: [length, [cells]]) and converts and returns it in (ship = name: length)"""
    
    frontend_ships = {}
    for ship in ships:
        frontend_ships.update({ship:ships[ship][0]})
    return frontend_ships

def convert_ships_to_backend(ships):
    """takes (ship = name:[x,y,rotation]) and converts and returns it to (ship = name: [length, [cells]])"""

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


app = Flask(__name__)

@app.route("/placement", methods=["GET", "POST"])
def placement_interface():

    if request.method == "GET": # send the template and ships to the frontend
        return render_template("placement.html", ships=convert_ships_to_frontend(original_ships), board_size=10)
    
    elif request.method == "POST": # retrieve the board data from the front end

        ships_json = request.get_json()

        global player_ships, player_board, AI_board

        # get the ships into the backend
        player_ships = convert_ships_to_backend(ships_json)
        for ship in player_ships:
            player_board = add_ship_to_board(player_board, ship)
        

        return jsonify("data recieved")
    else:
        return jsonify("unknown method")


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "GET":
        return render_template("main.html", player_board=convert_board_to_frontend(player_board), AI_board=convert_board_to_frontend(AI_board))
    else:
        return jsonify("unknown method")
    
@app.route("/attack", methods=["GET"])
def process_attack():

    if request.method == "GET":

        # fetch where the player is attacking
        y_coord = int(request.args.get("x"))
        x_coord = int(request.args.get("y"))

        
        # so we can access these.
        global player_board, player_ships, AI_board, AI_ships, AI_memory

        # attack the AI board and track whether or not we hit
        print("player attacks AI")
        hit, AI_board, AI_ships = attack((x_coord, y_coord), AI_board, AI_ships)

        # count how much AI ship is left
        AI_cells_left = 0
        for ship in AI_ships:
            AI_cells_left += AI_ships[ship][0]

        # if the AI is still in the game:
        if AI_cells_left > 0:
            # generate the AI's attack and hit the player
            print("AI attacks player")
            AI_coords, AI_memory = generate_attack(player_board, AI_memory)
            AI_hit, player_board, player_ships = attack(AI_coords, player_board, player_ships)
        else:
            print("AI is dead")

        # count how much player ship is left
        player_cells_left = 0
        for ship in player_ships:
            player_cells_left += player_ships[ship][0]

        # print to the console
        print("player cells remaining")
        print(player_cells_left)
        print("AI cells remaining")
        print(AI_cells_left)

        # if the game is still going:
        if player_cells_left > 0 and AI_cells_left > 0:
            finished = False
        else:
            # tell the player what happened
            if player_cells_left < 1:
                finished = "You loose."
            else:
                finished = "You win."

        frontend_AI_coords = (AI_coords[1], AI_coords[0])
        # tell the frontend if the player hit the AI, where the AI attacked and whether or not the game is over

        # if the AI is still in the game and so attacked:
        if AI_cells_left > 0:
            response = {"hit": hit,
                        "AI_Turn": frontend_AI_coords,
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
    else:
        return jsonify("unknown method")



if __name__ == '__main__':
    app.template_folder = "templates"
    app.run()
    original_ships, player_ships, player_board, AI_ships, AI_board, AI_memory = initialise_new_game()