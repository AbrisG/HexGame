def get_blue_nodes(state, coords_only=False):
    blue_nodes = list(filter(lambda x: x[1][0] == 'b', state.items()))
    if coords_only:
        return list(map(lambda x: x[0], blue_nodes))
    else:
        return blue_nodes


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
    return max(0, min(distances))
