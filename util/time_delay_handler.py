from point.point import Point
from point.point_list import PointList


def get_series_without_first_element(series, delay):
    result = series.copy()
    del result[0:delay]
    return result


def get_series_without_last_element(series, delay):
    result = series.copy()
    del result[-1*delay:]
    return result


def get_same_length_series_and_delayed_series(series, delay):
    return get_series_without_first_element(series, delay), get_series_without_last_element(series, delay)

def get_points_by_method_of_delay(series, delay):
    series, delayed_series = get_same_length_series_and_delayed_series(series, delay)
    point_list = []
    for index in range(len(series)):
        point_list.append(Point(series[index], delayed_series[index]))
    return PointList(point_list)
