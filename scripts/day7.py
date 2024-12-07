from copy import deepcopy


f = open("inputs/day7.txt", "r")
inputs = f.read().splitlines()
f.close()

inputs = [line.split(": ") for line in inputs]
for line in inputs:
    line[0] = int(line[0])
    line[1] = list(map(int, line[1].split(" ")))


def multiply(x, y): return x*y
def add(x, y): return x+y
def concatenate(x, y): return int(str(x) + str(y))


def test_equation(target, values, concatenate_operator=False):
    results = []
    values.reverse()

    while len(values) > 0:
        if len(results) == 0:
            results.append(values.pop())
        else:
            if concatenate_operator:
                results = results*3
                bounds_and_func = [
                    [(0, int(len(results)/3)), multiply],
                    [(1*int(len(results)/3), 2*int(len(results)/3)), add],
                    [(2*int(len(results)/3), len(results)), concatenate],
                ]
            else:
                results = results*2
                bounds_and_func = [
                    [(0, int(len(results)/2)), multiply],
                    [(int(len(results)/2), len(results)), add],
                ]

            next_value = values.pop()

            for i in range(len(bounds_and_func)):
                for j in range(*bounds_and_func[i][0]):
                    results[j] = bounds_and_func[i][1](results[j], next_value)

    for result in results:
        if result == target:
            return True

    return False


sum_ = sum_2 = 0
for target, values in inputs:
    if test_equation(target, deepcopy(values)):  # Part 1
        sum_ += target
    if test_equation(target, deepcopy(values), concatenate_operator=True):  # Part 2
        sum_2 += target

print(sum_)
print(sum_2)
