from search.Node import Node


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


def get_wraparound_nodes(blue_nodes):
    # Account for the wraparound
    all_blue_nodes = []
    for blue_node in blue_nodes:
        all_blue_nodes.append(blue_node)
        wraparound_coordinates = [
            (blue_node[0], blue_node[1] + 7),
            (blue_node[0] - 7, blue_node[1] + 7),
            (blue_node[0], blue_node[1] - 7),
            (blue_node[0] + 7, blue_node[1] - 7),
            (blue_node[0] + 7, blue_node[1])
        ]
        all_blue_nodes.extend(wraparound_coordinates)

    return all_blue_nodes


def h(coord: tuple, state, distance_f=axial_distance) -> int:
    # Get blue nodes
    blue_nodes = get_blue_nodes(state, coords_only=True)

    # Account for the wraparound
    all_blue_nodes = get_wraparound_nodes(blue_nodes)

    # Calculate the distance to all blue nodes
    distances = list(map(lambda bn: distance_f(coord, bn), all_blue_nodes))

    # Return the lowest distance
    return min(distances)


def paint_board(new_state):
    pass


def A_star(initial_state):
    queue = []
    visited = []
    for items in initial_state.items():
        if items[1][0] == 'r':
            node = Node(items[0], None, 0, h(items[0], initial_state), items[1][1], (0, 0), initial_state)
            queue.append(node)
            visited.append(node)

    while len(queue) > 0:
        current = min(queue, key=lambda x: x.f)
        queue.remove(current)

        neighbours = current.get_neighbours()

        for (dr, dq) in neighbours.keys():

            # Grab the state of the prior node
            new_state = current.state.copy()

            # Modify it to reflect the new node(s)
            del new_state[current.coord]

            for (r, q) in neighbours[(dr, dq)]:

                # Calculate and update k
                k = 1
                if (r, q) in new_state.keys():
                    k = new_state[(r, q)][1] + 1

                new_state[(r, q)] = ('r', k)


            # Check if goal state
            if is_goal_state(new_state):
                return paint_board(new_state)

            nodes_to_add = []

            for (r, q) in neighbours[(dr, dq)]:
                # Calculate heuristic
                heuristic = h((r, q), new_state)

                # Create new node
                new_node = Node((r, q), current, current.g + 1, heuristic, k, (dr, dq), new_state)

                if new_node in visited:
                    nodes_to_add = []
                    break

            queue.extend(nodes_to_add)
            visited.extend(nodes_to_add)

input = {(1, 4): ('r', 2), (5, 1): ('r', 1), (2, 4): ('b', 2), (1, 1): ('b', 1)}
A_star(input)
