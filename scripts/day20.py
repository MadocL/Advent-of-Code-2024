from rich.console import Console
from numpy import array


def print_inputs(inputs, char_to_reverse=None):
    """custom print"""
    console = Console()
    for i in range(inputs.shape[0]):
        for j in range(inputs.shape[1]):
            if (i, j) in char_to_reverse:
                console.print(inputs[i, j], end="", style="reverse")
            else:
                print(inputs[i, j], end="")
        print("")
    print("")


def init_scores(inputs, start, end):
    previous_position = None
    current_position = start
    current_score = 0
    scores = {current_position: 0}

    while current_position != end:
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = (current_position[0] + move[0], current_position[1] + move[1])

            if inputs[neighbour] != "#" and previous_position != neighbour:
                previous_position = current_position
                current_position = neighbour
                current_score += 1
                scores[current_position] = current_score
                break

    return scores


def search_cheats(inputs, start, end, scores):
    cheats = {}
    previous_position = None
    current_position = start

    while current_position != end:
        # print_inputs(inputs, char_to_reverse={current_position})

        for next_position, second_order_next_position in [
            ((current_position[0], current_position[1] + 1), (current_position[0], current_position[1] + 2)),  # right
            ((current_position[0], current_position[1] - 1), (current_position[0], current_position[1] - 2)),  # left
            ((current_position[0] + 1, current_position[1]), (current_position[0] + 2, current_position[1])),  # down
            ((current_position[0] - 1, current_position[1]), (current_position[0] - 2, current_position[1])),  # up
        ]:
            if (
                inputs[next_position] == "#"
                and 0 <= second_order_next_position[0] < inputs.shape[0]  # inside map bounds
                and 0 <= second_order_next_position[1] < inputs.shape[1]  # inside map bounds
                and inputs[second_order_next_position] in [".", "E"]
                and scores[second_order_next_position] >= scores[current_position] + 2
            ):
                cheats[(current_position, second_order_next_position)] = (
                    scores[second_order_next_position] - (scores[current_position] + 2)
                )

        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = (current_position[0] + move[0], current_position[1] + move[1])

            if inputs[neighbour] != "#" and previous_position != neighbour:
                previous_position = current_position
                current_position = neighbour
                break

    return cheats


def search_larger_cheats(inputs, start, end, scores):
    cheats = []
    previous_position = None
    current_position = start

    while current_position != end:
        # print_inputs(inputs, char_to_reverse={current_position})

        last_cheat_step_scores = search_cheats_from_cell(inputs, scores, start, visited=set())
        for cheat_end, cell_score, cheat_picoseconds in last_cheat_step_scores:
            if cell_score >= scores[current_position] + cheat_picoseconds:
                saved_picoseconds = cell_score - (scores[current_position] + cheat_picoseconds)
                cheats.append((current_position, cheat_end, saved_picoseconds))

        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbour = (current_position[0] + move[0], current_position[1] + move[1])

            if inputs[neighbour] != "#" and previous_position != neighbour:
                previous_position = current_position
                current_position = neighbour
                break

    return cheats


def search_cheats_from_cell(inputs, scores, start, visited, picoseconds_left=20):
    if inputs[start] in [".", "E"]:
        # print_inputs(inputs, char_to_reverse={(3, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (7, 3)})
        return [(start, scores[start], 20 - picoseconds_left)]

    if picoseconds_left == 1:
        return []

    # print_inputs(inputs, char_to_reverse=visited)
    last_cheat_step_scores = []

    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

        neighbour = (start[0] + move[0], start[1] + move[1])
        if (
            neighbour not in visited
            and 0 <= neighbour[0] < inputs.shape[0] and 0 <= neighbour[1] < inputs.shape[1]  # inside map bounds
            # and inputs[neighbour] == "#"
        ):
            last_cheat_step_scores += search_cheats_from_cell(
                inputs, scores,
                start=neighbour,
                visited=(visited | {start}),
                picoseconds_left=picoseconds_left - 1,
            )

    return last_cheat_step_scores


if __name__ == "__main__":
    # f = open("inputs/day20_small.txt", "r")
    f = open("inputs/day20.txt", "r")
    inputs = array([list(line) for line in f.read().splitlines()])
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
    scores = init_scores(inputs, start, end)
    cheats = search_cheats(inputs, start, end, scores)

    print(len(list(filter(lambda x: x[1] >= 100, cheats.items()))))

    # Part 2
    larger_cheats = search_larger_cheats(inputs, start, end, scores)
    # print(larger_cheats)

    for start, end, score in filter(lambda x: x[2] >= 50, sorted(larger_cheats, key=lambda x: x[2])):
        print(f"{start},{end}\t{score}")
