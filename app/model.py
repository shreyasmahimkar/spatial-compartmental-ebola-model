
class Model:
    def __init__(self):
        pass

    def load(self, filename):
        import json
        data = json.loads(open(filename).read())

        for region in data['regions']:
            self.regions.append(Region(region))

        for connection in data['connection']:
            self.connections.append(Connection(self.regions, connection))



            
