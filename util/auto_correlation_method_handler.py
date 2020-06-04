from util import time_delay_handler

def auto_correlation_integral(time_series, delay):
    series, delayed_series = time_delay_handler.get_same_length_series_and_delayed_series(time_series, delay)
    sum = 0
    for index in range(0, len(series)):
        sum += time_series[index] * delayed_series[index]
    return sum
