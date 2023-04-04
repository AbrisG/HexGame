import time
import random

from search.BFS import BFS
from search.a_star import A_star
from search.utils import render_board


def generate_tests(n=5):
    boards = []
    for i in range(n):
        coord_set = set()
        print(i)
        board = {}
        red_tile = generate_tile('r', coord_set)
        board[red_tile[0]] = red_tile[1]
        blue_tile = generate_tile('b', coord_set)
        board[blue_tile[0]] = blue_tile[1]
        # Generate a random board
        for j in range(random.randint(5, 10)):
            tile = generate_tile('rand', coord_set)
            board[tile[0]] = tile[1]
        boards.append(board)
    return boards


def generate_tile(colour, coord_set):
    # Generate a random coordinate
    coord = (random.randint(0, 6), random.randint(0, 6))
    while coord in coord_set:
        coord = (random.randint(0, 6), random.randint(0, 6))
    coord_set.add(coord)
    if colour == 'r':
        # Generate a random red tile
        return coord, ('r', random.randint(1, 6))
    elif colour == 'b':
        # Generate a random blue tile
        return coord, ('b', random.randint(1, 1))
    else:
        # Generate random tile
        return coord, ('r', random.randint(1, 6)) if random.random() < 0.5 else ('b', random.randint(1, 6))


if __name__ == '__main__':
    num_tests = 50
    print("Starting tests")
    tests = generate_tests(num_tests)
    print("Testing BFS")
    i = 0
    for test in tests:
        try:
            print(render_board(test, ansi=True))

            BFS_start_time = time.time()
            BFS_result = BFS(test)
            BFS_end_time = time.time()

            print("BFS result: " + str(BFS_result))

            print("BFS took " + str(BFS_end_time - BFS_start_time) + " seconds")

            i += 1

        except Exception as e:
            print("BFS failed with error: " + str(e))
            continue

    print("BFS passed " + str(i) + "/" + str(num_tests) + " tests")