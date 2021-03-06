import matplotlib.pyplot as plt
import numpy

from util import file_parser, time_delay_handler, auto_correlation_method_handler, mutual_information_handler
from util.grid import Grid


def plot_attractor_with_border_cells_and_outer_square(grid_cell_points, cell_points_of_figure_boarder, grid_interval,
                                                      data_point_list):
    ax = plt.figure().gca()
    #  plot.add_grid_lines(ax, g#rid_cell_points, grid_interval)
    #   plot.add_cells_contains_points(ax, cell_points_of_figure_boarder, grid_interval)
    # plot.add_outer_of_figure_border(ax, outer_cells, grid_interval)
    plt.plot(data_point_list.get_x_series(), data_point_list.get_y_series(), 'ro', markersize=2)
    plt.xlabel('Time series')
    plt.ylabel('Delayed time series')

def plot_auto_correlation_depends_on_delay(delay_array, auto_correlation_array):
    fig = plt.figure()
    plt.xlabel('Delay (relative)')
    plt.ylabel('Auto-correlation integral (relative)')
    plt.title('Auto-correlation function')
    plt.plot(delay_array, auto_correlation_array, 'ko', markersize=6)


def plot_mutual_information_depends_on_delay(delay_array, mutual_information_array):
    fig = plt.figure()
    plt.xlabel('Delay (relative)')
    plt.ylabel('Mutual information (relative)')
    plt.title('Mutual information function')
    plt.plot(delay_array, mutual_information_array, 'go', markersize=6)


def is_grid_cell_contains_point(cell_left_bottom_coordinates, points_list, interval):
    x_cell, y_cell = cell_left_bottom_coordinates
    for point in points_list:
        if (x_cell <= point.x <= x_cell + interval
                and y_cell <= point.y <= y_cell + interval):
            return 1
    return 0


def plot_methods_of_choosing_delay(delay_array, graphic_method_array, correlation_method_array, mutual_info_array):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax1.set_xlabel('Delay')

    ax1.set_ylabel('Square of attractor (relative)')
    p1, = ax1.plot(delay_array, graphic_method_array, 'ro',label='Graphic', markersize=6)

    ax2.set_ylabel('Auto-correlation (relative)')
    p2, = ax2.plot(delay_array, [el / 1000 for el in correlation_method_array], 'bo', label='Auto-correlation', markersize=6)

    ax3.set_ylabel('Mutual information (relative)')
    p3, = ax3.plot(delay_array, mutual_info_array, 'go', label='Mutual information', markersize=6)

    plots = [p1, p2, p3]
    ax1.legend(handles=plots, loc='center right')

    ax2.spines['right'].set_position(('outward', 60))

    ax1.yaxis.label.set_color(p1.get_color())
    ax2.yaxis.label.set_color(p2.get_color())
    ax3.yaxis.label.set_color(p3.get_color())

def get_grid_points_whose_cells_contains_data_points(data_point_list, grid_points, grid_interval):
    result = []
    for point in grid_points:
        cell_bottom_coordinates = (point.x, point.y)
        if is_grid_cell_contains_point(cell_bottom_coordinates, data_point_list.point_list, grid_interval):
            result.append(point)
    return result


def is_cell_belongs_to_the_figure_border(point, border_points):
    return point in border_points


def get_cell_points_out_of_figure_border(grid, figure_border_cells):
    structured_grid_points = grid.structured_grid_points

    # strike points from bottom to top
    outer_points_bottom = get_outer_points_striking_from_top_down(range(len(structured_grid_points)),
                                                                  range(len(structured_grid_points[0])),
                                                                  figure_border_cells,
                                                                  structured_grid_points)
    # strike points from top to bottom
    outer_points_top = get_outer_points_striking_from_top_down(
        range(len(structured_grid_points)),
        range(len(structured_grid_points[0]) - 1, 0, -1),
        figure_border_cells,
        structured_grid_points)

    outer_points_left = get_outer_points_striking_from_sides(
        range(len(structured_grid_points) - 1),
        range(len(structured_grid_points[0])),
        figure_border_cells,
        structured_grid_points)

    outer_points_right = get_outer_points_striking_from_sides(
        range(len(structured_grid_points) - 1, -1, -1),
        range(len(structured_grid_points[0])),
        figure_border_cells,
        structured_grid_points)

    return set(outer_points_left + outer_points_right + outer_points_top + outer_points_bottom)


def get_outer_points_striking_from_top_down(x_range, y_range, figure_boundary_cells,
                                            structured_grid_points):
    return get_outer_points_iterating_from_one_grid_side(x_range, y_range, figure_boundary_cells,
                                                         structured_grid_points, 1)


def get_outer_points_striking_from_sides(x_range, y_range, figure_boundary_cells,
                                         structured_grid_points):
    return get_outer_points_iterating_from_one_grid_side(y_range, x_range, figure_boundary_cells,
                                                         structured_grid_points, 0)


def get_outer_points_iterating_from_one_grid_side(outer_loop_coordinate_range, inner_loop_coordinate_range,
                                                  figure_boundary_cell_points,
                                                  structured_grid_points, is_outer_coordinate_is_x):
    outer_points = []
    for outer_coordinate_index in outer_loop_coordinate_range:
        for inner_coordinate_index in inner_loop_coordinate_range:
            if is_outer_coordinate_is_x:
                point = structured_grid_points[outer_coordinate_index][inner_coordinate_index]
            else:
                point = structured_grid_points[inner_coordinate_index][outer_coordinate_index]

            if not is_cell_belongs_to_the_figure_border(point, figure_boundary_cell_points):
                outer_points.append(point)
            else:
                break
    return outer_points


# data_point_list = file_parser.get_points_list_from_csv('chua_series.csv')

x_series = file_parser.get_series_from_csv('chua_series.csv')
square_depends_on_delay = []
auto_correlation_depends_on_delay_array = []
mutual_information_depends_on_delay_array = []
delay_array = []
for delay in range(1, 150):
    data_point_list = time_delay_handler.get_points_by_method_of_delay(x_series, delay)
    grid = Grid(data_point_list.get_x_boundaries(), data_point_list.get_y_boundaries(), 20)
    grid_cell_points = list(numpy.concatenate(grid.structured_grid_points))
    cell_points_of_figure_boarder = get_grid_points_whose_cells_contains_data_points(data_point_list,
                                                                                     grid_cell_points,
                                                                                     grid.grid_interval)
    outer_cells = get_cell_points_out_of_figure_border(grid, cell_points_of_figure_boarder)
    grid_square = len(grid_cell_points)
    out_of_figure_square = len(outer_cells)
    square = (grid_square - out_of_figure_square) / grid_square
    square_depends_on_delay.append(square)
    delay_array.append(delay)

    auto_correlation_depends_on_delay_array.append(
        auto_correlation_method_handler.auto_correlation_integral(x_series, delay))
    mutual_information_depends_on_delay_array.append(
        mutual_information_handler.mutual_information_from_series(x_series, delay)
    )

plot_methods_of_choosing_delay(delay_array, square_depends_on_delay, auto_correlation_depends_on_delay_array, mutual_information_depends_on_delay_array)

plot_attractor_with_border_cells_and_outer_square(grid_cell_points, cell_points_of_figure_boarder, grid.grid_interval,
                                                  data_point_list)
plt.show()
