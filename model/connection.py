import numpy as np

class Connection:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
#        print(origin.name, destination.name, weight)
        self.weight = weight
        self.migrations = {i : 0 for i in ['E', 'I']}

    def calc_migrations(self, global_migration_rate):
        force = global_migration_rate * self.origin.population_size() * self.destination.population_size() / (self.weight ** 2)

        for compartment in ['E', 'I']:
            prop = min(0.9, force * self.origin.model.compartments[compartment] / self.origin.population_size())
            props = [prop, 1 - prop]
            self.migrations[compartment] = np.random.multinomial(self.origin.model.compartments[compartment], props, size=1)[0][0]

    def complete_migrations(self):
        for compartment in ['E', 'I']:
            self.origin.model.compartments[compartment] -= self.migrations[compartment]
            self.origin.model.compartments[compartment] = max(0, self.origin.model.compartments[compartment])
            self.destination.model.compartments[compartment] += self.migrations[compartment]
            self.destination.model.compartments[compartment] = max(0, self.destination.model.compartments[compartment])

        


