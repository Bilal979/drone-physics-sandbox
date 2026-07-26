from src.drone import Drone
from src.simulation import Simulation
from src.vectors import Vector3
from src import constants
from src.flight_controller import FlightController
from src.flight_controller import FlightMode
import pytest

def test_simulation_history_length():
    # Arrange
    drone = Drone(constants.DEFAULT_MASS, Vector3(0,0,10.0))
    flight_controller = FlightController(constants.DEFAULT_MASS)
    sim = Simulation(drone, flight_controller, 0.02)

    # Act
    history = sim.run(1.0)

    # Assert
    assert len(history) == 50

def test_simulation_time_advances():
    # Arrange
    drone = Drone(constants.DEFAULT_MASS, Vector3(0,0,10.0))
    flight_controller = FlightController(constants.DEFAULT_MASS)
    sim = Simulation(drone, flight_controller, 0.02)

    # Act
    history = sim.run(1.0)

    # Assert
    assert history[-1]['time'] == pytest.approx(1.0)

def test_drone_climbs_with_high_thrust():
    # Arrange
    drone = Drone(mass=constants.DEFAULT_MASS, thrust=Vector3(0, 0, 100.0))
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(0.0, FlightMode.TAKEOFF)
    sim = Simulation(drone, flight_controller, 0.02)

    # Act
    history = sim.run(1.0)

    # Assert
    assert history[-1]['position'].z > 0

def test_drone_falls_with_zero_thrust():
    # Arrange
    drone = Drone(constants.DEFAULT_MASS, Vector3(0, 0, 0.0))
    flight_controller = FlightController(constants.DEFAULT_MASS)
    sim = Simulation(drone, flight_controller, 0.02)

    # Act
    history = sim.run(1.0)

    # Assert
    assert history[-1]['position'].z <= 0

def test_drone_hovers_with_balanced_thrust():
    # Arrange
    thrust = constants.DEFAULT_MASS * constants.GRAVITY
    drone = Drone(constants.DEFAULT_MASS, Vector3(0,0,thrust))
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(0.0, FlightMode.HOVER)
    sim = Simulation(drone, flight_controller)

    # Act
    history = sim.run(1.0)

    # Assert
    assert history[-1]['position'].z == pytest.approx(0.0)


