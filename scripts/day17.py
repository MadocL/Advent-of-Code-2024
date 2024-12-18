from multiprocessing import Process, cpu_count


def compute_program(program, registers):
    outputs = []
    i = 0

    while i < len(program):
        instruction = program[i]
        operand = program[i + 1]

        if operand in [0, 1, 2, 3]:
            combo_operand = operand
        elif operand == 4:
            combo_operand = registers[0]
        elif operand == 5:
            combo_operand = registers[1]
        elif operand == 6:
            combo_operand = registers[2]

        if instruction == 0:  # adv
            registers[0] = int(registers[0] / 2**combo_operand)
        elif instruction == 1:  # bxl
            registers[1] = registers[1] ^ operand
        elif instruction == 2:  # bst
            registers[1] = combo_operand % 8
        elif instruction == 3:  # jnz
            if registers[0] != 0:
                i = operand - 2
        elif instruction == 4:  # bxc
            registers[1] = registers[1] ^ registers[2]
        elif instruction == 5:  # out
            outputs.append(combo_operand % 8)
        elif instruction == 6:  # bdv
            registers[1] = int(registers[0] / 2**combo_operand)
        elif instruction == 7:  # cdv
            registers[2] = int(registers[0] / 2**combo_operand)

        i += 2

    return outputs


def worker_task(start, end, program):
    outputs = []
    i = start

    while outputs != program and i < end:
        registers = [i, 0, 0]
        outputs = compute_program(program, registers)
        i += 1

    if outputs == program:
        print(",".join([str(value) for value in outputs]))
        print(i-1)


def brute_force_part2(program):
    max_iterations = 10**9
    segment = max_iterations // cpu_count()
    processes = []

    for i in range(cpu_count()):
        start = i * segment
        end = start + segment

        p = Process(target=worker_task, args=(start, end, program))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    # f = open("inputs/day17_small.txt", "r")
    # f = open("inputs/day17_small2.txt", "r")
    f = open("inputs/day17.txt", "r")
    inputs = f.read().split("\n\n")
    f.close()

    registers = [int(line.split(": ")[1]) for line in inputs[0].splitlines()]
    program = [int(value) for value in inputs[1].split(": ")[1].split(",")]

    # Part 1
    outputs = compute_program(program, registers)
    print(",".join([str(value) for value in outputs]))

    # Part 2:  trying brute force: impossible to solve in a reasonable time
    # brute_force_part2(program)

    # decomposed program
    a = 62769524
    b = 0
    c = 0
    outputs = []

    while a != 0:
        b = int(a / (2**((a % 8) ^ 7)))

        result = (a % 8) ^ 7
        result = result ^ b
        result = result ^ 7
        result = result % 8
        outputs.append(str(result))

        # outputs.append(str(((((a % 8) ^ 7) ^ int(a / (2**((a % 8) ^ 7)))) ^ 7) % 8))  # one-line version

        a = int(a / 8)

    print(",".join(outputs))
