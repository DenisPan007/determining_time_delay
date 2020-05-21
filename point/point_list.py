class PointList:
    point_list = []

    def __init__(self, point_list):
        self.point_list = point_list

    def get_x_boundaries(self):
        series = self.get_x_series()
        return min(series), max(series)

    def get_y_boundaries(self):
        series = self.get_y_series()
        return min(series), max(series)

    def get_x_series(self):
        series = []
        for point in self.point_list:
            series.append(point.x)
        return series

    def get_y_series(self):
        series = []
        for point in self.point_list:
            series.append(point.y)
        return series
