from Action import Action
from utils import render_board


class NodeBFS:
    def __init__(self, coord, parent, k, state, offset):
        self.coord = coord
        self.parent = parent
        self.state = state
        self.k = k
        self.offset = offset


def generate_path(node):
    path = []
    while node.parent is not None:
        path.append(node)
        node = node.parent
    path.append(node)
    path.reverse()
    return path


def path_to_actions(path):
    actions = []
    for i in range(len(path) - 1):
        actions.append(
            Action(path[i].coord[0], path[i].coord[1], path[i + 1].offset[0], path[i + 1].offset[1], path[i].k))
    return actions


def paint_board(node, inp):
    # Save the path
    path = generate_path(node)

    # Convert the path into a series of actions
    actions = path_to_actions(path)

    # Paint the board
    for action in actions:
        del inp[(action.r, action.q)]
        for i in range(1, action.k + 1):
            new_square = (action.r + action.dr * i) % 7, (action.q + action.dq * i) % 7
            if new_square in inp.keys():
                inp[new_square] = ('r', inp[new_square][1] + 1)
            else:
                inp[new_square] = ('r', 1)

    return actions


def get_start(inp):
    queue = []
    visited = []
    blue_nodes = []
    for key, value in inp.items():
        if value[0] == 'r':
            node = NodeBFS(key, None, value[1], inp, (0, 0))
            queue.append(node)
            visited.append(key)
        else:
            blue_nodes.append(key)
    return queue, visited, blue_nodes


def BFS(inp):
    direction_list = [
        (0, 1),  # down-right
        (-1, 1),  # down
        (-1, 0),  # down-left
        (0, -1),  # up-left
        (1, -1),  # up
        (1, 0)  # up-right
    ]

    queue, visited, blue_nodes = get_start(inp)

    actions = []

    while len(queue) > 0:
        current = queue.pop(0)

        if current.coord in blue_nodes:
            # We found a solution, return the path
            actions += paint_board(current, inp)
            queue, visited, blue_nodes = get_start(inp)
            continue

        neighbours = []

        for i in range(len(direction_list)):
            direction = direction_list[i]
            new_state = current.state.copy()
            new_coords = []
            for j in range(1, current.k + 1):
                new_coord = ((current.coord[0] + direction[0] * j) % 7, (current.coord[1] + direction[1] * j) % 7)
                if new_coord in new_state.keys():
                    k = new_state[new_coord][1] + 1
                else:
                    k = 1

                new_state[new_coord] = ('r', k)

                if new_coord in visited:
                    new_coords = []
                    break
                else:
                    new_coords.append((new_coord, direction))

            neighbours.extend(
                list(map(lambda x: NodeBFS(x[0], current, new_state[x[0]][1], new_state, x[1]), new_coords)))

        queue += neighbours
        visited += list(map(lambda x: x.coord, neighbours))

    return list(map(lambda x: x.to_tuple(), actions))


input = {(1, 4): ('r', 2), (5, 1): ('r', 1), (2, 4): ('b', 2), (1, 1): ('b', 1)}
BFS(input)
