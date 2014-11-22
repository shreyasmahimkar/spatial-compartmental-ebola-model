from simulation import Simulation

if __name__ == '__main__':
    sim = Simulation()
    sim.load('../inputs/sl.json')
    sim.run()
