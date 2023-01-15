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
from networkx.drawing.nx_agraph import write_dot

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


def get_corners():
    return [(x, y, z) for x in [1, 9] for y in [1, 9] for z in [1, 9]]


def get_cube(xy, yz, xz):
    xyz = np.zeros((11, 11, 11), dtype=bool)
    for x in range(0, 11):
        for y in range(0, 11):
            for z in range(0, 11):
                if xy[(x, y)] or yz[(y, z)] or xz[(x, z)]:
                    xyz[(x, y, z)] = True
    return xyz


def get_maze(xyz, do_remove_nonbranching_nodes=True):
    def tup_sum(a, b):
        return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

    node_pos = list(zip(*np.where(~xyz)))  # Unobstructed positions
    nbr_vecs = [(-1,0,0), (1,0,0)] + [(0,-1,0), (0,1,0)] + [(0,0,-1), (0,0,1)]
    maze = nx.Graph()
    for from_pos in node_pos:
        for nbr_vec in nbr_vecs:
            to_pos = tup_sum(from_pos, nbr_vec)
            if to_pos in node_pos:  # Both endpoints are graph nodes. Found an edge.
                maze.add_edge(from_pos, to_pos)

    if do_remove_nonbranching_nodes:
        # If a node has only 2 neighbors, and all 3 nodes are collinear,
        # then remove the center node and join its two neighbors.
        # This process reduces the node count from 220 to 103.
        for node in list(maze.nodes):
            nbrs = list(maze.neighbors(node))
            if len(nbrs) == 2:
                nbr_a = nbrs[0]
                nbr_b = nbrs[1]
                same_x = node[0] == nbr_a[0] == nbr_b[0]
                same_y = node[1] == nbr_a[1] == nbr_b[1]
                same_z = node[2] == nbr_a[2] == nbr_b[2]
                if (same_x and same_y) or (same_x and same_z) or (same_y and same_z):
                    maze.remove_edge(node, nbr_a)
                    maze.remove_edge(node, nbr_b)
                    maze.remove_node(node)
                    maze.add_edge(nbr_a, nbr_b)
    return maze


def get_panel(s):
    """Convert a 2D string-based cross-sections of the maze to numpy array.
    In the numpy array form, True represents an obstacle; False, an empty space.
    """
    tr_map = str.maketrans('* ', '10')
    rows = map(lambda x: x.strip().translate(tr_map), s.split('\n')[1:])
    ints = [int(c) for c in ''.join(rows)]
    return make_mask(ints).reshape((11, 11))


def make_maze(do_remove_nonbranching_nodes=True):
    panel_xy = get_panel(OskarsMaze.xy)
    panel_yz = get_panel(OskarsMaze.yz)
    panel_xz = get_panel(OskarsMaze.xz)
    cube = get_cube(panel_xy, panel_yz, panel_xz)
    maze = get_maze(cube, do_remove_nonbranching_nodes)
    return maze


def print_paths(maze, nodes):
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            from_pos = nodes[i]
            to_pos = nodes[j]
            has_path = nx.has_path(maze, from_pos, to_pos)
            if has_path:
                path = nx.shortest_path(maze, source=from_pos, target=to_pos)
                print(f'Path from {from_pos} to {to_pos}: Shortest length = {len(path) - 1}')
            else:
                print(f'Path from {from_pos} to {to_pos}: None')


if __name__ == '__main__':
    maze = make_maze()
    # print(f'INFO: Maze has {maze.number_of_nodes()} nodes.')
    # print(f'INFO: Maze has {maze.number_connected_components()} connected components.')
    nodes = get_corners()
    assert_nodes_are_in_maze(maze, nodes)
    print_paths(maze, nodes)
    with open('oskars_maze.dot', 'w') as f:
        write_dot(maze, f)  # Convert to png with, e.g., dot -Tpng -o oskars_maze.png oskars_maze.dot
