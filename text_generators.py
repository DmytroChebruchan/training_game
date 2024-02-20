def step_intructions(attempts, player_name):
    return input(
        f"""\n{player_name} ,where would you like to move?
You have {attempts} chances for correct input:
UP to move up,
DOWN to move down,
LEFT to move left,
RIGHT to move right
"""
    )


def instructions_of_move(neighbours):
    if neighbours == 0:
        instructions = f"""\nYou can not hit anyone, therefore, you \
        only make a move to another cell.\nIf you want to hit player \
        - enter player`s name.\nIf you want to move - enter MOVE.\n"""

    else:
        players_list_string = ", ".join([player.name for player in neighbours])
        instructions = f"""\nYou can hit or move.\
        You can hit following players and finish your move:\
        {players_list_string}.\n Damage will be 1 point.\nIf you\
        want to hit player - enter player`s name.\nIf you want to move - \
        enter MOVE.\n"""

    return instructions
