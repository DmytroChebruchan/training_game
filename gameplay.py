from const import DIRECTIONS_LIST, DIRECTIONS
from game_elements import Player
from text_generators import attack_info_input, move_info_input


def create_players():
    # Добавляет игроков в игру

    quantity = input("How many players?")
    if quantity.isdigit():
        print("Invalid! Enter correct number of players")
        return

    quantity = int(quantity)
    list_of_players = []
    for _ in range(quantity):
        name = input("Enter player's name: ")
        list_of_players.append(Player(name=name))
    return list_of_players


def find_neighbours(main_player, list_of_players):
    return [
        player
        for player in list_of_players
        if player.name != player.name and (player.location ==
                                           main_player.location)
    ]


def move_collector(player, labyrinth, players_list):
    prev_location = [player.location[0], player.location[1]]
    cell_location = [
        [labyrinth.labyrinth[cell]["x"], labyrinth.labyrinth[cell]["y"]]
        for cell in labyrinth.labyrinth
    ]
    attempts = 3
    while attempts != 0:
        move_direction = move_info_input(attempts, player.name)

        if move_direction not in DIRECTIONS_LIST:
            attempts -= 1
            print(f"Wrong input! {attempts} attempts left.")
            continue

        dx, dy = DIRECTIONS[move_direction]
        player.location[0] += dx
        player.location[1] += dy
        new_location = [player.location[0], player.location[1]]

        prev_location_index = next(
            index
            for index, value in enumerate(labyrinth.labyrinth.items())
            if value[1]["x"] == player.location[0]
            and value[1]["y"] == prev_location[1]
        )

        new_location_index = next(
            index
            for index, value in enumerate(labyrinth.labyrinth.items())
            if value[1]["x"] == new_location[0]
            and value[1]["y"] == new_location[1]
        )
        for value in labyrinth.labyrinth.items():
            if (
                    value[1]["x"] == prev_location[0]
                    and value[1]["y"] == prev_location[1]
            ):
                if (
                        prev_location_index > new_location_index
                        and len(value[1]) == 3
                ):
                    print(f"Person tried to run. {player.name},"
                          f" game over!")
                    player.remove_player(players_list)
                    return

                elif (
                        (prev_location_index < new_location_index)
                        or (prev_location_index > new_location_index)
                        and (value[1]["special"] is True)
                ):
                    for cell in cell_location:
                        if (
                                player.location[0] == cell[0]
                                and player.location[1] == cell[1]
                        ):
                            print(f"Moved {move_direction} "
                                  f"to {player.location}")
                            return

                    else:
                        dx, dy = DIRECTIONS[move_direction]
                        player.location[0] -= dx
                        player.location[1] -= dy
                        player.health -= 1
                    print(
                        f"Wrong vector! {player.name} get 1 damage,"
                        f" {player.health} points left. "
                        f"Current location: {player.location}"
                    )
                    return

            if attempts == 0:
                print("Too many wrong inputs. "
                      "Next player to make action.")
                return


def handle_user_input(player, neighbours, labyrinth, list_of_players, attempts):
    users_input = attack_info_input(neighbours)
    if users_input == "MOVE":
        move_collector(player, labyrinth, list_of_players)
        return True

    for neighbour in neighbours:
        if users_input == neighbour.name:
            target_player = next(
                (p for p in neighbours if p.name == users_input), None)
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
