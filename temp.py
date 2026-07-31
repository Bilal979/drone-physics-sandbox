from src.drone import Drone
from src.simulation import Simulation
from src import constants

drone = Drone(constants.DEFAULT_MASS)
sim = Simulation(drone, constants.DEFAULT_DT)
history = sim.run(2.0)
print(history[19])
