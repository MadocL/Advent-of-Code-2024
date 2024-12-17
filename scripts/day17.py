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
            result = registers[0] / 2**combo_operand
            registers[0] = int(result)
        elif instruction == 1:  # bxl
            result = registers[1] ^ operand
            registers[1] = result
        elif instruction == 2:  # bst
            result = combo_operand % 8
            registers[1] = result
        elif instruction == 3:  # jnz
            if registers[0] != 0:
                i = operand - 2
        elif instruction == 4:  # bxc
            result = registers[1] ^ registers[2]
            registers[1] = result
        elif instruction == 5:  # out
            result = combo_operand % 8
            outputs.append(result)
        elif instruction == 6:  # bdv
            result = registers[0] / 2**combo_operand
            registers[1] = int(result)
        elif instruction == 7:  # cdv
            result = registers[0] / 2**combo_operand
            registers[2] = int(result)

        i += 2

    return outputs


def worker_task(start, end, program):
    # start, end, program = args

    outputs = []
    i = start
    while outputs != program and i < end:
        if i % 1000000 == 0:
            print(i)
        # print(f"{i=}, {outputs=}, {program=}")
        registers = [i, 0, 0]
        outputs = compute_program(program, registers)
        i += 1

    if outputs == program:
        print(",".join([str(value) for value in outputs]))
        print(i-1)


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

    # Part 2
    # outputs = []
    # i = 0

    # while outputs != program:
    #     # print(f"{i=}, {outputs=}, {program=}")
    #     registers = [i, 0, 0]
    #     outputs = compute_program(program, registers)
    #     i += 1

    # print(",".join([str(value) for value in outputs]))
    # print(i-1)

    target_outputs = program
    max_iterations = 1000000000

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
