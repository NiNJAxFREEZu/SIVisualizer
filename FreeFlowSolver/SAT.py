from FreeFlowSolver.board_logic import *
from FreeFlowSolver.symbols import *
from FreeFlowSolver.variable_logic import *
from functools import reduce
from datetime import datetime
import operator
import pycosat

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

        # zbierz typy kierunku sąsiadów komórki (top, bottom, left, right)
        neighbor_dirs = (dir_type for (dir_type, row, col)
                         in get_valid_neighbors(size, i, j))

        # nałóż na typy kierunku operację OR
        cell_flags = reduce(operator.or_, neighbor_dirs, 0)

        # stwórz dla komórki słownik zmiennych typów kierunku
        dir_vars[i, j] = dict()

        for code in DIR_TYPES:
            # jeśli flaga kierunku jest poprawna
            if cell_flags & code == code:
                num_dir_vars += 1
                dir_vars[i, j][code] = start_var + num_dir_vars

    return dir_vars, num_dir_vars


def make_color_clauses(board, colors, color_var):
    # generuje klauzuly obejmujące N*M zmiennych SAT koloru,
    # N - liczba komórek, M - liczba kolorów.

    clauses = []
    num_colors = len(colors)
    size = len(board)

    for i, j, char in loop_board(board):
        # sprawdzamy, czy komórka jest wierzchołkowa
        if char.isalnum():
            endpoint_color = colors[char]

            # dodaj klauzulę mówiącą o tym, że komórka ma taki kolor
            clauses.append([color_var(i, j, endpoint_color)])

            # dodaj klauzulę mówiącą o tym, że komórka nie ma żadnego innego koloru
            for other_color in range(num_colors):
                if other_color != endpoint_color:
                    clauses.append([-color_var(i, j, other_color)])

            # zbierz zmienne sąsiadów dla tego koloru
            neighbor_vars = [color_var(row, col, endpoint_color) for
                             _, row, col in get_valid_neighbors(size, i, j)]

            # dodaj klauzulę mówiącą o tym, że jeden z sąsiadów ma ten kolor
            clauses.append(neighbor_vars)

            # nie ma dwóch sąsiadów, którzy mają ten kolor
            clauses.extend(no_two(neighbor_vars))

        # jeżeli komórka nie jest wierzchołkowa
        else:
            # dodaj klauzulę mówiącą o tym, że jeden z kolorów tej komórki jest określony
            clauses.append([color_var(i, j, color)
                            for color in range(num_colors)])

            # dodaj klauzulę mówiącą o tym, że nie ma dwóch kolorów przypisanych dla tej komórki
            cell_color_vars = (color_var(i, j, color) for
                               color in range(num_colors))
            clauses.extend(no_two(cell_color_vars))

    return clauses


def make_dir_clauses(puzzle, colors, color_var, dir_vars):
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


def reduce_to_sat(puzzle, colors):
    # Redukuje daną planszę do problemu SAT.
    # Zwraca listę klauzul, gdzie każda z nich to lista
    # pojedynczych zmiennych SAT, również zanegowanych.

    size = len(puzzle)
    num_colors = len(colors)
    num_cells = size**2
    num_color_vars = num_colors * num_cells

    def color_var(i, j, color):
        # zwraca numer zmiennej koloru dla komórki (i, j)
        return (i*size + j)*num_colors + color + 1

    start = datetime.now()

    color_clauses = make_color_clauses(puzzle, colors, color_var)
    dir_vars, num_dir_vars = make_dir_vars(puzzle, num_color_vars)
    dir_clauses = make_dir_clauses(puzzle, colors,
                                   color_var, dir_vars)

    num_vars = num_color_vars + num_dir_vars
    clauses = color_clauses + dir_clauses

    print('\n color_clauses:', color_clauses)
    print('\n dir_clauses:', dir_clauses)

    print('\nWygenerowano', len(color_clauses), " klauzul z", num_color_vars, "zmiennymi koloru.")
    print('Wygenerowano', len(dir_clauses), "klauzul z", num_dir_vars, "zmiennymi kierunku.")
    print('Wygenerowano łącznie', len(clauses), "klauzul z", num_vars, "zmiennymi.")
    print("\n")

    return color_var, dir_vars, num_vars, clauses


def decode_solution(puzzle, colors, color_var, dir_vars, sol):
    # deszyfruje zbiór rozwiązań SAT przez cofnięcie szyfrowania w każdej komórce
    # dla koloru i typu kierunku. Zwraca tablicę par (kolor, typ kierunku).

    sol = set(sol)
    num_colors = len(colors)
    decoded = []

    for i, row in enumerate(puzzle):
        decoded_row = []
        for j, char in enumerate(row):

            # znajdź w rozwiązaniu zmienną koloru dla komórki
            cell_color = -1
            for color in range(num_colors):
                if color_var(i, j, color) in sol:
                    assert cell_color == -1
                    cell_color = color
            # error jeśli nie znaleziono zmiennej koloru dla komórki
            assert cell_color != -1

            # znajdź w rozwiązaniu zmienną kierunku dla komórki
            cell_dir_type = -1
            # jeśli komórka jest pusta
            if not char.isalnum():
                for dir_type, dir_var in dir_vars[i, j].items():
                    if dir_var in sol:
                        assert cell_dir_type == -1
                        cell_dir_type = dir_type
                # error jeśli nie znaleziono zmiennej koloru dla komórki
                assert cell_dir_type != -1

            decoded_row.append((cell_color, cell_dir_type))
        decoded.append(decoded_row)

    return decoded


def solve_sat(puzzle, colors, color_var, dir_vars, clauses):
    all_decoded = []

    sol = pycosat.solve(clauses)

    decoded = decode_solution(puzzle, colors, color_var, dir_vars, sol)
    all_decoded.append(decoded)

    print("Rozwiązanie (zbiór zmiennych): ")
    print(sol)

    print("Rozwiązana łamigłówka:")
    print(decoded)

    return sol, decoded


# board, colors = parse_puzzle('board.txt')
# color_var, dir_vars, num_vars, clauses = reduce_to_sat(board, colors)
# _, dec = solve_sat(board, colors, color_var, dir_vars, clauses)