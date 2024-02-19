from game_elements import Player
from text_generators import attack_info_input


def create_players():
    # Добавляет игроков в игру
    list_of_players = []
    quantity = input("How many players? ")
    if quantity.isdigit():
        quantity = int(quantity)
        for _ in range(quantity):
            name = input("Enter your name: ")
            list_of_players.append(Player(name=name))
    else:
        print("Invalid! Enter correct number of players")
    return list_of_players


def players_turn(player, labyrinth, list_of_players, attempts=3):
    while attempts != 0:
        other_players = [
            other_player
            for other_player in list_of_players
            if other_player.name != player.name
        ]
        neighbours = [
            other_player
            for other_player in other_players
            if other_player.location == player.location
        ]
        if neighbours:
            users_input = attack_info_input(neighbours)
            if users_input == "MOVE":
                player.move(labyrinth, list_of_players)
                player.work_with_objects(labyrinth, list_of_players)
                return

            for neighbour in neighbours:
                if users_input == neighbour.name:
                    target_player = [
                        player for player in neighbours if player.name == users_input
                    ][0]
                    player.attack_player(target_player)
                    print(
                        f"{player.name} damaged {target_player.name}, {target_player.health} health points left"
                    )
                    return
                # else:
                #     player.move(labyrinth, list_of_players)
                #     return
            print(f"Wrong input, try again. {attempts} tries left!")
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
