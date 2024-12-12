def search_region(i, j, inputs):
    stack = [(i, j)]
    region = set()
    perimeter = 0

    while len(stack) > 0:
        current_coords = stack[0]
        stack.remove(current_coords)
        region.add(current_coords)

        for neighbour in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            neighbour_coords = (current_coords[0] + neighbour[0], current_coords[1] + neighbour[1])
            if (
                0 <= neighbour_coords[0] < len(inputs)
                and 0 <= neighbour_coords[1] < len(inputs[neighbour_coords[0]])
                and inputs[neighbour_coords[0]][neighbour_coords[1]] == inputs[current_coords[0]][current_coords[1]]
                and neighbour_coords not in region
                and neighbour_coords not in stack
            ):
                stack.append(neighbour_coords)
            elif (
                not 0 <= neighbour_coords[0] < len(inputs)
                or not 0 <= neighbour_coords[1] < len(inputs[neighbour_coords[0]])
                or inputs[neighbour_coords[0]][neighbour_coords[1]] != inputs[current_coords[0]][current_coords[1]]
            ):
                perimeter += 1

    return inputs[current_coords[0]][current_coords[1]], region, perimeter


def count_region_sides(region, inputs):
    # counting the corners is like counting the sides
    corner_count = 0

    for coords in region:
        for corner_neighbours in [
            [(-1, -1), (-1, 0), (0, -1)],  # upper left
            [(-1,  1), (-1, 0), (0,  1)],  # upper right
            [( 1, -1), ( 1, 0), (0, -1)],  # lower left
            [( 1,  1), ( 1, 0), (0,  1)],  # lower right
        ]:
            neighbours_coords = [
                (coords[0] + neighbour[0], coords[1] + neighbour[1]) 
                for neighbour in corner_neighbours
            ]

            if (
                # overflow at the upper left bound
                not 0 <= neighbours_coords[0][0] < len(inputs) and not 0 <= neighbours_coords[0][1] < len(inputs[0])
                # overflow at the upper right bound
                or not 0 <= neighbours_coords[0][0] < len(inputs) and not 0 <= neighbours_coords[2][1] < len(inputs[0])
                # overflow at the lower left bound
                or not 0 <= neighbours_coords[2][0] < len(inputs) and not 0 <= neighbours_coords[0][1] < len(inputs[0])
                # overflow at the lower right bound
                or not 0 <= neighbours_coords[2][0] < len(inputs) and not 0 <= neighbours_coords[2][1] < len(inputs[0])
            ):
                corner_count += 1

            elif not 0 <= neighbours_coords[0][0] < len(inputs):  # overflow at the lower or upper bound
                if inputs[neighbours_coords[2][0]][neighbours_coords[2][1]] != inputs[coords[0]][coords[1]]:
                    corner_count += 1

            elif not 0 <= neighbours_coords[0][1] < len(inputs[0]):  # overflow at the left or right bound
                if inputs[neighbours_coords[1][0]][neighbours_coords[1][1]] != inputs[coords[0]][coords[1]]:
                    corner_count += 1

            else:
                if (
                    inputs[neighbours_coords[0][0]][neighbours_coords[0][1]] != inputs[coords[0]][coords[1]]
                    and inputs[neighbours_coords[1][0]][neighbours_coords[1][1]] == inputs[coords[0]][coords[1]]
                    and inputs[neighbours_coords[2][0]][neighbours_coords[2][1]] == inputs[coords[0]][coords[1]]
                ):
                    corner_count += 1
                if (
                    # inputs[neighbours_coords[0][0]][neighbours_coords[0][1]] != inputs[coords[0]][coords[1]]
                    inputs[neighbours_coords[1][0]][neighbours_coords[1][1]] != inputs[coords[0]][coords[1]]
                    and inputs[neighbours_coords[2][0]][neighbours_coords[2][1]] != inputs[coords[0]][coords[1]]
                ):
                    corner_count += 1

    return corner_count


if __name__ == "__main__":
    f = open("inputs/day12.txt", "r")
    inputs = f.read().splitlines()
    f.close()

    # Part 1
    regions = []
    visited = set()
    # search regions
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if (i, j) not in visited:
                plant_type, region, perimeter = search_region(i, j, inputs)
                visited = visited.union(region)
                regions.append((plant_type, region, perimeter))

    # for plant_type, region, perimeter in regions:
    #     print(f"{plant_type}\t{len(region)}\t{perimeter}\t{sorted(region)}")

    print(sum([len(region) * perimeter for _, region, perimeter in regions]))

    # Part 2
    sum_ = 0
    for plant_type, region, _, in regions:
        sides_count = count_region_sides(region, inputs)
        sum_ += len(region) * sides_count
        # print(f"{plant_type}\t{len(region)}\t{sides_count}")

    print(sum_)
