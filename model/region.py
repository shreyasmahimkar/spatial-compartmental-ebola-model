from compartmentalmodel import CompartmentalModel

class Region:
    def __init__(self, name, population_params, ebola_params, region_params):
        self.name = name
        self.model = CompartmentalModel(population_params, ebola_params, region_params, name == 'Kenema')

    def print_state(self):
        print(self.name, self.model.compartments, self.population_size(), self.model.get_total_cases(), self.model.disease_deaths)

    def update(self):
        self.model.update()

    def calc_prevalence(self):
        return self.model.calc_prevalence()

    def population_size(self):
        return self.model.population_size()

if __name__ == '__main__':
    import json
    data = json.loads(open('../inputs/sl.json').read())

    region = Region('Bo', data['population_params'], data['ebola_params'], data['regions']['Bo'])
    region.print_state()

    for i in range(100):
        region.update()
        print('Day {}: '.format(i), end='')
        region.print_state()
