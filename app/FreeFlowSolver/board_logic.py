from app.FreeFlowSolver.symbols import DELTAS

def loop_board(board):
    for i, row in enumerate(board):
        for j, char in enumerate(row):
            yield i, j, char


def pos_is_valid(size, i, j):
    return i >= 0 and i < size and j >= 0 and j < size


def get_all_neighbors(i, j):
    ## zwraca wszystkich możliwych sąsiadów komórki w wierszu i, kolumnie j
    return ((dir_bit, i+row, j+col)
            for (dir_bit, row, col) in DELTAS)


def get_valid_neighbors(size, i, j):
    ## zwraca wszystkich istniejących na planszy sąsiadów komórki w wierszu i, kolumnie j
    return ((dir_type, row, col) for (dir_type, row, col)
            in get_all_neighbors(i, j)
            if pos_is_valid(size, row, col))


def repair_colors(puzzle, colors):
    # jeśli w planszy użyto innych oznaczeń kolorów niż R, G, B, ...,
    # to zmieniamy je na właśnie taki format.

    if 'R' in colors.keys():
        return puzzle, colors

    color_lookup = 'RBYGOCMmPAWgTbcp'
    new_puzzle = []

    try:
        for row in puzzle:
            new_row = []
            for char in row:
                if char.isalnum():
                    char = color_lookup[ord(char)-ord('A')]
                new_row.append(char)

            new_puzzle.append(''.join(new_row))
        new_colors = dict((color_lookup[ord(char)-ord('A')], index)
                          for (char, index) in colors.items())

    except IndexError:
        return puzzle, colors

    return new_puzzle, new_colors


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
                    # print("Zarejestrowano ponownie kolor", char, ".")
                    # jeśli mamy już 2 komórki w tym kolorze
                    if color_counter[color]:
                        # print('Za dużo koloru', char, '!')
                        return None, None
                    color_counter[color] = 1
                else:
                    # print("Zarejestrowano kolor", char, ".")
                    color = len(colors)
                    colors[char] = color
                    color_counter.append(0)

    # sprawdź czy każdy kolor występuje dwa razy
    for char, color in colors.items():
        if not color_counter[color]:
            # print('Kolor', char, 'ma początek bez końca!')
            return None, None

    print('\n board:', board)
    print('\n colors:', colors)

    return board, colors
