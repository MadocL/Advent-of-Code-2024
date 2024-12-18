from math import inf
from rich.console import Console


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


def find_lowest_score_path(inputs, start_position, end):
    heap = [start_position]
    scores = {start_position: 0}
    facings = {start_position: "east"}
    predecessors = {}
    visited = []

    while len(heap) > 0:
        # print_inputs(inputs, char_to_reverse=visited)
        current_position = heap.pop(heap.index(min(heap, key=lambda x: scores.get(x, inf))))  # select min score cell
        visited.append(current_position)

        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = (current_position[0] + move[0], current_position[1] + move[1])

            if (  # out of bounds
                not 0 <= neighbour[0] < len(inputs)
                or not 0 <= neighbour[1] < len(inputs[0])
            ):
                continue

            if inputs[neighbour[0]][neighbour[1]] == "#":  # wall
                continue

            if neighbour not in visited and neighbour not in heap:
                heap.append(neighbour)

                new_facing, turning_malus = get_new_facing_and_turning_malus(facings[current_position], move)
                facings[neighbour] = new_facing

                if scores[current_position] + turning_malus + 1 < scores.get(neighbour, inf):
                    predecessors[neighbour] = current_position
                    scores[neighbour] = scores[current_position] + turning_malus + 1

    return scores[end], predecessors


def get_new_facing_and_turning_malus(facing, move):
    TURNING_MALUS = 1000

    if facing == "north":
        if move == (-1, 0):
            return "north", 0*TURNING_MALUS
        if move == (0, 1):
            return "east", 1*TURNING_MALUS
        if move == (0, -1):
            return "west", 1*TURNING_MALUS
        return "south", 2*TURNING_MALUS

    if facing == "east":
        if move == (0, 1):
            return "east", 0*TURNING_MALUS
        if move == (1, 0):
            return "south", 1*TURNING_MALUS
        if move == (-1, 0):
            return "north", 1*TURNING_MALUS
        return "west", 2*TURNING_MALUS

    if facing == "south":
        if move == (1, 0):
            return "south", 0*TURNING_MALUS
        if move == (0, -1):
            return "west", 1*TURNING_MALUS
        if move == (0, 1):
            return "east", 1*TURNING_MALUS
        return "north", 2*TURNING_MALUS

    if facing == "west":
        if move == (0, -1):
            return "west", 0*TURNING_MALUS
        if move == (-1, 0):
            return "north", 1*TURNING_MALUS
        if move == (1, 0):
            return "south", 1*TURNING_MALUS
        return "east", 2*TURNING_MALUS


if __name__ == "__main__":
    # f = open("inputs/day16_small.txt", "r")
    # f = open("inputs/day16_medium.txt", "r")
    f = open("inputs/day16.txt", "r")
    inputs = [list(line) for line in f.read().splitlines()]
    f.close()

    # search START and END
    start = None
    end = None

    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if inputs[i][j] == "S":
                start = (i, j)
            elif inputs[i][j] == "E":
                end = (i, j)

    # Part 1
    score, predecessors = find_lowest_score_path(inputs, start, end)
    print(score)

    # Part 2
    shortest_path = []
    current_position = end

    while current_position is not None:
        shortest_path.append(current_position)
        current_position = predecessors.get(current_position, None)

    # print(shortest_path)
    print_inputs(inputs, char_to_reverse=shortest_path)
