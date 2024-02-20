from game_elements import Labyrinth
from gameplay import create_players, game_loop


def main():
    labyrinth_instance = Labyrinth()
    labyrinth_instance.make_fire()

    players = create_players()

    game_loop(labyrinth_instance, players)


if __name__ == "__main__":
    main()
