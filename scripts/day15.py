from numpy import array, zeros
from copy import deepcopy
from rich.console import Console


def move_robot(map_, robot_pos, move):
    if move == "^":
        if "." not in map_[:robot_pos[0], robot_pos[1]]:
            return map_, robot_pos  # do nothing, robot can't move

        block_last_idx = robot_pos[0] - 1
        while "." not in map_[block_last_idx:robot_pos[0], robot_pos[1]]:
            if "#" in map_[block_last_idx:robot_pos[0], robot_pos[1]]:
                return map_, robot_pos  # can't move walls
            block_last_idx -= 1

        map_[block_last_idx:robot_pos[0], robot_pos[1]] = map_[block_last_idx + 1: robot_pos[0] + 1, robot_pos[1]]
        map_[robot_pos[0], robot_pos[1]] = "."
        robot_pos[0] -= 1

        return map_, robot_pos

    elif move == ">":
        if "." not in map_[robot_pos[0]][robot_pos[1] + 1:]:
            return map_, robot_pos  # do nothing, robot can't move

        block_last_idx = robot_pos[1] + 1
        while "." not in map_[robot_pos[0], robot_pos[1]:block_last_idx]:
            if "#" in map_[robot_pos[0], robot_pos[1]:block_last_idx]:
                return map_, robot_pos  # can't move walls
            block_last_idx += 1

        map_[robot_pos[0], robot_pos[1] + 1:block_last_idx] = map_[robot_pos[0], robot_pos[1]:block_last_idx - 1]
        map_[robot_pos[0], robot_pos[1]] = "."
        robot_pos[1] += 1

        return map_, robot_pos

    elif move == "v":
        if "." not in map_[robot_pos[0] + 1:, robot_pos[1]]:
            return map_, robot_pos  # do nothing, robot can't move

        block_last_idx = robot_pos[0] + 1
        while "." not in map_[robot_pos[0]:block_last_idx, robot_pos[1]]:
            if "#" in map_[robot_pos[0]:block_last_idx, robot_pos[1]]:
                return map_, robot_pos  # can't move walls
            block_last_idx += 1

        map_[robot_pos[0] + 1:block_last_idx, robot_pos[1]] = map_[robot_pos[0]:block_last_idx - 1, robot_pos[1]]
        map_[robot_pos[0], robot_pos[1]] = "."
        robot_pos[0] += 1

        return map_, robot_pos

    elif move == "<":
        if "." not in map_[robot_pos[0]][:robot_pos[1]]:
            return map_, robot_pos  # do nothing, robot can't move

        block_last_idx = robot_pos[1] - 1
        while "." not in map_[robot_pos[0], block_last_idx:robot_pos[1]]:
            if "#" in map_[robot_pos[0], block_last_idx:robot_pos[1]]:
                return map_, robot_pos  # can't move walls
            block_last_idx -= 1

        map_[robot_pos[0], block_last_idx:robot_pos[1]] = map_[robot_pos[0], block_last_idx + 1:robot_pos[1] + 1]
        map_[robot_pos[0], robot_pos[1]] = "."
        robot_pos[1] -= 1

        return map_, robot_pos


def print_map(map_, char_to_reverse=None):
    console = Console()
    """custom map print"""
    for i in range(map_.shape[0]):
        for j in range(map_.shape[1]):
            if char_to_reverse and i == char_to_reverse[0] and j == char_to_reverse[1]:
                console.print(map_[i, j], end="", style="reverse")
            else:
                print(map_[i, j], end="")
        print("")
    print("")


def part_1(map__, robot_pos):
    for move in moves_sequence:
        map__, robot_pos = move_robot(map__, robot_pos, move)
        # print_map(map__)

    sum_ = 0
    for i in range(map_.shape[0]):
        for j in range(map_.shape[1]):
            if map_[i, j] == "O":
                sum_ += 100 * i + j

    return sum_


def expand_map(map_):
    new_map = zeros(shape=(map_.shape[0], map_.shape[1]*2), dtype="<U1")

    for i in range(map_.shape[0]):
        for j in range(map_.shape[1]):
            if map_[i, j] == "@":
                new_map[i, j*2] = "@"
                new_map[i, j*2 + 1] = "."
            elif map_[i, j] == "O":
                new_map[i, j*2] = "["
                new_map[i, j*2 + 1] = "]"
            else:
                new_map[i, j*2] = map_[i, j]
                new_map[i, j*2 + 1] = map_[i, j]

    return new_map


