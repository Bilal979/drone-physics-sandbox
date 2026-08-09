import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from src.flight_controller import FlightMode

# Color per flight mode
MODE_COLORS = {
    'takeoff':  'green',
    'hover':    'yellow',
    'navigate': 'blue',
    'landing':  'orange',
    'idle':     'gray',
}

class Visualizer:
    def __init__(self, csv_path: str, waypoints: list=None):
        self.csv_path = csv_path
        self.waypoints = waypoints or []
        self.history = []
        self._load_csv()

    def _load_csv(self):
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.history.append({
                    'time': float(row['time']),
                    'x': float(row['position_x']),
                    'y': float(row['position_y']),
                    'z': float(row['position_z']),
                    'mode': row['drone_mode']
                })

    def plot_path(self):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # draw trail segment by segment, colored by mode
        for i in range(1, len(self.history)):
            prev = self.history[i - 1]
            curr = self.history[i]
            color = MODE_COLORS.get(curr['mode'], 'black')
            ax.plot(
                [prev['x'], curr['x']],
                [prev['y'], curr['y']],
                [prev['z'], curr['z']],
                color=color, linewidth=1.5
            )

        # draw waypoints
        if self.waypoints:
            wx = [w[0] for w in self.waypoints]
            wy = [w[1] for w in self.waypoints]
            wz = [w[2] for w in self.waypoints]
            ax.scatter(wx, wy, wz, color='red', s=80, zorder=5, label='Waypoints')

        # mark start and end
        ax.scatter(*[self.history[0]['x']], *[self.history[0]['y']], *[self.history[0]['z']],
                   color='lime', s=100, label='Start')
        ax.scatter(*[self.history[-1]['x']], *[self.history[-1]['y']], *[self.history[-1]['z']],
                   color='black', s=100, label='End')

        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Drone Flight Path')
        ax.legend()
        plt.tight_layout()
        plt.show()

