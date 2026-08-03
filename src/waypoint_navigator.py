from src.vectors import Vector3
from src.drone import DroneState
from src import constants

class WaypointNavigator:
    def __init__(self):
        self.waypoints = []
        self.current_index = 0
        self.completed = False

    def add_waypoint(self, waypoint: Vector3):
        self.waypoints.append(waypoint)

    @property
    def current_waypoint(self) -> Vector3:
        if self.completed:
            return None
        return self.waypoints[self.current_index]

    def update(self, drone_state: DroneState) -> Vector3:
        # compute and return thrust towards current waypoint

        # if completed return 0 thrust
        if self.completed:
            return Vector3(0, 0, 0) 

        # check if drone is within waypoint tolerance
        distance = (self.current_waypoint - drone_state.position).magnitude()
        if distance <= constants.WAYPOINT_TOLERANCE:
            if self.current_index == len(self.waypoints) - 1:
                self.completed = True
                return Vector3(0, 0, 0)

            self.current_index += 1
        
        # compute thrust/steering toawrds current waypoint
        return self._compute_thrust(drone_state.position, self.current_waypoint)


    def _compute_thrust(self, position: Vector3, waypoint: Vector3) -> Vector3:
        # compute thrust to waypoint
        direction = (waypoint - position).normalize()
        steering_thrust = direction * constants.CRUISE_THRUST
        
        # get hover thrust
        hover_thrust = Vector3(0, 0, constants.HOVER_THRUST)

        # compute total Thrust
        total_thrust = steering_thrust + hover_thrust
        
        return total_thrust

        