from region import Region
from connection import Connection

class Simulation:
    def __init__(self):
        self.regions = []
        self.connections = []

    def load(self, filename):
        import json
        data = json.loads(open('../inputs/sl.json').read())

        for region in data['regions']:
            self.regions.append(Region(region, data['population_params'], data['ebola_params'], data['regions'][region]))

        self.duration = data['duration']

    def print_summary(self):
        print('Day {}: '.format(self.time))

        for region in self.regions:
            region.print_state()

        print()

    def run(self):
        self.time = 0

        while(self.time < self.duration):
            for connection in self.connections:
                connection.update()

            for region in self.regions:
                region.update()

            self.print_summary()

            self.time += 1

