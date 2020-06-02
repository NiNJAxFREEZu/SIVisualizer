class Result:
    result = ""

    def load(self, filepath):
        with open(filepath, 'r') as resultFile:
            self.result = resultFile.readlines()