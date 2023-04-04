from Action import Action
from utils import render_board
import time


class NodeBFS:
    def __init__(self, coord, parent, k, state, offset, visited):
        self.coord = coord
        self.parent = parent
        self.state = state
        self.k = k
        self.offset = offset
        self.visited = visited

    dr_dq = [
        (0, 1),  # down-right
        (-1, 1),  # down
        (-1, 0),  # down-left
        (0, -1),  # up-left
        (1, -1),  # up
        (1, 0)  # up-right
    ]

    def get_neighbours(self):
        # Grab all the neighbours according to the offsets and the power (k)
        neighbours = {key: [] for key in NodeBFS.dr_dq}
        for i in range(1, self.k + 1):
            for (dr, dq) in NodeBFS.dr_dq:
                neighbours[(dr, dq)].append(((self.coord[0] + dr * i) % 7, (self.coord[1] + dq * i) % 7))
        return neighbours

    def __eq__(self, other):
        if not isinstance(other, NodeBFS):
            return False
        return self.coord == other.coord

    def __str__(self):
        return str(self.coord) + " " + str(self.k) + " " + str(self.offset) + " " + str(self.parent)


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

    print(render_board(inp, True))

    return actions


def get_blue_nodes(state):
    blue_nodes = []
    for key, value in state.items():
        if value[0] == 'b':
            blue_nodes.append(key)
    return blue_nodes


def is_goal_state(state):
    return len(get_blue_nodes(state)) == 0


def BFS(inp):
    inp = inp.copy()
    print(render_board(inp, True))
    #master = inp.copy()

    queue = []

    for key in inp.keys():
        if inp[key][0] == 'r':
            node = NodeBFS(key, None, inp[key][1], inp, (0, 0), [key])
            queue.append(node)

    while len(queue) > 0:
        current = queue.pop(0)

        """
        # Print the board after every move
        master.update(current.state)

        root = current
        while root.parent is not None:
           root = root.parent

        if current.parent is not None:
            master[current.parent.coord] = ('g', current.parent.k)

        print(root)
        print(render_board(master, True))
        """

        if is_goal_state(current.state):
            actions = paint_board(current, inp)
            return list(map(lambda x: x.to_tuple(), actions))

        neighbours = current.get_neighbours()

        for (dr, dq) in neighbours.keys():

            # Grab the state of the prior node
            new_state = current.state.copy()

            # Modify it to reflect the new node(s)
            del new_state[current.coord]

            nodes_to_check = []
            for (r, q) in neighbours[(dr, dq)]:
                # Calculate and update k
                k = 1
                if (r, q) in new_state.keys():
                    k = new_state[(r, q)][1] + 1

                if k > 6:
                    del new_state[(r, q)]
                    continue

                if (r, q) in current.visited:
                    continue

                new_state[(r, q)] = ('r', k)
                nodes_to_check.append((r, q))

            node_visited = current.visited.copy()
            node_visited.extend(nodes_to_check)

            for (r, q) in nodes_to_check:
                new_node = NodeBFS((r, q), current, new_state[(r, q)][1], new_state, (dr, dq), node_visited)
                queue.append(new_node)


if __name__ == '__main__':
    input_dict = {(5, 6): ('r', 2), (1, 0): ('b', 2), (1, 1): ('b', 1), (3, 2): ('b', 1), (1, 3): ('b', 3)}

    start = time.time()
    output = BFS(input_dict)
    end = time.time()

    print("Time taken: ", end - start)
    print("Output: ", output)