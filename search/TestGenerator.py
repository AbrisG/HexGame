import time
import random

from search.BFS import BFS
from search.a_star import A_star
from search.utils import render_board


def generate_tests(n=5):
    coord_set = set()
    boards = []
    for i in range(n):
        board = {}
        red_tile = generate_tile('r', coord_set)
        board[red_tile[0]] = red_tile[1]
        blue_tile = generate_tile('b', coord_set)
        board[blue_tile[0]] = blue_tile[1]
        # Generate a random board
        for j in range(random.randint(0, 10)):
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
        return coord, ('b', random.randint(1, 6))
    else:
        # Generate random tile
        return coord, ('r', random.randint(1, 6)) if random.random() < 0.5 else ('b', random.randint(1, 6))


tests = generate_tests(2)
for test in tests:
    print(render_board(test, ansi=True))

    try:
        # Time the algorithms
        A_star_start_time = time.time()
        A_star_result = A_star(test)
        A_star_end_time = time.time()

        print("A* result: " + str(A_star_result))

        BFS_start_time = time.time()
        BFS_result = BFS(test)
        BFS_end_time = time.time()

        print("BFS result: " + str(BFS_result))

        print("BFS took " + str(BFS_end_time - BFS_start_time) + " seconds")
        print("A* took " + str(A_star_end_time - A_star_start_time) + " seconds")

        # Check if the algorithms return the same result
        if len(BFS_result) != len(A_star_result):
            raise Exception("The algorithms returned different results")
    except Exception as e:
        print(e)
        print(test)
        break
