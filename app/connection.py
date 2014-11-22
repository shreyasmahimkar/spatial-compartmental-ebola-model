
class Connection:
    def __init__(self, regions, definition):
        self.from = definition[0]
        self.to = definition[1]
        self.weight = definition[2]

