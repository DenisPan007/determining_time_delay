import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy

from util import file_parser
from util.grid import Grid


def is_grid_cell_contains_point(cell_left_bottom_coordinates, points_list, interval):
    x_cell, y_cell = cell_left_bottom_coordinates
    for point in points_list:
        if (x_cell <= point.x <= x_cell + interval
                and y_cell <= point.y <= y_cell + interval):
            return 1
    return 0


def get_grid_points_whose_cells_contains_data_points(data_point_list, grid_points, grid_interval):
    result = []
    for point in grid_points:
        cell_bottom_coordinates = (point.x, point.y)
        if is_grid_cell_contains_point(cell_bottom_coordinates, data_point_list.point_list, grid_interval):
            result.append(point)
    return result


def is_cell_belongs_to_the_figure_border(point, border_points):
    return point in border_points


def get_square_of_figure_limited_by_outer_data_points(grid, figure_border_cells):
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



    return outer_points_left + outer_points_right + outer_points_top + outer_points_bottom


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


points_list = file_parser.get_points_list_from_csv('test_data.csv')

grid = Grid(points_list.get_x_boundaries(), points_list.get_y_boundaries(), 19)

grid_points = list(numpy.concatenate(grid.structured_grid_points))

grid_points_whose_cells_contains_data_points = get_grid_points_whose_cells_contains_data_points(points_list,
                                                                                                grid_points,
                                                                                                grid.grid_interval)
outer_cells = get_square_of_figure_limited_by_outer_data_points(grid, grid_points_whose_cells_contains_data_points)

fig = plt.figure()
ax = fig.gca()

# plot grid lines
for point in grid_points:
    cell_bottom_coordinates = (point.x, point.y)
    rect = patches.Rectangle(cell_bottom_coordinates, grid.grid_interval, grid.grid_interval,
                             linewidth=0.15, edgecolor='k', facecolor='None')
    ax.add_patch(rect)

# plot cells contains points
for point in grid_points_whose_cells_contains_data_points:
    cell_bottom_coordinates = (point.x, point.y)
    rect = patches.Rectangle(cell_bottom_coordinates, grid.grid_interval, grid.grid_interval,
                             linewidth=0, edgecolor='b', facecolor='b', alpha=.5)
    ax.add_patch(rect)

# plot outer of figure border cells
for point in outer_cells:
    cell_bottom_coordinates = (point.x, point.y)
    rect = patches.Rectangle(cell_bottom_coordinates, grid.grid_interval, grid.grid_interval,
                             linewidth=0, edgecolor='g', facecolor='g', alpha=.5)
    ax.add_patch(rect)

plt.plot(points_list.get_x_series(), points_list.get_y_series(), 'ro', markersize=3)

plt.show()
