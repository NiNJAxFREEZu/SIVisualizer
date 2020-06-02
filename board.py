from config import Config
from random import randrange


def load(filepath):
    with open(filepath, 'r') as boardFile:
        board = boardFile.readlines()
    return board


def randomColour():
    red = randrange(256)
    green = randrange(256)
    blue = randrange(256)
    return red, green, blue

