from dataclasses import dataclass, field
from src.vectors import Vector3
from src import constants

@dataclass
class DroneState:
    position: Vector3= field(default_factory=lambda: Vector3(0,0,0))
    velocity: Vector3= field(default_factory=lambda: Vector3(0,0,0))
    acceleration: Vector3= field(default_factory=lambda: Vector3(0,0,0))


class Drone:
    def __init__(self, mass, thrust):
        self.mass = mass
        self.thrust = thrust
        self.state = DroneState()


    def set_thrust(self, thrust):
        self.thrust = thrust

    def apply_force(self, force: Vector3):
        self.state.acceleration = force/self.mass

    def update(self, dt):
        # update velocity and position using current acceleration
        self.state.velocity = self.state.velocity + self.state.acceleration*dt
        self.state.position = self.state.position + self.state.velocity*dt

