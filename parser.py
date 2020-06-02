# [[0, 6], [0, 0], [1, 0], [0, 2], [1, 0], [1, 3], [0, 4], [0, 1], [0, 0]]

# 1 pole to kolor, 2 pole typ kierunku

"""

"""
from random import randrange
import collections

file = f"C:\\Users\\Patryk\\PycharmProjects\\SIVisualizer\\board_01.txt"

COLOR_VALUES = {
    "R": (255, 0, 0),
    "G": (0, 255, 0),
    "B": (0, 0, 255),
    "Y": (255, 255, 0),
    "P": (255, 0, 127),
    "T": (0, 204, 204),
    "V": (153, 0, 153),
    "N": (0, 0, 102),
    "O": (255, 128, 0),
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


if __name__ == '__main__':
    for line in parse_input_file(file):
        print(line)


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
