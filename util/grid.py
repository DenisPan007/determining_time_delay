from point.point import Point


class Grid:
    """Needed to store points on they positions on grid"""
    grid_interval = 0
    x_boundary_left = 0
    x_boundary_right = 0
    y_boundary_bottom = 0
    y_boundary_top = 0

    def __init__(self, x_boundaries, y_boundaries, amount_of_intervals):
        self.structured_grid_points = []
        self.x_boundary_left, self.x_boundary_right = x_boundaries
        self.y_boundary_bottom, self.y_boundary_top = y_boundaries
        self.grid_interval = self.get_grid_interval(amount_of_intervals, x_boundaries, y_boundaries)
        self.set_grid_points()

    def set_grid_points(self):
        x = self.x_boundary_left
        y = self.y_boundary_bottom
        # from left
        x_position_index = 0
        while x < self.x_boundary_right:
            # from bottom
            self.structured_grid_points.append([])
            while y < self.y_boundary_top:
                self.structured_grid_points[x_position_index].append(Point(x, y))
                y += self.grid_interval
            x += self.grid_interval
            y = self.y_boundary_bottom
            x_position_index += 1

    def get_grid_interval(self, amount_of_intervals, x_boundaries, y_boundaries):
        x_boundary_left, x_boundary_right = x_boundaries
        y_boundary_left, y_boundary_right = y_boundaries
        x_interval = abs(x_boundary_right - x_boundary_left) / amount_of_intervals
        y_interval = abs(y_boundary_right - y_boundary_left) / amount_of_intervals
        interval = min(x_interval, y_interval)
        return interval
