import time
from Node import Node
from Action import Action
from utils import render_board


def get_blue_nodes(state, coords_only=False):
    blue_nodes = list(filter(lambda x: x[1][0] == 'b', state.items()))
    if coords_only:
        return list(map(lambda x: x[0], blue_nodes))
    else:
        return blue_nodes


def is_goal_state(state):
    return len(get_blue_nodes(state)) == 0


def axial_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[0] + a[1] - b[0] - b[1])) / 2


def uniform_cost(a, b):
    return 1


def get_wraparound_nodes(blue_nodes):
    # Account for the wraparound
    all_blue_nodes = []
    for blue_node in blue_nodes:
        all_blue_nodes.append(blue_node)
        wraparound_coordinates = [
            (blue_node[0], blue_node[1] + 7),
            (blue_node[0] - 7, blue_node[1] + 7),
            (blue_node[0] - 7, blue_node[1]),
            (blue_node[0], blue_node[1] - 7),
            (blue_node[0] + 7, blue_node[1] - 7),
            (blue_node[0] + 7, blue_node[1])
        ]
        all_blue_nodes.extend(wraparound_coordinates)

    return all_blue_nodes


def h(coord, k, state, distance_f=axial_distance) -> int:
    # Get blue nodes
    blue_nodes = get_blue_nodes(state, coords_only=True)

    # Account for the wraparound
    all_blue_nodes = get_wraparound_nodes(blue_nodes)

    # Calculate the distance to all blue nodes
    distances = list(map(lambda bn: max(distance_f(coord, bn) - k + 1, 0), all_blue_nodes))

    # Return the lowest distance
    return min(distances)


def path_to_actions(path):
    actions = []
    for i in range(len(path) - 1):
        actions.append(
            Action(path[i].coord[0], path[i].coord[1], path[i + 1].offset[0], path[i + 1].offset[1], path[i].k))
    return actions


def paint_board(node, state):
    # Get the path
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()

    actions = path_to_actions(path)

    print(render_board(state, True))

    return actions


def A_star(initial_state):
    initial_state = initial_state.copy()

    print(render_board(initial_state, True))

    queue = []
    visited = []

    for items in initial_state.items():
        if items[1][0] == 'r':
            node = Node(items[0], None, 0, h(items[0], items[1][1], initial_state), items[1][1], (0, 0), initial_state)
            queue.append(node)
            visited.append(node)

    while len(queue) > 0:
        current = min(queue, key=lambda x: x.f)
        queue.remove(current)

        neighbours = current.get_neighbours(by_direction=True)

        for (dr, dq) in neighbours.keys():
            # Grab the state of the prior node
            new_state = current.state.copy()

            # Modify it to reflect the new node(s)
            del new_state[current.coord]

            to_remove = []

            for (r, q) in neighbours[(dr, dq)]:
                # Calculate and update k
                k = 1
                if (r, q) in new_state.keys():
                    k = new_state[(r, q)][1] + 1

                # Check if k greater than max power, if not add to the state
                if k > 6:
                    to_remove.append((r, q))
                else:
                    new_state[(r, q)] = ('r', k)

            neighbours[(dr, dq)] = list(filter(lambda x: x not in to_remove, neighbours[(dr, dq)]))

            nodes_to_add = []

            for (r, q) in neighbours[(dr, dq)]:
                k = new_state[(r, q)][1]

                # Calculate heuristic with the prior state
                heuristic = h((r, q), k, current.state)

                # Create new node
                new_node = Node((r, q), current, current.g + 1, heuristic, k, (dr, dq), new_state)
                nodes_to_add.append(new_node)

            # Check if goal state
            if is_goal_state(new_state):
                actions = paint_board(nodes_to_add[0], new_state)
                return list(map(lambda x: x.to_tuple(), actions))

            queue.extend(nodes_to_add)
            visited.extend(nodes_to_add)


if __name__ == '__main__':
    print(get_wraparound_nodes([(0, 0)]))
    print(axial_distance((0,0), (6,6)))
    input_dict = {(5, 6): ('r', 2), (1, 0): ('b', 2), (1, 1): ('b', 1), (3, 2): ('b', 1), (1, 3): ('b', 3)}

    start = time.time()
    output = A_star(input_dict)
    end = time.time()

    print("Time taken: ", end - start)
    print("Output: ", output)
