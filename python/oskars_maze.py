#!/usr/bin/env python
#
# Find solutions to Oskar's Maze, which is a 3D puzzle.
# For a photo of the maze, see https://www.puzzle-place.com/wiki/Oskar%27s_Maze
#
# This script constructs a 3D representation of the maze from three 2D projections
# of the maze. It then finds paths from various points in the maze to various other points.
# (Some mazes have pre-selected start and finish points, but this maze does not.)
#
# Coordinates used range from 0 to 10 for each of the x, y, and z axes.

import networkx as nx

import numpy as np
from numpy.ma import make_mask


# TODO: Done in haste. Check that these aren't flipped in some way.
class OskarsMaze:
    # Front side
    xy = """
       ***********
       *         *
       *** ***** *
       * *     * *
       * * *******
       *   *   * *
       * *** *** *
       *   * * * *
       *** * * * *
       *         *
       ***********"""

    # Left side
    yz = """
        ***********
        * *     * *
        * ***** * *
        *   *   * *
        * * * * * *
        * * * *   *
        *** * *****
        * * *     *
        * * *** * *
        *       * *
        ***********"""

    # Top side
    xz = """
        ***********
        *     *   *
        * *** *** *
        *   * *   *
        * * *** ***
        * *     * *
        * ***** * *
        *   *   * *
        *** ***** *
        *         *
        ***********"""


def assert_nodes_are_in_maze(maze, nodes):
    are_corners_in_maze = [(x, y, z) in maze for (x, y, z) in get_corners()]
    assert(all(are_corners_in_maze))


def cube_to_maze(xyz):
    def tup_sum(a, b):
        return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

    node_pos = list(zip(*np.where(~xyz)))  # Record their positions
    nbr_vecs = [(-1,0,0), (1,0,0)] + [(0,-1,0), (0,1,0)] + [(0,0,-1), (0,0,1)]

    maze = nx.DiGraph()
    for from_pos in node_pos:
        for nbr_vec in nbr_vecs:
            to_pos = tup_sum(from_pos, nbr_vec)
            if to_pos in node_pos:  # Found an open connector (edge) of the maze
                # from_idx = pos2idx[from_pos]
                # to_idx = pos2idx[to_pos]
                maze.add_edge(from_pos, to_pos)
    return maze


def get_corners():
    return [(x, y, z) for x in [1, 9] for y in [1, 9] for z in [1, 9]]


def get_maze():
    array_xy = str2d_to_array2d(OskarsMaze.xy)
    array_yz = str2d_to_array2d(OskarsMaze.yz)
    array_xz = str2d_to_array2d(OskarsMaze.xz)
    cube = panels_to_cube(array_xy, array_yz, array_xz)
    maze = cube_to_maze(cube)
    return maze


def panels_to_cube(xy, yz, xz):
    result = np.zeros((11, 11, 11), dtype=bool)
    for x in range(0, 11):
        for y in range(0, 11):
            for z in range(0, 11):
                if xy[(x, y)] or yz[(y, z)] or xz[(x, z)]:
                    result[(x, y, z)] = True
    # TODO: If a node has only 2 neighbors, and all 3 nodes are collinear,
    #       then remove that node and join its two neighbors.
    return result


def str2d_to_array2d(s):
    """Convert a 2D string-based cross-sections of the maze to numpy array.
    In the numpy array form, True represents an obstacle; False, an empty space.
    """
    tr_map = str.maketrans('* ', '10')
    rows = map(lambda x: x.strip().translate(tr_map), s.split('\n')[1:])
    ints = [int(c) for c in ''.join(rows)]
    return make_mask(ints).reshape((11, 11))


if __name__ == '__main__':
    maze = get_maze()
    # assert(maze.number_of_nodes() == 220)  # Before non-branching nodes are removed
    corners = get_corners()
    assert_nodes_are_in_maze(maze, corners)

    for i in range(len(corners)):
        for j in range(i + 1, len(corners)):
            from_pos = corners[i]
            to_pos = corners[j]
            has_path = nx.has_path(maze, from_pos, to_pos)
            if has_path:
                path = nx.shortest_path(maze, source=from_pos, target=to_pos)
                print(f'Path from {from_pos} to {to_pos}: shortest length is {len(path)}')
            else:
                print(f'Path from {from_pos} to {to_pos}: None')
