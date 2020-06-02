from config import Config


def load(filepath):
    with open(filepath, 'r') as boardFile:
        board = boardFile.readlines()
    return board



