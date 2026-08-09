import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from src.flight_controller import FlightMode
from matplotlib.animation import FuncAnimation

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
                    'mode': row['drone_mode'],
                    'velocity_magnitude': float(row['velocity_magnitude'])
                })
    
    

    def animate(self, interval: int = 20, step: int = 5):
        """
        interval: ms between frames
        step: how many history entries to skip per frame (higher = faster playback)
        """
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # static waypoints
        if self.waypoints:
            wx = [w[0] for w in self.waypoints]
            wy = [w[1] for w in self.waypoints]
            wz = [w[2] for w in self.waypoints]
            ax.scatter(wx, wy, wz, color='red', s=80, zorder=5)

        # set fixed axis limits from full history
        all_x = [h['x'] for h in self.history]
        all_y = [h['y'] for h in self.history]
        all_z = [h['z'] for h in self.history]
        ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
        ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
        ax.set_zlim(0, max(all_z) + 1)

        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Drone Flight Animation')

        # drone marker and trail line
        drone_dot, = ax.plot([], [], [], 'o', color='black', markersize=8)
        trail, = ax.plot([], [], [], '-', color='blue', linewidth=1.5, alpha=0.6)
        time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

        def init():
            drone_dot.set_data([], [])
            drone_dot.set_3d_properties([])
            trail.set_data([], [])
            trail.set_3d_properties([])
            time_text.set_text('')
            return drone_dot, trail, time_text

        def update_frame(frame_idx):
            idx = min(frame_idx * step, len(self.history) - 1)
            subset = self.history[:idx + 1]

            xs = [h['x'] for h in subset]
            ys = [h['y'] for h in subset]
            zs = [h['z'] for h in subset]

            trail.set_data(xs, ys)
            trail.set_3d_properties(zs)

            drone_dot.set_data([xs[-1]], [ys[-1]])
            drone_dot.set_3d_properties([zs[-1]])

            current = self.history[idx]
            time_text.set_text(f"t={current['time']:.2f}s  mode={current['mode']} velocity={current['velocity_magnitude']:.2f}m/s")

            return drone_dot, trail, time_text

        frames = len(self.history) // step + 1
        anim = FuncAnimation(fig, update_frame, frames=frames,
                            init_func=init, interval=interval, blit=False)

        plt.tight_layout()
        plt.show()

    def animate_colored_trail(self, interval: int = 20, step: int = 5):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # static waypoints
        if self.waypoints:
            wx = [w[0] for w in self.waypoints]
            wy = [w[1] for w in self.waypoints]
            wz = [w[2] for w in self.waypoints]
            ax.scatter(wx, wy, wz, color='red', s=80, zorder=5)

        # fixed axis limits
        all_x = [h['x'] for h in self.history]
        all_y = [h['y'] for h in self.history]
        all_z = [h['z'] for h in self.history]
        ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
        ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
        ax.set_zlim(0, max(all_z) + 1)

        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Drone Flight Animation')

        drone_dot, = ax.plot([], [], [], 'o', color='black', markersize=8, zorder=10)
        time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)
        trail_lines = []  # keep track of drawn segments to clear them

        def init():
            drone_dot.set_data([], [])
            drone_dot.set_3d_properties([])
            time_text.set_text('')
            return drone_dot, time_text

        def update_frame(frame_idx):
            # clear previous trail segments
            while trail_lines:
                trail_lines.pop().remove()

            idx = min(frame_idx * step, len(self.history) - 1)
            subset = self.history[:idx + 1]

            # redraw trail segment by segment colored by mode
            for i in range(1, len(subset)):
                prev = subset[i - 1]
                curr = subset[i]
                color = MODE_COLORS.get(curr['mode'], 'black')
                line, = ax.plot(
                    [prev['x'], curr['x']],
                    [prev['y'], curr['y']],
                    [prev['z'], curr['z']],
                    color=color, linewidth=1.5, alpha=0.8
                )
                trail_lines.append(line)

            # update drone dot
            curr = subset[-1]
            drone_dot.set_data([curr['x']], [curr['y']])
            drone_dot.set_3d_properties([curr['z']])
            time_text.set_text(f"t={curr['time']:.2f}s  mode={curr['mode']} velocity={curr['velocity_magnitude']:.2f}m/s")

            return drone_dot, time_text

        frames = len(self.history) // step + 1
        anim = FuncAnimation(fig, update_frame, frames=frames,
                            init_func=init, interval=interval, blit=False)

        plt.tight_layout()
        plt.show()

    def save_gif(self, output_path: str = 'files/flight.gif', interval: int = 50, step: int = 8):
        """Save animation as GIF. Higher step = fewer frames = smaller file."""
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        if self.waypoints:
            wx = [w[0] for w in self.waypoints]
            wy = [w[1] for w in self.waypoints]
            wz = [w[2] for w in self.waypoints]
            ax.scatter(wx, wy, wz, color='red', s=80, zorder=5)

        all_x = [h['x'] for h in self.history]
        all_y = [h['y'] for h in self.history]
        all_z = [h['z'] for h in self.history]
        ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
        ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
        ax.set_zlim(0, max(all_z) + 1)
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Drone Flight Simulation')

        drone_dot, = ax.plot([], [], [], 'o', color='black', markersize=6, zorder=10)
        time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, fontsize=8)
        trail_lines = []

        def init():
            drone_dot.set_data([], [])
            drone_dot.set_3d_properties([])
            time_text.set_text('')
            return drone_dot, time_text

        def update_frame(frame_idx):
            while trail_lines:
                trail_lines.pop().remove()
            idx = min(frame_idx * step, len(self.history) - 1)
            subset = self.history[:idx + 1]
            for i in range(1, len(subset)):
                prev = subset[i - 1]
                curr = subset[i]
                color = MODE_COLORS.get(curr['mode'], 'black')
                line, = ax.plot(
                    [prev['x'], curr['x']],
                    [prev['y'], curr['y']],
                    [prev['z'], curr['z']],
                    color=color, linewidth=1.5, alpha=0.8
                )
                trail_lines.append(line)
            curr = subset[-1]
            drone_dot.set_data([curr['x']], [curr['y']])
            drone_dot.set_3d_properties([curr['z']])
            time_text.set_text(f"t={curr['time']:.2f}s  mode={curr['mode']} velocity={curr['velocity_magnitude']:.2f}m/s")
            return drone_dot, time_text

        frames = len(self.history) // step + 1
        anim = FuncAnimation(fig, update_frame, frames=frames,
                            init_func=init, interval=interval, blit=False)

        print(f"Saving GIF to {output_path} ...")
        anim.save(output_path, writer='pillow', fps=1000 // interval)
        plt.close()
        print("Done.")


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

