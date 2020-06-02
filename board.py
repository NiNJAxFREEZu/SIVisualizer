from config import Config


class Board:

    def load(filepath):
        with open(filepath, 'r') as boardFile:
            board = boardFile.readlines()
        return board

