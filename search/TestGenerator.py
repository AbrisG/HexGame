import time
import random

from search.BFS import BFS
from search.a_star import A_star
from search.utils import render_board

import matplotlib.pyplot as plt


def generate_tests(n=5, number_of_nodes=-1):
    boards = []
    for i in range(n):
        coord_set = set()
        board = {}
        red_tile = generate_tile('r', coord_set)
        board[red_tile[0]] = red_tile[1]
        blue_tile = generate_tile('b', coord_set)
        board[blue_tile[0]] = blue_tile[1]
        # Generate a random board
        if number_of_nodes != -1:
            for j in range(number_of_nodes):
                tile = generate_tile('rand', coord_set)
                board[tile[0]] = tile[1]
        else:
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
        return coord, ('b', random.randint(1, 1))
    else:
        # Generate random tile
        return coord, ('r', random.randint(1, 6)) if random.random() < 0.5 else ('b', random.randint(1, 6))


if __name__ == '__main__':
    num_tests = 50
    print("Starting tests")
    tests = generate_tests(num_tests)
    print("Testing BFS")

    BFS_i = num_tests
    A_star_i = num_tests

    results = {'BFS': [], 'A*': []}

    optimality = {'BFS': [], 'A*': []}

    for test in tests:
        print(render_board(test, ansi=True))

        failure = False

        try:
            BFS_start_time = time.time()
            BFS_result = BFS(test)
            BFS_end_time = time.time()

            print("BFS result: " + str(BFS_result))
            print("BFS took " + str(BFS_end_time - BFS_start_time) + " seconds")
            results['BFS'].append(BFS_end_time - BFS_start_time)

        except Exception as e:
            print("BFS failed with error: " + str(e))
            results['BFS'].append(-1)
            failure = True

        try:
            A_star_start_time = time.time()
            A_star_result = A_star(test)
            A_star_end_time = time.time()

            print("A_star result: " + str(A_star_result))
            print("A_star took " + str(A_star_end_time - A_star_start_time) + " seconds")
            results['A*'].append(A_star_end_time - A_star_start_time)

        except Exception as e:
            print("A_star failed with error: " + str(e))
            results['A*'].append(-1)
            failure = True

        if failure:
            continue

        if len(BFS_result) != len(A_star_result):
            print(test)
            print("BFS and A* returned different results")

            optimality['BFS'].append(len(BFS_result))
            optimality['A*'].append(len(A_star_result))

    # print statistics
    print('\n\n\n')

    print('Statistics:')
    print('-' * 50)
    print("BFS average time: " + str(sum([i for i in results['BFS'] if i != -1])
                                     / len([i for i in results['BFS'] if i != -1])))
    print("A* average time: " + str(sum([i for i in results['A*'] if i != -1])
                                    / len([i for i in results['A*'] if i != -1])))

    print('-' * 50)

    print("BFS passed " + str(len([i for i in results['BFS'] if i != -1])) + " tests")
    print("A* passed " + str(len([i for i in results['A*'] if i != -1])) + " tests")

    print('-' * 50)

    print("There are " + str(len(optimality['BFS'])) + " tests where BFS and A* returned different results")
    for i in range(len(optimality['BFS'])):
        print("BFS length: " + str(optimality['BFS'][i]) + "A* length: " + str(optimality['A*'][i]))
        print('-' * 50)

    #  Create a graph with respect ot the number of nodes
    dict_plot = {'BFS': [], 'A*': []}
    for i in range(1, 12):
        tests = generate_tests(5, i)
        results_temp = {'BFS': [], 'A*': []}
        for test in tests:
            try:
                BFS_start_time = time.time()
                BFS_result = BFS(test)
                BFS_end_time = time.time()
                results_temp['BFS'].append(BFS_end_time - BFS_start_time)
            except Exception as e:
                results_temp['BFS'].append(-1)
            try:
                A_star_start_time = time.time()
                A_star_result = A_star(test)
                A_star_end_time = time.time()
                results_temp['A*'].append(A_star_end_time - A_star_start_time)
            except Exception as e:
                results_temp['A*'].append(-1)

        dict_plot['BFS'].append(sum([i for i in results_temp['BFS'] if i != -1]) / len([i for i in results_temp['BFS'] if i != -1]))
        dict_plot['A*'].append(sum([i for i in results_temp['A*'] if i != -1]) / len([i for i in results_temp['A*'] if i != -1]))

    plt.plot([i for i in range(1, 12)], dict_plot['BFS'], label='BFS')
    plt.plot([i for i in range(1, 12)], dict_plot['A*'], label='A*')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time')
    plt.legend()
    plt.show()

