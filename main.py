from game_elements import Labyrinth, Player
from gameplay import create_players, game_loop


def main():

    labyrinth_instance = Labyrinth()
    labyrinth_instance.make_fire()

    game_loop(labyrinth_instance, create_players())


if __name__ == "__main__":
    main()
