from functools import reduce
import operator
import itertools
from board_logic import get_valid_neighbors
from symbols import DIR_TYPES
from collections import defaultdict
import os
import sys
import operator
import itertools
from datetime import datetime
from argparse import ArgumentParser
from collections import defaultdict
import pycosat

LEFT = 1
RIGHT = 2
TOP = 4
BOTTOM = 8

DELTAS = [(LEFT, 0, -1),
          (RIGHT, 0, 1),
          (TOP, -1, 0),
          (BOTTOM, 1, 0)]

def pos_is_valid(size, i, j):
    return i >= 0 and i < size and j >= 0 and j < size

def valid_neighbors(size, i, j):
    ## zwraca wszystkich istniejących sąsiadów komórki w wierszu i, kolumnie j
    return ((dir_type, row, col) for (dir_type, row, col)
            in get_all_neighbors(i, j)
            if pos_is_valid(size, row, col))

def get_all_neighbors(i, j):
    ## zwraca wszystkich możliwych sąsiadów komórki w wierszu i, kolumnie j
    return ((dir_type, i+row, j+col)
            for (dir_type, row, col) in DELTAS)

def test(size, i, j):
    neighbor_dirs = (dir_type for (dir_type, row, col)
                     in valid_neighbors(size, i, j))

    for x in neighbor_dirs:
        print(x)

    # nałóż na typy kierunku operację OR
    cell_flags = reduce(operator.or_, neighbor_dirs, 0)
    print(cell_flags)

def get_pairs(collection):
    # zwraca wszystkie kombinacje dwóch elementów z kolekcji
    # np. get_pairs('ABCD', 2) -> AB AC AD BC BD CD
    return itertools.combinations(collection, 2)

def no_two(satvars):
    ## bazując na zbiorze zmiennych SAT zwraca klauzuly określające,
    ## że nie ma takiej pary zmiennych, gdzie obie zmienne są prawdziwe.
    return ((-a, -b) for (a, b) in get_pairs(satvars))

def loop_board(board):
    for i, row in enumerate(board):
        for j, char in enumerate(row):
            yield i, j, char

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

def color_var(i, j, color):
    size = 3
    num_colors = 2
    return (i * size + j) * num_colors + color + 1

def make_color_clauses(puzzle, colors):
    # zwraca klauzuly dotyczące zmiennych koloru dla każdej komórki

    clauses = []
    num_colors = len(colors)
    size = len(puzzle)

    def color_var(i, j, color):
        return (i * size + j) * num_colors + color + 1

    for i, j, char in loop_board(puzzle):
        # jeśli komórka jest wierzchołkowa
        if char.isalnum():
            endpoint_color = colors[char]

            # klauzula mówiąca o tym, że komórka ma ten kolor
            clauses.append([color_var(i, j, endpoint_color)])

            # nie ma innego koloru przypisanego tej komórce
            for other_color in range(num_colors):
                if other_color != endpoint_color:
                    clauses.append([-color_var(i, j, other_color)])

            # zebranie zmiennych kolorów dla sąsiadów komórki wierzchołkowej
            neighbor_vars = [color_var(ni, nj, endpoint_color) for
                             _, ni, nj in valid_neighbors(size, i, j)]

            # jeden z sąsiadów ma ten kolor
            clauses.append(neighbor_vars)

            # nie ma dwóch sąsiadów o tym kolorze
            clauses.extend(no_two(neighbor_vars))

        else:

            # komórce jest przypisany jeden z kolorów
            clauses.append([color_var(i, j, color)
                            for color in range(num_colors)])

            # nie ma dwóch kolorów przypisanych komórce
            cell_color_vars = (color_var(i, j, color) for
                               color in range(num_colors))

            clauses.extend(no_two(cell_color_vars))

    return clauses

def make_dir_vars(board, start_var):
    ## tworzy zmienne SAT typu kierunku dla każdej komórki

    size = len(board)
    dir_vars = dict()
    num_dir_vars = 0

    for i, j, char in loop_board(board):
        # sprawdzamy, czy komórka jest wierzchołkowa,
        # nie potrzebujemy tworzyć jej słownika
        if char.isalnum():
            continue

        # zbierz sąsiadów komórki (left 1, right 2, top 4, bottom 8)
        neighbor_dirs = (dir_type for (dir_type, row, col)
                         in get_valid_neighbors(size, i, j))

        # nałóż na sąsiadów operację OR
        dir_flag = reduce(operator.or_, neighbor_dirs, 0)
        print("cellflags ", i, j, ": ", dir_flag)

        # stwórz dla komórki słownik zmiennych typów kierunku
        dir_vars[i, j] = dict()

        # dla każdej kombinacji sąsiadów utwórz zmienną kierunku,
        # np. kierunki LR (3), BL(9), BR(10) -> {3: 126, 9: 127, 10: 128}
        for code in DIR_TYPES:
            if dir_flag & code == code:
                num_dir_vars += 1
                dir_vars[i, j][code] = start_var + num_dir_vars

    return dir_vars, num_dir_vars

def make_dir_clauses(puzzle, colors, dir_vars):
    # Generuje klauzuly zawierające zmienne SAT koloru i typu kierunku.
    # Każda wolna komórka musi mieć dokładnie jeden typ kierunku,
    # a typy kierunku określają sąsiadów o tym samym kolorze.

    dir_clauses = []
    num_colors = len(colors)
    size = len(puzzle)

    # dla każdej komórki
    for i, j, char in loop_board(puzzle):

        # jeśli komórka jest wierzchołkowa,
        # to nie potrzebujemy dla niej zmiennej dir
        if char.isalnum():
            continue

        cell_dir_dict = dir_vars[(i, j)]              # słownik typów kierunku komórki
        cell_dir_vars = list(cell_dir_dict.values())  # zmienne kierunku

        print("\ndict: ", cell_dir_dict)
        print("\nvars: ", cell_dir_vars)

        # komórka ma przynajmniej jeden typ kierunku
        dir_clauses.append(cell_dir_vars)

        # nie ma więcej niż 1 typu kierunku przypisanego do komórki
        dir_clauses.extend(no_two(cell_dir_vars))

        # dla każdego koloru
        for color in range(num_colors):

            # pobierz zmienną koloru komórki
            cell_color = color_var(i, j, color)

            # dla każdego sąsiada
            for dir_bit, n_i, n_j in get_all_neighbors(i, j):

                # pobierz zmienną koloru sąsiada
                neighbor_color = color_var(n_i, n_j, color)

                # dla każdej zmiennej kierunku komórki
                for dir_type, dir_var in cell_dir_dict.items():

                    # jeżeli typ kierunku wskazuje na sąsiada
                    if dir_type & dir_bit:
                        # kolory komórki i sąsiada są takie same
                        dir_clauses.append([-dir_var, -cell_color, neighbor_color])
                        dir_clauses.append([-dir_var, cell_color, -neighbor_color])
                    # jeżeli typ kierunku nie wskazuje na sąsiada
                    elif pos_is_valid(size, n_i, n_j):
                        # kolory komórki i sąsiada są różne
                        dir_clauses.append([-dir_var, -cell_color, -neighbor_color])

    return dir_clauses

board, colors = parse_puzzle('board2.txt')
print(colors)
color_clauses = make_color_clauses(board, colors)
print(color_clauses)

dirvars, varnum = make_dir_vars(board, 18)
print(dirvars)

dirclauses = make_dir_clauses(board, colors, dirvars)
print(dirclauses)