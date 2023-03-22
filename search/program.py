# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board


def eval_function(index, power):
    return 1


def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    print(path[::-1])
    return path[::-1]


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # create a total path list
    total_path = []

    while len(input.keys()) > 1:
        # Create a queue
        queue = []

        # Create a generated set
        generated = set()

        # Add all red cells to the queue
        for key, value in input.items():
            if value[0] == "r":
                queue.append(key)
                generated.add(key)

        start = queue[0]

        # create parent dictionary
        parents = {}

        # While the queue is not empty
        while len(queue) > 0:
            # Get the first element of the queue
            current = queue.pop(0)

            if current in input.keys() and input[current][0] == 'b':
                total_path += backtrace(parents, start, current)

                del input[start]
                input[current] = ('r', input[current][1])
                break

            # Get the 6 neighbors of current cell's neighbours
            neighbours = [
                (current[0] + 0, current[1] + 1),
                (current[0] - 1, current[1] + 1),
                (current[0] - 1, current[1] + 0),
                (current[0] + 0, current[1] - 1),
                (current[0] + 1, current[1] - 1),
                (current[0] + 1, current[1] + 0)
            ]

            neighbours = list(map(lambda t: (t[0] % 7, t[1] % 7), neighbours))
            neighbours = list(filter(lambda t: t not in generated, neighbours))

            # For each neighbour
            for neighbour in neighbours:
                parents[neighbour] = current

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
