# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion
import BFS
from search import a_star
from utils import render_board
import numpy as np
from Node import Node
import s

direction_list = [(0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1), (1, 0)]


def calculate_distance(node1, node2):

    # Create a list of nodes with an offset of 7 in each direction
    node2_list = [
        (node2.coord[0], node2.coord[1] + 7),
        (node2.coord[0], node2.coord[1] - 7),
        (node2.coord[0] - 7, node2.coord[1]),
        (node2.coord[0] + 7, node2.coord[1]),
        node2.coord
    ]

    dist_list = []
    for n in node2_list:
        dist_list.append(np.sqrt((node1.coord[0] - n[0])**2 + (node1.coord[1] - n[1])**2))

    return min(dist_list)


def calculate_h(node, input_dict):
    blues = list(filter(lambda t: t[1][0] == 'b', input_dict.items()))

    minimum = -1
    for blue in blues:
        minimum = min(calculate_distance(node, Node(blue[0], None, 0, -1, -1)), minimum)

    return minimum


def backtrace(start, end):
    path = [end]
    while path[-1].coord != start.coord:
        path.append(path[-1].parent)

    # Convert the path to a list of coordinates
    path = list(map(lambda n: n.coord, path))
    return path[::-1]


def is_node_in_generated(new_node, generated):
    filtered = list(filter(lambda n: n.coord == new_node.coord, generated))
    return len(filtered) > 0


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    return a_star.A_star(input)
