# [[0, 6], [0, 0], [1, 0], [0, 2], [1, 0], [1, 3], [0, 4], [0, 1], [0, 0]]

# 1 pole to kolor, 2 pole typ kierunku

"""

"""
import collections
from random import randrange
import json
import math

COLOR_VALUES = {
    "R": (255, 51, 51),
    "G": (97, 255, 144),
    "B": (100, 149, 237),
    "Y": (255, 213, 0),
    "P": (255, 97, 129),
    "T": (97, 255, 223),
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


def parse_input_file_to_2d_array(BOARD):
    board = list()
    for line in BOARD:
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


# def parse_result_to_2d_array(path, colors):
#     with open(path) as f:
#         input_board = json.load(f)
#     size = len(input_board)
#     dim = int(math.sqrt(size))
#     input_board = chunks(input_board, dim)
#
#     board = list()
#     for line in input_board:
#         new_row = list()
#         for elem in line:
#             color = colors[str(elem[0])]
#             color = COLOR_VALUES[color]
#             new_row.append(color)
#         board.append(new_row)
#     return board


def parse_result_to_2d_array(SOLUTION, colors):
    board = list()
    for line in SOLUTION:
        new_row = list()
        for elem in line:
            color = colors[str(elem[0])]
            color = COLOR_VALUES[color]
            new_row.append(color)
        board.append(new_row)
    return board


