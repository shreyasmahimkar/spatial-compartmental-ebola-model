import numpy as np

class Connection:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.migrations = {i : 0 for i in ['S', 'E', 'I', 'R']}
        print(self.weight)

    def calc_migrations(self, global_migration_rate):
        for compartment in ['S', 'E', 'I', 'R']:
            props = [self.weight * global_migration_rate * self.origin.model.compartments[compartment] / self.origin.population_size()]
            props.append(1 - props[0])
            self.migrations[compartment] = np.random.multinomial(self.origin.model.compartments[compartment], props, size=1)[0][0]

    def complete_migrations(self):
        for compartment in ['S', 'E', 'I', 'R']:
            self.origin.model.compartments[compartment] -= self.migrations[compartment]
            self.origin.model.compartments[compartment] = max(0, self.origin.model.compartments[compartment])
            self.destination.model.compartments[compartment] += self.migrations[compartment]
            self.destination.model.compartments[compartment] = max(0, self.destination.model.compartments[compartment])

        


