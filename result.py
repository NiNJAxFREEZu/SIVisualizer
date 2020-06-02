from config import Config


class Result:

    def load(filepath):
        with open(filepath, 'r') as resultFile:
            result = resultFile.readlines()
        return result
