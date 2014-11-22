
class Connection:
    def __init__(self, data):
        self.origin = data[0]
        self.osm_id = data[1]
        self.destination = data[2]

        weight = data[3]
        if weight == 'unclassified':
            self.weight = 1
        elif weight == 'footway':
            self.weight = 1
        elif weight == 'service':
            self.weight = 1
        elif weight == 'residential':
            self.weight = 2
        elif weight == 'path':
            self.weight = 2
        elif weight == 'track':
            self.weight = 3
        elif weight == 'trunk':
            self.weight = 3
        elif weight == 'road':
            self.weight = 3 
        elif weight == 'tertiary':
            self.weight = 4
        elif weight == 'secondary':
            self.weight = 5
        elif weight == 'primary':
            self.weight = 7
        else:
            print('Unrecognized weight "' + weight + '"')


def load_road_csv(csv_filename):
    all_connections = []
    csv_fh = open(csv_filename, 'r')
    for line in csv_fh:
        data = line.strip().split(",")
        if data[0] and data[1] and data[2] and data[3]:
            new_conn = Connection(data)
            all_connections.append(new_conn)
    return all_connections
    

