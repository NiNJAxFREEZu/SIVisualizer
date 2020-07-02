import itertools

def get_pairs(collection):
    # zwraca wszystkie kombinacje dwóch elementów z kolekcji
    # np. get_pairs('ABCD') -> AB AC AD BC BD CD
    return itertools.combinations(collection, 2)

def no_two(satvars):
    ## bazując na zbiorze zmiennych SAT zwraca klauzuly określające,
    ## że nie ma takiej pary zmiennych, gdzie obie zmienne są prawdziwe.
    return ((-a, -b) for (a, b) in get_pairs(satvars))

