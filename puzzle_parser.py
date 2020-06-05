# [[0, 6], [0, 0], [1, 0], [0, 2], [1, 0], [1, 3], [0, 4], [0, 1], [0, 0]]

# 1 pole to kolor, 2 pole typ kierunku

"""

"""
import collections
from random import randrange
import json
import math

COLOR_VALUES = {
    "R": (255, 50, 50),
    "G": (50, 255, 50),
    "B": (50, 50, 255),
    "Y": (255, 255, 50),
    "P": (255, 50, 127),
    "T": (50, 204, 204),
    "V": (153, 50, 153),
    "N": (50, 50, 102),
    "O": (255, 128, 50),
    "S": (64, 64, 64)
}


def randomColour():
    red = randrange(256)
    green = randrange(256)
    blue = randrange(256)
    return red, green, blue


def check_board(board):
    cnt = collections.Counter(board)
    del cnt['.']

    return all(counter == 2 for counter in cnt.values())


def parse_input_file(path):
    with open(path, 'r') as input_board:
        input_board = input_board.read().split()
        input_board = [sign for elem in input_board for sign in elem]

    if not check_board(input_board):
        return None

    parsed_board = list()
    for index, sign in enumerate(input_board):
        if sign == '.':
            color = "blank"
        else:
            color = COLOR_VALUES[sign]

        field_info = dict()
        field_info["index"] = index
        field_info["color"] = color
        parsed_board.append(field_info)
    return parsed_board


def parse_input_file_to_2d_array(path):
    with open(path, 'r') as input_board:
        input_board = input_board.read().split()

    board = list()
    for line in input_board:
        new_row = list()
        for sign in line:
            if sign == '.':
                color = "blank"
            else:
                color = COLOR_VALUES[sign]
            new_row.append(color)
        board.append(new_row)

    return board


res = "result_01.txt"

c = {
    "0": "R",
    "1": "G"
}


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def parse_result_to_2d_array(path, colors):
    with open(path) as f:
        input_board = json.load(f)
    size = len(input_board)
    dim = int(math.sqrt(size))
    input_board = chunks(input_board, dim)

    board = list()
    for line in input_board:
        new_row = list()
        for elem in line:
            color = colors[str(elem[0])]
            color = COLOR_VALUES[color]
            new_row.append(color)
        board.append(new_row)
    return board


from ast import literal_eval

t = "test"
import itertools


def test(path, colors):
    with open(path) as f:
        input_board = [list(literal_eval(line)) for line in f]
        input_board = list(itertools.chain(*input_board))

    board = list()
    for line in input_board:
        new_row = list()
        for elem in line:
            color = colors[str(elem[0])]
            color = COLOR_VALUES[color]
            new_row.append(color)
        board.append(new_row)
    return board


if __name__ == '__main__':
    for l in test(t, c):
        print(l)
    print()


def parse_puzzle(filename):
    # pobiera z pliku informacje na temat planszy,
    # zwraca słownik mapujący znaki kolorów na liczby
    # np. {"R":0, "G":1, "Y",2}

    f = open(filename, "r")
    if f.mode == 'r':
        board = f.read().splitlines()

    size = len(board[0])
    board = board[:size]

    colors = dict()
    color_counter = []

    for i, row in enumerate(board):
        for j, char in enumerate(row):
            # jeśli komórka jest wierzchołkowa
            if char.isalnum():
                # jeśli już odnotowaliśmy ten kolor na planszy
                if char in colors:
                    color = colors[char]
                    print("Just got ", char, " again.")
                    # jeśli mamy już 2 komórki w tym kolorze
                    if color_counter[color]:
                        print('I already have too many ', char, '!')
                        return None, None
                    color_counter[color] = 1
                else:
                    print("Just got ", char, ".")
                    color = len(colors)
                    colors[char] = color
                    color_counter.append(0)

    # sprawdź czy każdy kolor występuje dwa razy
    for char, color in colors.items():
        if not color_counter[color]:
            print('Color ', char, ' has start but no end!')
            return None, None

    return board, colors
