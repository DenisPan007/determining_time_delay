import math

import numpy as np

from util import time_delay_handler


def get_scale_from_series(series, number_of_intervals=10):
    scale = []
    maximum = max(series)
    minimum = min(series)
    interval = (maximum - minimum) / number_of_intervals

    index = minimum
    while index <= maximum:
        scale.append(index)
        index += interval
    return scale


def get_marginal_probability(x, scale):
    return np.histogram(x, scale)[0]


def get_joint_probability(x, y, scale):
    """The result is a grid: vertical is x scale, horizontal is y scale;:
    sum of vertical columns is y marginal probability (not normalized)
    sum of horizontal columns is x marginal probability (not normalized)
    given x = [1,2,3,4,5], y = [1,1,1,3,4] and scale = [1,2,3,4,5]
    result:
       1  2  3  4
    1  1  0  0  0
    2  1  0  0  0
    3  1  0  0  0
    4  0  0  1  1
    """
    return np.histogram2d(x, y, scale)[0]


def mutual_information(x, y):
    scale = get_scale_from_series(x)
    p_x = get_marginal_probability(x, scale)
    p_y = get_marginal_probability(y, scale)
    p_xy = get_joint_probability(x, y, scale)
    p_x_normalized = p_x/ sum(p_x)
    p_y_normalized = p_y/sum(p_y)
    p_xy_normalized = p_xy/np.sum(p_xy)

    mutual_sum = 0
    for i in range(len(p_x_normalized)):
        for j in range(len(p_y_normalized)):
            px = p_x_normalized[i]
            py = p_y_normalized[j]
            pxy = p_xy_normalized[i][j]
            if px != 0 and py != 0 and pxy != 0:
                mutual_sum += pxy * math.log2(pxy / (px * py))
    return mutual_sum

def mutual_information_from_series(time_series, delay):
    series, delayed_series = time_delay_handler.get_same_length_series_and_delayed_series(time_series, delay)
    return mutual_information(series, delayed_series)