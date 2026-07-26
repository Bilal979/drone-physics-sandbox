from src.drone import Drone
from src.simulation import Simulation
from src.vectors import Vector3
from src.flight_controller import FlightController, FlightMode
from src import constants

def main():
    # 1 create drone with default mass and thrust
    drone = Drone(constants.DEFAULT_MASS, Vector3(0, 0, 0.0))

    # 2 Initialize flight controller
    flight_controller = FlightController(constants.DEFAULT_MASS)

    # 3 Add phases to the flight controller
    flight_controller.add_phase(0.0, FlightMode.TAKEOFF)
    flight_controller.add_phase(2.0, FlightMode.HOVER)
    flight_controller.add_phase(4.0, FlightMode.LANDING)
    flight_controller.add_phase(6.0, FlightMode.IDLE)


    # 2 create simulation with the drone
    sim = Simulation(drone, flight_controller, constants.DEFAULT_DT)

    # 3 run simulation
    history = sim.run(8.0)

    # 4 print history
    for state in history:
        print(f"Time: {state['time']:.2f} Position: {state['position']}")

    
if __name__ == "__main__":
    main()