
from region import Region
from connection import Connection

def road_type_to_weight(type):
    weight = 0
    if type == 'unclassified':
        weight = 2
    elif type == 'footway':
        weight = 1
    elif type == 'service':
        weight = 1
    elif type == 'residential':
        weight = 10
    elif type == 'path':
        weight = 3
    elif type == 'track':
        weight = 2
    elif type == 'trunk':
        weight = 1
    elif type == 'road':
        weight = 1 
    elif type == 'tertiary':
        weight = 2
    elif type == 'secondary':
        weight = 2
    elif type == 'primary':
        weight = 6
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
#                    print(sum_connections)
                    conn = Connection(origin, destination, 0.1)#502 - sum_connections)
                    self.connections.append(conn)

    def load_road_csv(self, csv_filename):
        csv_fh = open(csv_filename, 'r')
        return [line.strip().split(",") for line in csv_fh]

    def print_summary(self, short=False):
        if short:
            for region in sorted(self.regions, key=lambda r: r.name):
                print(region.model.total_cases,end='\t')
#                print(region.name, end=',')
            print()
        else:
            print('Day {}: '.format(self.time))

            for region in sorted(self.regions, key=lambda r: r.name):
                region.print_state()

            print()

    def run(self):
        self.time = 0

        while(self.time < self.duration):
            for connection in self.connections:
                connection.calc_migrations(0.0001)

            for connection in self.connections:
                connection.complete_migrations()

            if self.time == 1: #5/26
                [i for i in self.regions if i.name in ['Kenema', 'Kailahun']][0].model.compartments['I'] += 1

            if self.time == 16: # 6/10
                [i for i in self.regions if i.name in ['Bo', 'Bombali', 'Bonthe', 'Kono', 'Moyamba', 'Port Loko', 'Pujehun', 'Tonkolili', 'Western Area Rural', 'Western Area Urban']][0].model.compartments['I'] += 1

            if self.time == 108: #9/10
                [i for i in self.regions if i.name == 'Kambia'][0].model.compartments['I'] += 1

            if self.time == 142: #10/14
                [i for i in self.regions if i.name == 'Koinadugu'][0].model.compartments['I'] += 1

            for region in self.regions:
                region.update()

#            self.print_summary(True)

            self.time += 1

        self.print_summary(True)
