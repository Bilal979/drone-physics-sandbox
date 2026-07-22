from src.vectors import Vector3
from src import constants

class PhysicsEngine:
    def __init__(self, gravity=constants.GRAVITY):
        self.gravity = gravity

    def compute_gravity(self, mass:float) -> Vector3:
        # force due to gravity
        force = mass * self.gravity
        return Vector3(0, 0, -1*force)

    def compute_drag(self, velocity:Vector3) -> Vector3:
        speed = velocity.magnitude()
        drag = velocity *(-constants.DRAG_COEFFICIENT * speed)
        return drag


    def compute_net_force(self, thrust:Vector3, mass:float, velocity:Vector3) -> Vector3:
        # thrust is a force
        #thrust_vector = Vector3(0, 0, thrust)
        drag = self.compute_drag(velocity)
        net_force = thrust + self.compute_gravity(mass) + drag
        return net_force

    def compute_acceleration(self, net_force:Vector3, mass:float) -> Vector3:
        acceleration = net_force/mass
        return acceleration

    



