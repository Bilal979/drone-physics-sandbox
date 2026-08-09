from src.drone import Drone
from src.simulation import Simulation
from src.vectors import Vector3
from src.flight_controller import FlightController, FlightMode
from src import constants
from src.waypoint_navigator import WaypointNavigator
from src.visualizer import Visualizer

waypoints = [
    Vector3(2, 2, 5),
    Vector3(4, 4, 5),
    Vector3(10, 10, 5),
    Vector3(0, 10, 5),
    Vector3(0, 3, 5),
]

def main():
    # 1 create drone with default mass and thrust
    drone = Drone(constants.DEFAULT_MASS)

    # 2 initialize way point navigator
    navigator = WaypointNavigator()
    for waypoint in waypoints:
        navigator.add_waypoint(waypoint)

    # 2 Initialize flight controller
    flight_controller = FlightController(constants.DEFAULT_MASS, navigator=navigator)

    # 3 Add phases to the flight controller
    flight_controller.add_phase(0.0, FlightMode.TAKEOFF)
    flight_controller.add_phase(2.0, FlightMode.HOVER)
    flight_controller.add_phase(4.0, FlightMode.NAVIGATE)
    # flight_controller.add_phase(4.0, FlightMode.LANDING)
    # flight_controller.add_phase(6.0, FlightMode.IDLE)


    # 2 create simulation with the drone
    sim = Simulation(drone, flight_controller, constants.DEFAULT_DT)

    # 3 run simulation
    history = sim.run(27.0)

    # 4 print history
    # for state in history:
    #     print(f"Time: {state['time']:.2f} Position: {state['position']}")

    # 5 expot history to csv
    sim.export_csv("files/history.csv")

    # 6 visualize history
    vis = Visualizer(csv_path="files/history.csv", waypoints=[(waypoint.x, waypoint.y, waypoint.z) for waypoint in waypoints])
    # vis.plot_path()
    vis.animate()

    # 7 save animation as gif
    vis.save_gif('files/flight.gif')
    
if __name__ == "__main__":
    main()