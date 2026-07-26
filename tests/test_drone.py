from src.drone import Drone
from src.vectors import Vector3
import pytest
from src import constants

def test_drone_initial_state():
    # Arrange
    position = Vector3(0, 0, 0)
    velocity = Vector3(0, 0, 0)
    acceleration = Vector3(0, 0, 0)
    mass = constants.DEFAULT_MASS
    thrust = (0,0,10)

    # Act
    drone = Drone(mass, thrust)

    # Assert
    assert drone.state.position == position
    assert drone.state.velocity == velocity
    assert drone.state.acceleration == acceleration

def test_set_thrust():
    # Arrange
    thrust = (0,0,10.0)
    mass = constants.DEFAULT_MASS

    # Act
    drone = Drone(mass, thrust)
    drone.set_thrust(thrust)

    # Assert
    assert drone.thrust == thrust

def test_apply_force_sets_acceleration():
    # Arrange
    mass = 2.0
    thrust = 10.0
    force = Vector3(0, 0, thrust)

    # Act
    drone = Drone(mass, thrust)
    drone.apply_force(force)

    # Assert
    assert drone.state.acceleration == Vector3(0, 0, thrust/mass)

def test_update_changes_velocity():
    # Arrange
    mass = 2.0
    thrust = 10.0
    force = Vector3(0, 0, thrust)

    # Act
    drone = Drone(mass, thrust)
    drone.apply_force(force)
    drone.update(1.0)

    # Assert
    assert drone.state.velocity == Vector3(0, 0, thrust/mass)


def test_update_changes_position():
    # Arrange
    mass = 1.0
    thrust = 10.0
    force = Vector3(0, 0, thrust)

    # Act
    drone = Drone(mass, thrust)
    drone.apply_force(force)
    drone.update(1.0)

    # Assert
    assert drone.state.position == Vector3(0, 0, thrust/mass)

def test_ground_constraint():           # Drone with 0 thrust should not fall below z=0
    # Arrange
    drone = Drone(mass=1.0,thrust=Vector3(0,0,0.0))

    # Act
    for _ in range(100):
        drone.apply_force(Vector3(0, 0, -9.81))  # gravity
        drone.update(0.02)

    # Assert
    assert drone.state.position.z >= 0
    assert drone.state.velocity.z >= 0





