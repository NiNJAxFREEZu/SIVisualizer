from config import Config


def load(filepath):
    with open(filepath, 'r') as resultFile:
        result = resultFile.readlines()
    return result
