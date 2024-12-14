from cv2 import imshow, waitKey, imwrite
from math import prod
from numpy import zeros

WIDTH = 101
HEIGHT = 103


def parse_input(inputs):
    return [
        (
            [
                int(position.split("=")[1].split(",")[0]),
                int(position.split("=")[1].split(",")[1]),
            ],
            [
                int(velocity.split("=")[1].split(",")[0]),
                int(velocity.split("=")[1].split(",")[1]),
            ],
        )
        for position, velocity in [tuple(input_.split(" ")) for input_ in inputs]
    ]


def elapse_x_seconds(x, robots_config):
    return [
        [
            (position[0] + x * velocity[0]) % WIDTH,
            (position[1] + x * velocity[1]) % HEIGHT,
        ]
        for position, velocity in robots_config
    ]


def get_quadrants():
    return [
        [
            [0, WIDTH//2],  # upper left
            [0, HEIGHT//2],
        ],
        [
            [WIDTH//2 + 1, WIDTH],  # upper right
            [0, HEIGHT//2],
        ],
        [
            [0, WIDTH//2],  # lower left
            [HEIGHT//2 + 1, HEIGHT],
        ],
        [
            [WIDTH//2 + 1, WIDTH],  # lower right
            [HEIGHT//2 + 1, HEIGHT],
        ],
    ]


def display(positions, i):
    map_ = zeros((WIDTH, HEIGHT))

    for position in positions:
        map_[position[0], position[1]] += 1

    imwrite(f"day14/{i}.png", map_*255)
    # imshow("bathroom map", map_ * 255)
    # waitKey(1000)


if __name__ == "__main__":
    f = open("inputs/day14.txt", "r")
    inputs = f.read().splitlines()
    f.close()

    robots_config = parse_input(inputs)

    # Part 1
    quadrants = get_quadrants()
    quadrant_counts = [0]*4

    for position in sorted(elapse_x_seconds(100, robots_config)):
        for i in range(len(quadrants)):
            if (
                quadrants[i][0][0] <= position[0] < quadrants[i][0][1]
                and quadrants[i][1][0] <= position[1] < quadrants[i][1][1]
            ):
                quadrant_counts[i] += 1
                break

    print(prod(quadrant_counts))

    # Part 2
    for i in range(1, 10000):
        print(i)
        display(elapse_x_seconds(i, robots_config), i)
        # spotted at 6493 ! :D
