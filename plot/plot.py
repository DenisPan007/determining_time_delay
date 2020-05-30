import matplotlib.patches as patches


def add_grid_lines(ax, grid_cell_points, grid_interval):
    for point in grid_cell_points:
        cell_bottom_coordinates = (point.x, point.y)
        rect = patches.Rectangle(cell_bottom_coordinates, grid_interval, grid_interval,
                                 linewidth=0.15, edgecolor='k', facecolor='None')
        ax.add_patch(rect)


def add_cells_contains_points(ax, cell_points_of_figure_boarder, grid_interval):
    for point in cell_points_of_figure_boarder:
        cell_bottom_coordinates = (point.x, point.y)
        rect = patches.Rectangle(cell_bottom_coordinates, grid_interval, grid_interval,
                                 linewidth=0, edgecolor='b', facecolor='b', alpha=.5)
        ax.add_patch(rect)


def add_outer_of_figure_border(ax, outer_cells, grid_interval):
    for point in outer_cells:
        cell_bottom_coordinates = (point.x, point.y)
        rect = patches.Rectangle(cell_bottom_coordinates, grid_interval, grid_interval,
                                 linewidth=0, edgecolor='g', facecolor='g', alpha=.5)
        ax.add_patch(rect)
