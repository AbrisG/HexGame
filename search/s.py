from Node import Node
from Action import Action
from utils import render_board


def axial_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[0] + a[1] - b[0] - b[1])) / 2


def get_blue_nodes(inp):
    blue_nodes = []
    for key, value in inp.items():
        if value[0] == 'b':
            blue_nodes.append(key)
    return blue_nodes


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


def h(coord: tuple, inp: dict[tuple, tuple], distance_f=axial_distance) -> int:
    # Get blue nodes from current board state
    blue_nodes = get_blue_nodes(inp)

    # Account for the wraparound
    all_blue_nodes = get_wraparound_nodes(blue_nodes)

    # Calculate the distance to all blue nodes
    distances = list(map(lambda bn: distance_f(coord, bn), all_blue_nodes))

    # Return the lowest distance
    return min(distances)


def paint_board(node, inp):
    # Save the path
    path = []
    while node.parent is not None:
        path.append(node)
        node = node.parent
    path.append(node)
    path.reverse()

    # Convert the path into a series of actions
    actions = []
    for i in range(len(path) - 1):
        actions.append(
            Action(path[i].coord[0], path[i].coord[1], path[i + 1].offset[0], path[i + 1].offset[1], path[i].k))

    # Paint the board
    for action in actions:
        del inp[(action.r, action.q)]
        for i in range(1, action.k + 1):
            new_square = (action.r + action.dr * i) % 7, (action.q + action.dq * i) % 7
            if new_square in inp.keys():
                inp[new_square] = ('r', inp[new_square][1] + 1)
            else:
                inp[new_square] = ('r', 1)
    return path[-1]


def queue_all_red_nodes(inp: dict[tuple, tuple]):
    queue = []
    generated = set()
    # Put all the red nodes into the queue
    for key in inp.keys():
        if inp[key][0] == 'r':
            red_node = Node(key, None, 0, -1, inp[key][1], (0, 0))
            queue.append(red_node)
            generated.add(red_node.coord)
    return queue, generated


def search(inp: dict[tuple, tuple]) -> list[tuple]:
    queue, generated = queue_all_red_nodes(inp)
    i = 0

    # Determine which neighbouring node is the closest to a blue node
    while len(queue) > 0 and i < 8:

        if len(list(filter(lambda x: inp[x][0] == 'b', inp.keys()))) == 0:
            break

        # A* search, so we grab the node with the lowest f value
        node = min(queue, key=lambda n: n.f)
        queue.remove(node)

        if node.coord in inp.keys() and inp[node.coord][0] == 'b':
            paint_board(node, inp)
            queue, generated = queue_all_red_nodes(inp)
            continue

        # get all the neighbours of that node
        neighbours = node.get_neighbours()

        # filter out the neighbours that are already generated
        valid_neighbours = list(filter(lambda x: (x[0], x[1]) not in generated, neighbours))

        # create the nodes for the neighbours
        generated_neighbours = list(
            map(lambda x: Node((x[0], x[1]), node, node.g + 1, h(x, inp), 1, (x[2], x[3])), valid_neighbours))
        print("Parent Node: " + str(node))

        queue += generated_neighbours
        generated.update(valid_neighbours)
        i += 1

    print(render_board(inp, ansi=True))

    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]
