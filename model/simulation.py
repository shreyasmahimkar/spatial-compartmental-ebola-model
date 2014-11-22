
from region import Region
from connection import Connection

def road_type_to_weight(type):
    weight = 0
    if type == 'unclassified':
        weight = 1
    elif type == 'footway':
        weight = 1
    elif type == 'service':
        weight = 1
    elif type == 'residential':
        weight = 2
    elif type == 'path':
        weight = 2
    elif type == 'track':
        weight = 3
    elif type == 'trunk':
        weight = 3
    elif type == 'road':
        weight = 3 
    elif type == 'tertiary':
        weight = 4
    elif type == 'secondary':
        weight = 5
    elif type == 'primary':
        weight = 7
    else:
        print('Unrecognized road type: "' + type + '"')
        
    return weight            
    

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

        roads = self.load_road_csv('../inputs/conn.csv')

        for origin in self.regions:
            for destination in self.regions:
                if origin == destination: continue
                sum_connections = 0
                for road in roads:
                    if road[0] == origin.name and road[2] == destination.name:
                        sum_connections += road_type_to_weight(road[3])
                if(sum_connections > 0):
                    conn = Connection(origin, destination, sum_connections)
                    self.connections.append(conn)

    def load_road_csv(self, csv_filename):
        csv_fh = open(csv_filename, 'r')
        return [line.strip().split(",") for line in csv_fh]

    def print_summary(self):
        print('Day {}: '.format(self.time))

        for region in self.regions:
            region.print_state()

        print()

    def run(self):
        self.time = 0

        while(self.time < self.duration):
            for connection in self.connections:
                connection.calc_migrations(0.0001)

            for connection in self.connections:
                connection.complete_migrations()

            for region in self.regions:
                region.update()

            self.print_summary()

            self.time += 1

