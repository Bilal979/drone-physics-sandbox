from src.drone import Drone
from src.simulation import Simulation
from src import constants

def main():
    # 1 create drone with default mass and thrust
    drone = Drone(constants.DEFAULT_MASS, 15.0)

    # 2 create simulation with the drone
    sim = Simulation(drone, constants.DEFAULT_DT)

    # 3 run simulation
    history = sim.run(1.0)

    # 4 print history
    for state in history:
        print(f"Time: {state['time']:.2f} Position: {state['position']}")

    
if __name__ == "__main__":
    main()