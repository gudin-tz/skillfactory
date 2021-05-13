#!/usr/bin/python

import sys


class Colors:
    INPT = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'


def message_print(msg, key):
    """
    Print function with color by base on type message
    :param msg: text of message
    :param key: key of type message
    :return: nothing, just print
    """
    if key == 'INFO':
        print(Colors.INFO + ' ' + key + ': ' + msg + Colors.END)
    elif key == 'WARN':
        print(Colors.WARNING + ' ' + key + ': ' + msg + Colors.END)
    elif key == 'FAIL':
        print(Colors.FAIL + ' ' + key + ': ' + msg + Colors.END)
    elif key == 'INPT':
        print(Colors.INPT + ' ' + key + ': ' + msg + Colors.END)


def game(current_turn):
    """
    Shaping current game turn, turns history and gamepad grid
    :param current_turn: current game turn coordinates of gamer (1 is Human, 2 is AI)
    :return: if winner has been defined returns True, if not is False
    """
    if current_turn % 2 != 0:
        value = list(map(int, input_value().split(',')))
        gamer = 1
    else:
        value = ai()
        gamer = 2

    if value:
        turns_history[step**2 - current_turn + 1] = value
        game_field[int(value[0]) - 1][int(value[1]) - 1] = gamer

    print(turns_history)
    print('Game turn #' + str(gamer) + ': ' + str(value))
    for x in game_field:
        print(x)
    print('\n')

    if not get_game_matrix():
        return False

    if value:
        for _gamer in gamers:
            if search_turn(_gamer, 0):
                msg = 'The winner: ' + gamers[_gamer]
                message_print(msg, 'INFO')
                return True
    else:
        msg = 'There is no winner has been defined!'
        message_print(msg, 'INFO')
        return False

    return game(current_turn - 1)


def get_game_matrix():
    """
    Getting gamepad grid function in matrix data
    :return: gamepad matrix data
    """
    game_matrix['rows'] = game_field

    cols_list = []

    for y in range(step):
        row = list()

        for x in range(step):
            row.append(game_field[x][y])

        cols_list.append(row)

    game_matrix['cols'] = cols_list

    diagonals_list = []

    diagonal = list()

    for y in range(step):
        diagonal.append(game_field[y][y])
    diagonals_list.append(diagonal)

    diagonal = list()

    for y in range(step - 1, -1, -1):
        diagonal.append(game_field[step - 1 - y][y])
    diagonals_list.append(diagonal)

    game_matrix['diagonals'] = diagonals_list

    if not game_matrix:
        return False

    return game_matrix


def input_value():
    """
    Function activated if Human's game turn now
    :return: Human's game turn coordinates data
    """
    value = str(input(' Your game turn# ')).replace('(', '').replace(')', '').replace(' ', '')
    while not check_value(value):
        value = str(input(' Your game turn# ')).replace('(', '').replace(')', '').replace(' ', '')

    return value


def check_value(value):
    """
    Function checks inputted Human's game turn data
    :param value: Human's game turn data
    :return: True - if data correctly, False - if not
    """
    if not value:
        msg = 'Inputted game data value is empty! Please, to try again...'
        message_print(msg, 'WARN')
        return False

    if ',' not in value or value.count(',') > 1:
        msg = 'Inputted game data value is incorrect! Please, to try again...'
        message_print(msg, 'WARN')
        return False

    err = []

    for asis_value in value.split(','):
        try:
            int(asis_value)
        except ValueError:
            err.append(asis_value)
            continue

        if int(asis_value) > 3:
            err.append(asis_value)

    if err:
        msg = ('There are some inputted asis\'s values is incorrect type or great then 3: (' + err.pop() +
               ')! Please, to try again...')
        message_print(msg, 'WARN')
        return False

    if list(map(int, value.split(','))) in turns_history.values():
        msg = 'This value is already been in past turns! Please, to try again...'
        message_print(msg, 'WARN')
        return False

    return True


def search_turn(gamer, field_fullness):
    """
    Function searches game winner or if AI's game turn now then function searches optimater game turn.
    If gamer is Human (1) function gets pre-winner Human's game row, column or diagonal.
    If pre-winner Human's game turn does not exists function searches AI winner game turn.
    :param gamer: gamer code (1 is Human, 2 is AI)
    :param field_fullness: gamepad fullness (for 0 to 3, 0  - string of gamepad grid is empty, 1 - current gamer
                           does only one game turn on that string, and etc)
    :return: turn data or False if no any data has been defined
    """
    turn = {}

    for matrix in game_matrix:
        for y in range(len(game_matrix[matrix])):
            if game_matrix[matrix][y].count(gamer) == 3:
                return True

            if 0 in game_matrix[matrix][y]:
                if game_matrix[matrix][y].count(gamer) == step - field_fullness:
                    turn[matrix] = [y, game_matrix[matrix][y]]

    if not turn:
        return False

    if list(turn.keys())[0] == 'rows':
        turn = [turn['rows'][0] + 1, turn['rows'][1].index(0) + 1]
    elif list(turn.keys())[0] == 'cols':
        turn = [turn['cols'][1].index(0) + 1, turn['cols'][0] + 1]
    elif list(turn.keys())[0] == 'diagonals':
        if turn['diagonals'][0] == 0:
            turn = [turn['diagonals'][1].index(0) + 1, turn['diagonals'][1].index(0) + 1]
        elif turn['diagonals'][0] == 1:
            turn = [step - turn['diagonals'][1].index(0), turn['diagonals'][1].index(0) + 1]

    return turn


def ai():
    """
    AI's game turn function
    :return: AI's game turn if exists or False
    """
    return ai_winning_turn()


def ai_winning_turn():
    """
    Function defined AI's winning game turn
    :return: AI's winning game turn or Human's winning game turn
    """
    turn = search_turn(2, 1)

    if not turn:
        turn = gamer_winning_turn(1)

    return turn


def gamer_winning_turn(gamer, recurse=1):
    """
    Function defined gamer's winning game turn
    :param gamer: gamer code
    :param recurse: search depth
    :return: gamer's winning game turn or simple (no winning) turn
    """
    if recurse == 0:
        return simple_turn()

    turn = search_turn(gamer, 1)

    if not turn:
        turn = gamer_winning_turn(1, recurse - 1)

    return turn


def simple_turn(field_fullness=2):
    """
    Simple AI game turn
    :param field_fullness: search depth
    :return: game turn
    """
    if field_fullness > step:
        return False

    turn = search_turn(2, field_fullness)

    if turn:
        return turn

    return simple_turn(field_fullness + 1)


if __name__ == '__main__':
    max_turns_count = int(sys.argv[1])
    game_field = []
    game_matrix = {}
    turns_history = {}
    step = int(max_turns_count**0.5)
    gamers = {1: 'You', 2: 'AI'}

    message_print('Input your turn value in format "x-asis,y-asis"', 'INPT')

    for i in range(step):
        arr = []
        for j in range(step):
            arr.append(0)
        game_field.append(arr)

    if not game(max_turns_count):
        sys.exit()

    sys.exit()
