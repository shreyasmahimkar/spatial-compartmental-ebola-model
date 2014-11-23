import numpy as np
from regionmodel import RegionModel

class CompartmentalModel(RegionModel):
    num_models = 0
    def __init__(self, population_params, ebola_params, model_params, first=False):
        self.id = CompartmentalModel.num_models
        CompartmentalModel.num_models += 1
        self.compartments = {i : 0 for i in ['S', 'E', 'I', 'R']}
        natural_mortality_rate = population_params['natural_mortality_rate']
        ebola_mortality_rate = ebola_params['disease_mortality_rate']
        self.transitions = {'S' : {'E' : 0, 'D' : natural_mortality_rate}, 
                            'E' : {'I' : 1 / ebola_params['mean_latent_period'], 'D' : natural_mortality_rate}, 
                            'I' : {'R' : 1 / ebola_params['mean_infective_period'], 'D' : ebola_mortality_rate}, 
                            'R' : {'D' : natural_mortality_rate}}
        self.total_cases = 0
        self.disease_deaths = 0
        self.compartments['R'] = int(population_params['natural_ebola_resistance'] * model_params['population_size'])
        self.compartments['S'] = model_params['population_size'] - self.compartments['R']
        self.compartments['I'] = 14 if first else 0
        self.effective_contact_rate = ebola_params['effective_contact_rate']
        self.birth_rate = population_params['birth_rate']
        self.natural_resistance = population_params['natural_ebola_resistance']

    def get_total_cases(self):
        return self.total_cases

    def update(self):
        deltas = {i : 0 for i in ['S', 'E', 'I', 'R', 'D']}

        self.transitions['S']['E'] = self.effective_contact_rate * self.calc_prevalence()

        births = int(self.birth_rate * self.population_size())
        resistant_births = int(births * self.natural_resistance)
        self.compartments['R'] += resistant_births
        self.compartments['S'] += (births - resistant_births)

        for source in self.transitions:
            trans_list = [(i, self.transitions[source][i]) for i in self.transitions[source]]
            props = [i[1] for i in trans_list]
            props.append(1 - sum(props))
            transitions = {i[0] : j for i, j in zip(trans_list, list(np.random.multinomial(self.compartments[source], props, size=1))[0])}

            for dest in transitions:
                delta = transitions[dest]
                if source != 'D': deltas[source] -= delta
                deltas[dest] += delta

                if source == 'I' and dest == 'D':
                    self.disease_deaths += delta
                if source == 'S' and dest == 'E':
                    self.total_cases += delta

        for compartment in self.compartments:
            self.compartments[compartment] += deltas[compartment]

    def calc_prevalence(self):
        return self.compartments['I'] / self.population_size()

    def population_size(self):
        return sum([self.compartments[i] for i in self.compartments])

