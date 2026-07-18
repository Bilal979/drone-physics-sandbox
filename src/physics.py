from src.vectors import Vector3
from src import constants

class PhysicsEngine:
    def __init__(self, gravity=constants.GRAVITY):
        self.gravity = gravity

    def compute_gravity(self, mass:float) -> Vector3:
        # force due to gravity
        force = mass * self.gravity
        return Vector3(0, 0, -1*force)

    def compute_net_force(self, thrust:float, mass:float) -> Vector3:
        # thrust is a force
        thrust_vector = Vector3(0, 0, thrust)
        net_force = thrust_vector + self.compute_gravity(mass)
        return net_force

    def compute_acceleration(self, net_force:Vector3, mass:float) -> Vector3:
        acceleration = net_force/mass
        return acceleration

    



