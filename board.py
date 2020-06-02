class Board:
    board = ""

    def load(self, filepath):
        with open(filepath, 'r') as boardFile:
            self.board = boardFile.readlines()

