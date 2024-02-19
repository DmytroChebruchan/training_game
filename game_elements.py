import json

import random

from const import DIRECTIONS_LIST, DIRECTIONS

from text_generators import move_info_input


class Labyrinth:
    def __init__(self):
        with open("labyrinth_map.json", "r") as json_file:
            self.labyrinth = json.load(json_file)

    def make_fire(self):
        # Генерирует в 5-ти случайных ячейках пламя
        fire_counter = 0
        while fire_counter < 4:
            random_key = random.choice(list(self.labyrinth.keys()))
            current_cell = self.labyrinth[random_key]
            if current_cell.get("objects") is not None:
                continue
            current_cell["objects"] = {"fire": 1}
            fire_counter += 1

        return self.labyrinth

    def remove_fire(self):
        # Удаляет пламя из ячеек в конце круга
        for key, cell in self.labyrinth.items():
            if cell["objects"] == {"fire": 1}:
                del cell["objects"]

        return self.labyrinth


class Player:
    name: str
    active: bool = False
    x: int = 0
    y: int = 0
    location: list = [0, 0]
    health: int = 5
    items: dict = {}

    def __init__(self, name):
        self.name = name

    def work_with_objects(self, labyrinth, players_list):
        for _ in labyrinth.labyrinth.items():
            if (
                self.location[0] == _[1]["x"]
                and self.location[1] == _[1]["y"]
                and _[1]["objects"] is not None
            ):
                if _[1]["objects"] == {"fire": 1}:
                    self.health -= 1
                    print(f"{self.name} gets in fire, "
                          f"{self.health} points left.")

                if _[1]["objects"] == {"heart": 1}:
                    self.health = 5
                    print(f"{self.name} feels better! Health is {self.health}.")

                if _[1]["objects"] == {"key": 1}:
                    self.items.update({"key": 1})
                    _[1]["objects"].pop("key")
                    print(f"{self.name} got key! {self.items}")

                if _[1]["objects"] == {"Golem": 1}:
                    if self.items == {"key": 1}:
                        print(
                            f"***** {self.name} wins this game! "
                            f"Congratulations! *****"
                        )
                    else:
                        print(f"{self.name} was killed by Golem!")
                        self.remove_player(players_list)

    def remove_player(self, list_of_players: list):
        for player in list_of_players:
            if self.name == player.name:
                list_of_players.remove(player)

    def move(self, labyrinth, players_list):
        prev_location = [self.location[0], self.location[1]]
        cell_location = [
            [labyrinth.labyrinth[cell]["x"], labyrinth.labyrinth[cell]["y"]]
            for cell in labyrinth.labyrinth
        ]
        attempts = 3
        while attempts != 0:
            move_direction = move_info_input(attempts, self.name)

            if move_direction not in DIRECTIONS_LIST:
                attempts -= 1
                print(f"Wrong input! {attempts} attempts left.")

            if move_direction in DIRECTIONS_LIST:
                dx, dy = DIRECTIONS[move_direction]
                self.location[0] += dx
                self.location[1] += dy
                new_location = [self.location[0], self.location[1]]

                prev_location_index = next(
                    index
                    for index, value in enumerate(labyrinth.labyrinth.items())
                    if value[1]["x"] == self.location[0]
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
                            print(f"Person tried to run. {self.name},"
                                  f" game over!")
                            self.remove_player(players_list)
                            return

                        elif (
                            (prev_location_index < new_location_index)
                            or (prev_location_index > new_location_index)
                            and (value[1]["special"] is True)
                        ):
                            for cell in cell_location:
                                if (
                                    self.location[0] == cell[0]
                                    and self.location[1] == cell[1]
                                ):
                                    print(f"Moved {move_direction} "
                                          f"to {self.location}")
                                    return

                            else:
                                dx, dy = DIRECTIONS[move_direction]
                                self.location[0] -= dx
                                self.location[1] -= dy
                                self.health -= 1
                            print(
                                f"Wrong vector! {self.name} get 1 damage,"
                                f" {self.health} points left. "
                                f"Current location: {self.location}"
                            )
                            return

                    if attempts == 0:
                        print("Too many wrong inputs. "
                              "Next player to make action.")
                        return

    # def make_step(self, direction):
    #     self.x += direction[0]
    #     self.y += direction[1]

    def attack_player(self, target_player):
        target_player.health -= 1
        return (f"{target_player.name} lost 1 health point."
                f"{target_player.health} health points left")
