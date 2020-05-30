import pandas

from point.point import Point
from point.point_list import PointList


def get_points_list_from_csv(file_path):
    col_list = ["t", "x(t)", "y(t)"]
    result = pandas.read_csv(file_path, usecols=col_list)
    x = result["x(t)"]
    y = result["y(t)"]
    t = result["t"]
    points_list = []
    for index in t:
        points_list.append(Point(x.get(index), y.get(index)))
    return PointList(points_list)

def get_series_from_csv(file_path):
    col_list = ["t", "x(t)"]
    result = pandas.read_csv(file_path, usecols=col_list)
    x = result["x(t)"]
    t = result["t"]
    series = []
    for index in t:
        series.append(x.get(index))
    return series
