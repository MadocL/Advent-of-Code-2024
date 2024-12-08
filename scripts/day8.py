def load_inputs():
    f = open("inputs/day8.txt", "r")
    inputs = f.read().splitlines()
    f.close()

    return [list(line) for line in inputs]


def search_antennas(inputs):
    antennas = dict()

    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if inputs[i][j] != ".":
                if antennas.get(inputs[i][j]) is None:
                    antennas[inputs[i][j]] = [(i, j)]
                else:
                    antennas[inputs[i][j]].append((i, j))

    return antennas


def search_all_antinodes(antennas_subset, bounds, only_first_antinodes=False):
    # search all antinodes for a given antenna type
    antinodes = set()

    for i in range(len(antennas_subset)):
        for j in range(i+1, len(antennas_subset)):
            if only_first_antinodes:
                antinodes.update(
                    search_antinodes_for(antennas_subset[i], antennas_subset[j], bounds, only_first_antinodes=True)
                )
            else:
                antinodes.update(
                    search_antinodes_for(antennas_subset[i], antennas_subset[j], bounds, only_first_antinodes=False)
                )

    return antinodes


def search_antinodes_for(antenna_1, antenna_2, bounds, only_first_antinodes=False):
    antinodes = set()
    delta = (antenna_1[0] - antenna_2[0], antenna_1[1] - antenna_2[1])

    k = 1 if only_first_antinodes else 0

    while (
        0 <= antenna_1[0] + k*delta[0] < bounds[0]
        and 0 <= antenna_1[1] + k*delta[1] < bounds[1]
    ):
        antinodes.add((antenna_1[0] + k*delta[0], antenna_1[1] + k*delta[1]))
        if only_first_antinodes:
            break
        k += 1

    k = 1 if only_first_antinodes else 0

    while (
        0 <= antenna_2[0] - k*delta[0] < bounds[0]
        and 0 <= antenna_2[1] - k*delta[1] < bounds[1]
    ):
        antinodes.add((antenna_2[0] - k*delta[0], antenna_2[1] - k*delta[1]))
        if only_first_antinodes:
            break
        k += 1

    return antinodes


if __name__ == "__main__":
    inputs = load_inputs()
    bounds = (len(inputs), len(inputs[0]))
    antennas = search_antennas(inputs)

    antinodes = set()
    antinodes_2 = set()

    for antenna_type in antennas.keys():
        antennas_subset = antennas[antenna_type]
        # print(f"{antenna_type}\t{antennas_subset}")

        antinodes.update(search_all_antinodes(antennas_subset, bounds, only_first_antinodes=True))  # Part 1
        antinodes_2.update(search_all_antinodes(antennas_subset, bounds))  # Part 2

    print(len(antinodes))
    print(len(antinodes_2))
