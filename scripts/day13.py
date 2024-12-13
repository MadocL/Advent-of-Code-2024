from decimal import Decimal


def parse_inputs(inputs):
    return [
        [
            [
                Decimal(config[0].split(" ")[2].split("+")[1][:-1]),
                Decimal(config[0].split(" ")[3].split("+")[1]),
            ],
            [
                Decimal(config[1].split(" ")[2].split("+")[1][:-1]),
                Decimal(config[1].split(" ")[3].split("+")[1]),
            ],
            [
                Decimal(config[2].split(" ")[1].split("=")[1][:-1]),
                Decimal(config[2].split(" ")[2].split("=")[1]),
            ],
        ]
        for config in [config.split("\n") for config in inputs]
    ]


def compute_solutions(machine_config):
    x_a = machine_config[0][0]
    y_a = machine_config[0][1]
    x_b = machine_config[1][0]
    y_b = machine_config[1][1]
    X = machine_config[2][0]
    Y = machine_config[2][1]

    k_b = (Y - ((y_a * X) / (x_a))) / (y_b - ((y_a * x_b) / (x_a)))
    k_a = (X - x_b * k_b) / (x_a)

    return float(k_a), float(k_b)


if __name__ == "__main__":
    # f = open("inputs/day13_example.txt", "r")
    f = open("inputs/day13.txt", "r")
    inputs = f.read().split("\n\n")
    f.close()

    machine_configs = parse_inputs(inputs)
    sum_ = 0

    # Part 1
    for config in machine_configs:
        k_a, k_b = compute_solutions(config)

        if int(k_a) == k_a and int(k_b) == k_b and k_a <= 100 and k_b <= 100:
            sum_ += 3*int(k_a) + int(k_b)

    print(sum_)

    # Part 2
    sum_2 = 0

    for config in machine_configs:
        config[2][0] += Decimal("10000000000000")
        config[2][1] += Decimal("10000000000000")

        k_a, k_b = compute_solutions(config)

        if int(k_a) == k_a and int(k_b) == k_b:
            sum_2 += 3*int(k_a) + int(k_b)

    print(sum_2)
