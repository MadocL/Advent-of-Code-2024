def find_end_positions(i, j):
    if inputs[i][j] == 9:
        return [(i, j)]

    end_positions_coords = []

    for neighbour in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbour_i, neighbour_j = i + neighbour[0], j + neighbour[1]
        if (
            0 <= neighbour_i < len(inputs) and 0 <= neighbour_j < len(inputs[0])
            and inputs[neighbour_i][neighbour_j] == inputs[i][j] + 1
        ):
            end_positions_coords.extend(find_end_positions(neighbour_i, neighbour_j))

    return end_positions_coords


if __name__ == "__main__":
    f = open("inputs/day10.txt", "r")
    inputs = f.read().splitlines()
    f.close()

    inputs = [[int(value) for value in list(line)] for line in inputs]
    scores = [[0]*len(inputs[0]) for _ in range(len(inputs))]
    ratings = [[0]*len(inputs[0]) for _ in range(len(inputs))]

    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if inputs[i][j] == 0:
                end_positions = find_end_positions(i, j)
                ratings[i][j] = len(end_positions)  # Part 1
                scores[i][j] = len(set(end_positions))  # Part 2

    sum_ = sum([sum(line) for line in scores])
    sum_ratings = sum([sum(line) for line in ratings])

    print(sum_)
    print(sum_ratings)
