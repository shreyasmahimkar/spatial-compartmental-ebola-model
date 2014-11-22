import sys

class Node:

    def __init__(self, name, json_file):
        self.name = name
        self.population = 0
        self.load_json_file(json_file)
        self.state = "Susceptible"
        

    def change_state(self, state):
        self.state = state

    def set_population(self, population):
        self.population = population

    def load_json_file(self, filename):
        import json
        try:
            data = json.loads(open(filename).read())

            for region in data['regions']:
                self.regions.append(Region(region))

            for connection in data['connection']:
                self.connections.append(Connection(self.regions, connection))

        except IOError:
            print("Error: can't find the json file or read the data")



            
