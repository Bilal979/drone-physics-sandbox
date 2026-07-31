from src.flight_controller import FlightController, FlightMode
from src.drone import DroneState
from src.vectors import Vector3
from src import constants
import pytest

def test_default_mode_is_idle():
    # Arrange
    flight_controller = FlightController(constants.DEFAULT_MASS)

    # Act
    mode = flight_controller.mode

    # Assert
    assert mode == FlightMode.IDLE

def test_time_based_phase_transition():
    # Arrange
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(0.0, FlightMode.TAKEOFF)

    # Act
    flight_controller.update(1.0, DroneState())

    # Assert
    assert flight_controller.mode == FlightMode.TAKEOFF


def test_multiple_phases_apply_in_order():
    # Arrange
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(0.0, FlightMode.TAKEOFF)
    flight_controller.add_phase(2.0, FlightMode.HOVER)

    # Act
    flight_controller.update(2.0, DroneState())

    # Assert
    assert flight_controller.mode == FlightMode.HOVER

def test_landing_transition_to_idle_on_ground():
    # Arrange
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(4.0, FlightMode.LANDING)

    # Act
    flight_controller.update(4.0, DroneState())

    # Assert
    assert flight_controller.mode == FlightMode.IDLE

def test_landing_does_not_transition_if_airborne():
    # Arrange
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(4.0, FlightMode.LANDING)

    # Act
    flight_controller.update(4.0, DroneState(Vector3(0, 0, 1)))

    # Assert
    assert flight_controller.mode == FlightMode.LANDING

def test_thrust_for_each_mode():
    # Arrange
    flight_controller = FlightController(constants.DEFAULT_MASS)
    flight_controller.add_phase(0.0, FlightMode.TAKEOFF)
    flight_controller.add_phase(2.0, FlightMode.HOVER)
    flight_controller.add_phase(4.0, FlightMode.LANDING)

    # Act
    takeoff_thrust = flight_controller.update(0.0, DroneState())
    hover_thrust = flight_controller.update(2.0, DroneState())
    landing_thrust = flight_controller.update(4.0, DroneState(Vector3(0, 0, 1)))
    idle_thrust = flight_controller.update(4.0, DroneState())

    # Assert
    assert takeoff_thrust.z == constants.TAKEOFF_THRUST
    assert hover_thrust.z == constants.HOVER_THRUST
    assert landing_thrust.z == constants.LANDING_THRUST
    assert idle_thrust.z == 0



    