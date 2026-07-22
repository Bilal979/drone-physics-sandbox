from src.physics import PhysicsEngine
from src.vectors import Vector3
import pytest
from src import constants

def test_gravity_points_downward():
    # Arrange
    engine = PhysicsEngine()

    # Act
    gravity = engine.compute_gravity(1)

    # Assert
    assert gravity == Vector3(0, 0, -9.81)

def test_hover_thrust_produces_zero_net_force():
    # Arrange
    mass = constants.DEFAULT_MASS
    gravity = constants.GRAVITY
    
    # Act
    hover_thrust = constants.DEFAULT_MASS * constants.GRAVITY
    hover_thrust = Vector3(0, 0, hover_thrust)
    engine = PhysicsEngine()
    net_force = engine.compute_net_force(hover_thrust, mass, Vector3(0, 0, 0))

    # Assert
    assert net_force == Vector3(0, 0, 0)

def test_net_force_with_climb_thrust():
    # Arrange
    thrust_force = 15.0
    mass = constants.DEFAULT_MASS
    net_thrust_force = thrust_force - mass * constants.GRAVITY
    net_thrust_force = Vector3(0, 0, net_thrust_force)

    # Act
    engine = PhysicsEngine()
    net_force = engine.compute_net_force(Vector3(0, 0, thrust_force), mass, Vector3(0, 0, 0))

    # Assert
    assert net_force == net_thrust_force

def test_acceleration_equals_force_over_mass():
    # Arrange
    thrust_force = 15.0
    mass = constants.DEFAULT_MASS
    acceleration = thrust_force/mass

    # Act
    engine = PhysicsEngine()
    vector_acceleration = engine.compute_acceleration(net_force=Vector3(0, 0, thrust_force), mass=mass)

    # Assert
    assert vector_acceleration == Vector3(0, 0, acceleration)