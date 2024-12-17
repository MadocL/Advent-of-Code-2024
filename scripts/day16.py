from math import inf
from rich.console import Console
from sys import setrecursionlimit
from copy import deepcopy


def print_inputs(inputs, char_to_reverse=None):
    """custom print"""
    console = Console()
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if (i, j) in char_to_reverse:
                console.print(inputs[i][j], end="", style="reverse")
            else:
                print(inputs[i][j], end="")
        print("")
    print("")


def find_lowest_score_path(inputs, current_position, facing, visited, memoize):
    # print_inputs(inputs, char_to_reverse=visited)
    if inputs[current_position[0]][current_position[1]] == "E":
        return 0

    if memoize.get((current_position, facing)) is not None:
        return memoize[(current_position, facing)]

    next_possible_moves = []

    for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbour = (current_position[0] + move[0], current_position[1] + move[1])

        if inputs[neighbour[0]][neighbour[1]] != "#" and neighbour not in visited:
            if move == (0, 1):
                if facing == "east":
                    next_possible_moves.append((1, neighbour, facing))
                elif facing == "north" or facing == "south":
                    next_possible_moves.append((1001, neighbour, "east"))
                else:
                    next_possible_moves.append((2001, neighbour, "east"))
            elif move == (1, 0):
                if facing == "south":
                    next_possible_moves.append((1, neighbour, facing))
                elif facing == "west" or facing == "east":
                    next_possible_moves.append((1001, neighbour, "south"))
                else:
                    next_possible_moves.append((2001, neighbour, "south"))
            elif move == (0, -1):
                if facing == "west":
                    next_possible_moves.append((1, neighbour, facing))
                elif facing == "north" or facing == "south":
                    next_possible_moves.append((1001, neighbour, "west"))
                else:
                    next_possible_moves.append((2001, neighbour, "west"))
            else:  # to the west
                if facing == "north":
                    next_possible_moves.append((1, neighbour, facing))
                elif facing == "west" or facing == "east":
                    next_possible_moves.append((1001, neighbour, "north"))
                else:
                    next_possible_moves.append((2001, neighbour, "north"))

    visited.add(current_position)

    if len(next_possible_moves) == 0:
        return inf

    score_ = min([
        score + find_lowest_score_path(inputs, next_position, next_facing, deepcopy(visited), memoize)
        for score, next_position, next_facing in next_possible_moves
    ])

    memoize[(current_position, facing)] = score_
    return score_


if __name__ == "__main__":
    setrecursionlimit(10000)

    # f = open("inputs/day16_small.txt", "r")
    # f = open("inputs/day16_medium.txt", "r")
    f = open("inputs/day16.txt", "r")
    inputs = [list(line) for line in f.read().splitlines()]
    f.close()

    memoize = {}

    # search START
    start = None
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if inputs[i][j] == "S":
                start = (i, j)
                break
        if start is not None:
            break

    score = find_lowest_score_path(inputs, start, "east", set(), memoize)

    print(score)
