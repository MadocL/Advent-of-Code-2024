from rich.console import Console
from math import inf

DEFAULT_GRID_SIZE = (70+1, 70+1)
DEFAULT_BYTES_AMOUNT = 1024


def create_grid(inputs, grid_size=DEFAULT_GRID_SIZE, bytes_amount=DEFAULT_BYTES_AMOUNT):
    grid = [["." for _ in range(grid_size[0])] for _ in range(grid_size[1])]

    for i in range(bytes_amount):
        y, x = inputs[i]
        grid[x][y] = "#"

    return grid


def print_grid(grid, coords_to_reverse=set()):
    """custom print"""
    console = Console()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in coords_to_reverse:
                console.print(grid[i][j], end="", style="reverse")
            else:
                print(grid[i][j], end="")
        print("")
    print("")


def find_shortest_path(grid, grid_size=DEFAULT_GRID_SIZE, check_solvable=False):
    """Breadth-First Search"""

    heap = [(0, 0)]
    visited = []
    previous = {}
    scores = {}

    while len(heap) > 0:
        current_position = heap.pop(0)
        visited.append(current_position)

        if current_position == (0, 0):
            scores[current_position] = 0
        else:
            current_score = scores.get(current_position, inf)
            scores[current_position] = min(scores[previous[current_position]] + 1, current_score)

        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = (current_position[0] + move[0], current_position[1] + move[1])

            if (  # out of bounds
                not 0 <= neighbour[0] < grid_size[0]
                or not 0 <= neighbour[1] < grid_size[1]
            ):
                continue

            if grid[neighbour[0]][neighbour[1]] == "#":  # corrupted cell
                continue

            if neighbour not in visited and neighbour not in heap:
                heap.append(neighbour)
                previous[neighbour] = current_position

    # print_grid(grid, coords_to_reverse=visited)

    if check_solvable:
        if scores.get((grid_size[0]-1, grid_size[1]-1)) is not None:
            return scores[(grid_size[0]-1, grid_size[1]-1)]
        return False

    return scores[(grid_size[0]-1, grid_size[1]-1)]


if __name__ == "__main__":
    # test = True
    test = False

    if test:
        f = open("inputs/day18_small.txt", "r")
    else:
        f = open("inputs/day18.txt", "r")
    inputs = [(int(line.split(",")[0]), int(line.split(",")[1])) for line in f.read().splitlines()]
    f.close()

    # Part 1
    if test:
        test_bytes_amount = 12
        test_grid_size = (6+1, 6+1)
        grid = create_grid(inputs, grid_size=test_grid_size, bytes_amount=test_bytes_amount)
        score = find_shortest_path(grid, grid_size=test_grid_size)
    else:
        grid = create_grid(inputs)
        score = find_shortest_path(grid)

    print_grid(grid)
    print(score)

    # Part 2
    score = True
    i = 0

    if test:
        i = 0
        while score:
            print(i)
            y, x = inputs[test_bytes_amount + i]
            grid[x][y] = "#"
            score = find_shortest_path(grid, grid_size=test_grid_size, check_solvable=True)
            i += 1

    else:
        while score:
            print(i)
            y, x = inputs[DEFAULT_BYTES_AMOUNT + i]
            grid[x][y] = "#"
            score = find_shortest_path(grid, check_solvable=True)
            i += 1

    print(f"{y},{x}")
    # solution is 60,46
