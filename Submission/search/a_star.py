import time
from .Node import Node
from .HeuristicCalc import h, get_blue_nodes
from .utils import render_board
from .Action import Action
import heapq


def is_goal_state(state):
    return len(get_blue_nodes(state)) == 0


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

    for key in initial_state.keys():
        if initial_state[key][0] == 'r':
            node = Node(key, None, initial_state[key][1], initial_state, (0, 0), [key],
                        0, h(key, initial_state[key][1], initial_state))  # TODO - h()
            heapq.heappush(queue, node)

    while len(queue) > 0:
        current = heapq.heappop(queue)

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
                if is_goal_state(new_state):
                    node = Node((r, q), current, new_state[(r,q)][1], new_state, (dr, dq), node_visited, 0, 0)
                    actions = paint_board(node, new_state)
                    return list(map(lambda x: x.to_tuple(), actions))

                new_node = Node((r, q), current, new_state[(r, q)][1], new_state, (dr, dq), node_visited,
                                current.g + 1, h((r,q), new_state[(r,q)][1], new_state))  # TODO - h()
                heapq.heappush(queue, new_node)


if __name__ == '__main__':
    input_dict = {(0, 0): ('r', 2), (4, 0): ('b', 1), (0, 3): ('b', 6), (3, 5): ('r', 6), (6, 2): ('r', 2), (2,5):('b',2)}

    start = time.time()
    output = A_star(input_dict)
    end = time.time()

    print("Time taken: ", end - start)
    print("Output: ", output)
