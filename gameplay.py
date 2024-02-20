from const import DIRECTIONS_LIST, DIRECTIONS
from game_elements import Player
from text_generators import instructions_of_move, step_intructions


def create_players():

    quantity = input("How many players?")
    try:
        quantity = int(quantity)
    except ValueError:
        print("Invalid! Enter correct number of players")

    list_of_players = []
    for _ in range(quantity):
        name = input("Enter player's name: ")
        if name not in [player.name for player in list_of_players]:
            list_of_players.append(Player(name=name))
    return list_of_players


def find_neighbours(main_player, list_of_players):
    return [
        player
        for player in list_of_players
        if player.name != player.name and (player.location() == main_player.location())
    ]


def move_collector(player, labyrinth, players_list):
    cell_location = [
        [labyrinth.labyrinth[cell]["x"], labyrinth.labyrinth[cell]["y"]]
        for cell in labyrinth.labyrinth
    ]
    attempts = 3
    while attempts != 0:
        move_direction = input(step_intructions(attempts, player.name)).upper()

        if move_direction not in DIRECTIONS_LIST:
            attempts -= 1
            print(f"Wrong input! {attempts} attempts left.")
            continue

        dx, dy = DIRECTIONS[move_direction]
        player.x += dx
        player.y += dy
        new_location = [player.x, player.y]

        prev_location_index = next(
            index
            for index, value in enumerate(labyrinth.labyrinth.items())
            if value[1]["x"] == player.x and value[1]["y"] == player.y
        )

        new_location_index = next(
            index
            for index, value in enumerate(labyrinth.labyrinth.items())
            if (value[1]["x"], value[1]["y"]) == new_location
        )

        for item in labyrinth.labyrinth.items():
            if item[1] == player.location():
                if prev_location_index > new_location_index and len(item[1]) == 3:
                    print(f"Person tried to run. {player.name}," f" game over!")
                    player.remove_player(players_list)
                    return

                elif (
                    (prev_location_index < new_location_index)
                    or (prev_location_index > new_location_index)
                    and (item[1]["special"] is True)
                ):
                    for cell in cell_location:
                        if player.x == cell[0] and player.y == cell[1]:
                            print(f"Moved {move_direction} " f"to {player.location}")
                            return

                    else:
                        dx, dy = DIRECTIONS[move_direction]
                        player.x -= dx
                        player.y -= dy
                        player.health -= 1
                    print(
                        f"Wrong vector! {player.name} gets 1 damage,"
                        f" {player.health} points of health left. "
                        f"Current location: {player.location}"
                    )
                    return
    print("Too many wrong inputs. " "Next player to make action.")


def handle_user_input(player, neighbours, labyrinth, list_of_players, attempts):
    users_input = input(instructions_of_move(neighbours))

    if users_input == "MOVE":
        move_collector(player, labyrinth, list_of_players)
        return True

    if users_input in [neighbour.name for neighbour in neighbours]:
        target_player = [
            neighbour for neighbour in neighbours if neighbour.name == users_input
        ][0]
        if target_player:
            player.attack_player(target_player)
            print(
                f"{player.name} damaged {target_player.name},"
                f" {target_player.health} health points left"
            )
            return True
    print(f"Wrong input, try again. {attempts} tries left!")
    return False


def players_turn(player, labyrinth, list_of_players, attempts=3):
    while attempts != 0:
        neighbours = find_neighbours(player, list_of_players)
        if neighbours:
            if handle_user_input(
                player, neighbours, labyrinth, list_of_players, attempts
            ):
                return
            attempts -= 1
        else:
            player.move(labyrinth, list_of_players)
            player.work_with_objects(labyrinth, list_of_players)
            return
    print("You did nothing, try next time!")


def game_loop(labyrinth, players_list):
    if len(players_list) == 0:
        print("Game over.")
        return

    for player in players_list:
        print(f"Player {player.name} is active!")
        players_turn(player, labyrinth, players_list)

        if player.health == 0:
            print("Game over for player ", player.name)
            players_list = [p for p in players_list if p != player]

    game_loop(labyrinth, players_list)