def move_cells(map_, cell_to_move, move, do_not_check_first=False):
    # print_map(map_, char_to_reverse=cell_to_move)

    if move == "^":
        if "." not in map_[:cell_to_move[0], cell_to_move[1]]:
            return False  # do nothing, this cell can't move

        block_last_idx = cell_to_move[0] - 1

        while "." not in map_[block_last_idx:cell_to_move[0], cell_to_move[1]]:
            block = list(reversed(map_[block_last_idx:cell_to_move[0], cell_to_move[1]]))
            if "#" in block:
                return False  # can't move walls

            for i in range(len(block)):
                if block[i] == "[":
                    if map_[cell_to_move[0] - (i+1), cell_to_move[1] + 1] == "]":
                        result = move_cells(deepcopy(map_), (cell_to_move[0] - (i+1), cell_to_move[1] + 1), move)
                        if result is not False:
                            map_ = result
                        else:
                            return False

                elif block[i] == "]":
                    if map_[cell_to_move[0] - (i+1), cell_to_move[1] - 1] == "[":
                        result = move_cells(deepcopy(map_), (cell_to_move[0] - (i+1), cell_to_move[1] - 1), move)
                        if result is not False:
                            map_ = result
                        else:
                            return False

            block_last_idx -= 1

        map_[block_last_idx:cell_to_move[0], cell_to_move[1]] = map_[
            block_last_idx + 1: cell_to_move[0] + 1, cell_to_move[1]
        ]
        map_[cell_to_move[0], cell_to_move[1]] = "."

    elif move == "v":
        if "." not in map_[cell_to_move[0] + 1:, cell_to_move[1]]:
            return False  # do nothing, this cell can't move

        block_last_idx = cell_to_move[0] + 1
        while "." not in map_[cell_to_move[0]+1:block_last_idx, cell_to_move[1]]:
            block = map_[cell_to_move[0]+1:block_last_idx, cell_to_move[1]]
            if "#" in block:
                return False  # can't move walls

            for i in range(block.shape[0]):
                if block[i] == "[":
                    if map_[cell_to_move[0] + i+1, cell_to_move[1] + 1] == "]":
                        result = move_cells(deepcopy(map_), (cell_to_move[0] + i+1, cell_to_move[1] + 1), move)
                        if result is not False:
                            map_ = result
                            # print_map(map_, char_to_reverse=cell_to_move)
                        else:
                            return False

                elif block[i] == "]":
                    if map_[cell_to_move[0] + i+1, cell_to_move[1] - 1] == "[":
                        result = move_cells(deepcopy(map_), (cell_to_move[0] + i+1, cell_to_move[1] - 1), move)
                        if result is not False:
                            map_ = result
                            # print_map(map_, char_to_reverse=cell_to_move)
                        else:
                            return False

            block_last_idx += 1

        map_[cell_to_move[0] + 1:block_last_idx, cell_to_move[1]] = map_[
            cell_to_move[0]:block_last_idx - 1, cell_to_move[1]
        ]
        map_[cell_to_move[0], cell_to_move[1]] = "."

    return map_


def move_robot_new_map(map_, robot_pos, move):
    if move == "^":
        result = move_cells(deepcopy(map_), robot_pos, move)
        if result is not False:
            map_ = result
            robot_pos[0] -= 1

        return map_, robot_pos

    elif move == ">":
        if "." not in map_[robot_pos[0]][robot_pos[1] + 1:]:
            return map_, robot_pos  # do nothing, robot can't move

        block_last_idx = robot_pos[1] + 1
        while "." not in map_[robot_pos[0], robot_pos[1]:block_last_idx]:
            if "#" in map_[robot_pos[0], robot_pos[1]:block_last_idx]:
                return map_, robot_pos  # can't move walls
            block_last_idx += 1

        map_[robot_pos[0], robot_pos[1] + 1:block_last_idx] = map_[robot_pos[0], robot_pos[1]:block_last_idx - 1]
        map_[robot_pos[0], robot_pos[1]] = "."
        robot_pos[1] += 1

        return map_, robot_pos

    elif move == "v":
        result = move_cells(deepcopy(map_), robot_pos, move)
        if result is not False:
            map_ = result
            robot_pos[0] += 1

        return map_, robot_pos

    elif move == "<":
        if "." not in map_[robot_pos[0]][:robot_pos[1]]:
            return map_, robot_pos  # do nothing, robot can't move

        block_last_idx = robot_pos[1] - 1
        while "." not in map_[robot_pos[0], block_last_idx:robot_pos[1]]:
            if "#" in map_[robot_pos[0], block_last_idx:robot_pos[1]]:
                return map_, robot_pos  # can't move walls
            block_last_idx -= 1

        map_[robot_pos[0], block_last_idx:robot_pos[1]] = map_[robot_pos[0], block_last_idx + 1:robot_pos[1] + 1]
        map_[robot_pos[0], robot_pos[1]] = "."
        robot_pos[1] -= 1

        return map_, robot_pos


if __name__ == "__main__":
    # Console().clear()

    # f = open("inputs/day15_small.txt", "r")
    # f = open("inputs/day15_small_2.txt", "r")
    # f = open("inputs/day15_medium.txt", "r")
    f = open("inputs/day15.txt", "r")
    inputs = f.read().split("\n\n")
    f.close()

    map_ = array([list(line) for line in inputs[0].splitlines()])
    print_map(map_)

    moves_sequence = list("".join(inputs[1].splitlines())) if "\n" in inputs[1][:-1] else list(inputs[1])[:-1]

    # search robot position
    for i in range(map_.shape[0]):
        for j in range(map_.shape[1]):
            if map_[i, j] == "@":
                robot_position = [i, j]
                break

    # Part 1
    sum_ = part_1(deepcopy(map_), deepcopy(robot_position))
    print(sum_)

    # Part 2
    new_map = expand_map(map_)
    robot_position = [robot_position[0], robot_position[1]*2]
    print_map(new_map)

    # for i in range(len(moves_sequence)):
    #     if i % 10 == 0:
    #         print(i)
    #     print(moves_sequence[i])
    #     new_map, robot_position = move_robot_new_map(new_map, robot_position, moves_sequence[i])
    #     print_map(new_map)
    for move in moves_sequence:
        print(move)
        new_map, robot_position = move_robot_new_map(new_map, robot_position, move)
        # print_map(new_map)

    sum_2 = 0
    for i in range(new_map.shape[0]):
        for j in range(new_map.shape[1]):
            if new_map[i, j] == "[":
                sum_2 += 100 * i + j

    print(sum_2)
