from Node import Node
from Action import Action
from utils import render_board
from timeout_decorator import timeout


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
    distances = list(map(lambda bn: max(distance_f(coord, bn), 0), all_blue_nodes))

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

@timeout(30)
def A_star(initial_state):
    initial_state = initial_state.copy()

    queue = []
    g_tracker = {}

    for items in initial_state.items():
        if items[1][0] == 'r':
            node = Node(items[0], None, 0, h(items[0], items[1][1], initial_state), items[1][1], (0, 0), initial_state)
            g_tracker[items[0]] = 0
            queue.append(node)

    while len(queue) > 0:
        current = min(queue, key=lambda x: x.f)
        queue.remove(current)

        neighbours = current.get_neighbours()

        for (r, q, dr, dq) in neighbours.keys():
            # Check if the node is the best so far (g_tracker)
            # tentative_g = current.g + 1
            # if tentative_g >= g_tracker[(r, q)]:
            #     continue

            # Check if the node is already in the queue
            if (r, q) in queue:
                continue

            # Grab the state of the prior node
            new_state = current.state.copy()

            # Modify it to reflect the new node(s)
            del new_state[current.coord]

            # Calculate and update k
            k = 1
            if (r, q) in new_state.keys():
                k = new_state[(r, q)][1] + 1

            # If the k > 6 then the node dissapears, and we don't track it
            if k > 6:
                continue

            new_state[(r, q)] = ('r', k)

            # Calculate heuristic with the prior state
            heuristic = h((r, q), k, current.state)

            # Create new node
            new_node = Node((r, q), current, current.g + 1, heuristic, k, (dr, dq), new_state)

            # Update g_tracker
            g_tracker[(r, q)] = new_node.g

            # Check if goal state
            if is_goal_state(new_state):
                actions = paint_board(new_node, new_state)
                return list(map(lambda x: x.to_tuple(), actions))

            # Add to queue
            queue.append(new_node)

input = {(5, 3): ('r', 3), (1, 3): ('b', 3), (2, 0): ('b', 6), (6, 0): ('r', 2), (6, 4): ('b', 5), (0, 1): ('r', 1), (2, 3): ('b', 6), (6, 2): ('b', 5)}
print(A_star(input))