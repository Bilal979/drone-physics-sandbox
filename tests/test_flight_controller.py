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
    # hover_thrust = flight_controller.update(2.0, DroneState())
    landing_thrust = flight_controller.update(4.0, DroneState(Vector3(0, 0, 1)))
    idle_thrust = flight_controller.update(4.0, DroneState())

    # Assert
    assert takeoff_thrust.z == constants.TAKEOFF_THRUST
    # assert hover_thrust.z == constants.HOVER_THRUST
    assert landing_thrust.z == constants.LANDING_THRUST
    assert idle_thrust.z == 0


def test_hover_holds_position_when_at_target():
    # drone is exactly at hover position with zero velocity
    # PD output should be near zero (no error, no velocity)
    fc = FlightController(constants.DEFAULT_MASS)
    fc.add_phase(0.0, FlightMode.HOVER)
    state = DroneState()
    state.position = Vector3(0, 0, 5)
    thrust = fc.update(0.0, state)   # sets hover_target = (0,0,5)
    # call again from same position — error is zero
    thrust2 = fc.update(0.1, state)
    assert abs(thrust2.z) < 0.1   # near zero, no correction needed

def test_hover_corrects_upward_when_below_target():
    # drone drops below hover target — thrust z should be positive
    fc = FlightController(constants.DEFAULT_MASS)
    fc.add_phase(0.0, FlightMode.HOVER)
    state_initial = DroneState()
    state_initial.position = Vector3(0, 0, 5)
    fc.update(0.0, state_initial)   # set hover target at z=5

    state_low = DroneState()
    state_low.position = Vector3(0, 0, 3)  # drone dropped to z=3
    thrust = fc.update(0.1, state_low)
    assert thrust.z > 0   # should push upward

def test_hover_damps_horizontal_velocity():
    # drone has horizontal velocity — thrust x should oppose it
    fc = FlightController(constants.DEFAULT_MASS)
    fc.add_phase(0.0, FlightMode.HOVER)
    state = DroneState()
    state.position = Vector3(0, 0, 5)
    fc.update(0.0, state)   # set hover target

    state_moving = DroneState()
    state_moving.position = Vector3(0, 0, 5)
    state_moving.velocity = Vector3(3, 0, 0)  # moving in +x
    thrust = fc.update(0.1, state_moving)
    assert thrust.x < 0   # D term should push in -x to brake




    