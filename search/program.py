# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board
import numpy as np
from Node import Node

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
    total_path = []

    while len(input.keys()) > 1:
        queue = []
        generated = set()

        # Add all red cells to the queue
        for key, value in input.items():
            if value[0] == "r":
                new_node = Node(key, None, 0, -1, -1)

                queue.append(new_node)
                generated.add(new_node)

        start = queue[0]

        # While the queue is not empty
        while len(queue) > 0:
            # Get the element in the queue with the lowest f value and remove it from the queue
            current = min(queue, key=lambda n: n.f)
            queue.remove(current)

            if current.coord in input.keys() and input[current.coord][0] == 'b':
                total_path += backtrace(start, current)

                del input[start.coord]
                input[current.coord] = ('r', input[current.coord][1])
                break

            neighbours = []

            for i in range(len(direction_list)):
                direction = direction_list[i]

                new_coord = ((current.coord[0] + direction[0]) % 7, (current.coord[1] + direction[1]) % 7)

                g = current.g + 1
                new_node = Node(new_coord, current, g, -1, -1)

                h = calculate_h(new_node, input)
                new_node.h = h
                new_node.f = g + h

                if is_node_in_generated(new_node, generated):
                    continue

                neighbours.append(new_node)
                generated.add(new_node)

            queue += neighbours
            generated.update(neighbours)

    # The render_board function is useful for debugging -- it will print out a
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=True))

    # remove duplicate items from the total_path list
    total_path = list(dict.fromkeys(total_path))

    print(total_path)

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]
