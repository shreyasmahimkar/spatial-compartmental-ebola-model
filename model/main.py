from simulation import Simulation

if __name__ == '__main__':
    for i in range(100):
        sim = Simulation()
        sim.load('../inputs/sl.json')
        sim.run()
