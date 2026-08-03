from src.waypoint_navigator import WaypointNavigator
from src.drone import DroneState
from src.vectors import Vector3
from src import constants
import pytest

def test_initial_state():
    #Arrange
    navigator = WaypointNavigator()

    # Act
    navigator.add_waypoint(Vector3(0, 0, 5))
    navigator.add_waypoint(Vector3(10, 0, 5))
    navigator.add_waypoint(Vector3(10, 10, 5))

    # Assert
    assert navigator.current_index == 0

def test_add_waypoints():
    # Arrange
    navigator = WaypointNavigator()

    # Act
    navigator.add_waypoint(Vector3(0, 0, 5))
    navigator.add_waypoint(Vector3(10, 0, 5))
    navigator.add_waypoint(Vector3(10, 10, 5))

    # Assert
    assert navigator.current_waypoint == Vector3(0, 0, 5)

def test_no_waypoints_returns_zero_thrust():
    # Arrange
    navigator = WaypointNavigator()

    # Act
    thrust = navigator.update(DroneState(Vector3(0, 0, 0)))

    # Assert
    assert thrust == Vector3(0, 0, 0)

def test_completed_returns_zero_thrust():
    # Arrange
    navigator = WaypointNavigator()

    # Act
    navigator.add_waypoint(Vector3(10, 10, 5))

    # Assert
    assert navigator.update(DroneState(Vector3(10, 10, 5))) == Vector3(0, 0, 0)

def test_advances_to_next_waypoint_when_close():
    # Arrange
    navigator = WaypointNavigator()

    # Act
    navigator.add_waypoint(Vector3(0, 0, 5))
    navigator.add_waypoint(Vector3(10, 0, 5))
    navigator.update(DroneState(Vector3(0, 0, 4.5)))

    # Assert
    assert navigator.current_index == 1

def test_thrust_points_toward_waypoint():
    # Arrange
    navigator = WaypointNavigator()

    # Act
    navigator.add_waypoint(Vector3(10, 0, 5))
    thrust = navigator.update(DroneState(Vector3(0, 0, 0)))

    # Assert
    assert thrust.x > 0

def test_hover_component_in_thrust():
    # Arrange
    navigator = WaypointNavigator()

    # Act
    navigator.add_waypoint(Vector3(10, 0, 5))
    thrust = navigator.update(DroneState(Vector3(0, 0, 0)))

    # Assert
    assert thrust.z >= 9.81
