from Action import Action
from utils import render_board


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
