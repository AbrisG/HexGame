import time
from Node import Node
from HeuristicCalc import h, get_blue_nodes
from utils import render_board


def is_goal_state(state):
    return len(get_blue_nodes(state)) == 0


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

        neighbours = current.get_neighbours()

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
    input_dict = {(5, 6): ('r', 2), (1, 0): ('b', 2), (1, 1): ('b', 1), (3, 2): ('b', 1), (1, 3): ('b', 3)}

    start = time.time()
    output = A_star(input_dict)
    end = time.time()

    print("Time taken: ", end - start)
    print("Output: ", output)
