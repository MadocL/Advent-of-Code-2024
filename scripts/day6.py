from copy import deepcopy


def load_inputs():
    f = open("inputs/day6.txt", "r")
    inputs = f.read().splitlines()
    f.close()

    return [list(line) for line in inputs]  # convert string into char array


def search_guard_position_and_facing(inputs):
    guard_pos = None

    # search guard position
    for i in range(len(inputs)):
        for j in range(len(inputs[0])):
            if inputs[i][j] not in ["#", "."]:
                guard_pos = [i, j]

                if inputs[i][j] == "^":
                    facing = "up"
                elif inputs[i][j] == "<":
                    facing = "left"
                elif inputs[i][j] == ">":
                    facing = "right"
                elif inputs[i][j] == "v":
                    facing = "down"
                break
        if guard_pos is not None:
            break

    return guard_pos, facing


# Part 1

inputs = load_inputs()
guard_pos, facing = search_guard_position_and_facing(inputs)

# walking
while (True):
    if facing == "up":
        if guard_pos[0] - 1 < 0:
            break
        if inputs[guard_pos[0]-1][guard_pos[1]] == "#":
            facing = "right"
        else:
            inputs[guard_pos[0]][guard_pos[1]] = "X"
            guard_pos[0] -= 1

    elif facing == "down":
        if guard_pos[0] + 1 >= len(inputs):
            break
        if inputs[guard_pos[0]+1][guard_pos[1]] == "#":
            facing = "left"
        else:
            inputs[guard_pos[0]][guard_pos[1]] = "X"
            guard_pos[0] += 1

    elif facing == "left":
        if guard_pos[1] - 1 < 0:
            break
        if inputs[guard_pos[0]][guard_pos[1]-1] == "#":
            facing = "up"
        else:
            inputs[guard_pos[0]][guard_pos[1]] = "X"
            guard_pos[1] -= 1

    elif facing == "right":
        if guard_pos[1] + 1 >= len(inputs[0]):
            break
        if inputs[guard_pos[0]][guard_pos[1]+1] == "#":
            facing = "down"
        else:
            inputs[guard_pos[0]][guard_pos[1]] = "X"
            guard_pos[1] += 1

inputs[guard_pos[0]][guard_pos[1]] = "X"

count = 0
# count distinct positions
for i in range(len(inputs)):
    for j in range(len(inputs[0])):
        if inputs[i][j] == "X":
            count += 1


print(count)

# Part 2


def is_stuck_in_loop(inputs, guard_pos, facing, i, j):
    rotation_positions = []
    inputs[i][j] = "O"
    is_stuck = False

    while (True):
        # loop detection
        for i in range(len(rotation_positions)-2):
            if rotation_positions[i] == rotation_positions[-1]:
                is_stuck = True
                break

        if is_stuck:
            break

        if facing == "up":
            if guard_pos[0] - 1 < 0:
                break
            if inputs[guard_pos[0]-1][guard_pos[1]] in ["#", "O"]:
                facing = "right"
                inputs[guard_pos[0]][guard_pos[1]] = "+"
                rotation_positions.append([guard_pos[0], guard_pos[1]])
            else:
                guard_pos[0] -= 1

        elif facing == "down":
            if guard_pos[0] + 1 >= len(inputs):
                break
            if inputs[guard_pos[0]+1][guard_pos[1]] in ["#", "O"]:
                facing = "left"
                inputs[guard_pos[0]][guard_pos[1]] = "+"
                rotation_positions.append([guard_pos[0], guard_pos[1]])
            else:
                guard_pos[0] += 1

        elif facing == "left":
            if guard_pos[1] - 1 < 0:
                break
            if inputs[guard_pos[0]][guard_pos[1]-1] in ["#", "O"]:
                facing = "up"
                inputs[guard_pos[0]][guard_pos[1]] = "+"
                rotation_positions.append([guard_pos[0], guard_pos[1]])
            else:
                guard_pos[1] -= 1

        elif facing == "right":
            if guard_pos[1] + 1 >= len(inputs[0]):
                break
            if inputs[guard_pos[0]][guard_pos[1]+1] in ["#", "O"]:
                facing = "down"
                inputs[guard_pos[0]][guard_pos[1]] = "+"
                rotation_positions.append([guard_pos[0], guard_pos[1]])
            else:
                guard_pos[1] += 1

    return is_stuck


inputs = load_inputs()
guard_pos, facing = search_guard_position_and_facing(inputs)

count_2 = 0
for i in range(len(inputs)):
    for j in range(len(inputs[0])):
        if i == guard_pos[0] and j == guard_pos[1]:
            continue
        if is_stuck_in_loop(deepcopy(inputs), deepcopy(guard_pos), deepcopy(facing), i, j):
            print(
                f"[{i*len(inputs[0])+j}/{len(inputs)*len(inputs[0])}] "
                f"({round((i*len(inputs[0])+j)/(len(inputs)*len(inputs[0]))*100, ndigits=2)}%)"
            )
            count_2 += 1

print(count_2)
