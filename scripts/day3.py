from re import findall

pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"

f = open("inputs/day3.txt", "r")
inputs = f.read()
f.close()

# Part 1
sum_ = 0
instructions = findall(pattern, inputs)
for instruction in instructions:
    x, y = instruction[4:-1].split(",")
    sum_ += int(x) * int(y)

print(sum_)


# Part 2

instructions = []

split_by_dont = inputs.split("don't()")
instructions.extend(findall(pattern, split_by_dont[0]))
for i in range(1, len(split_by_dont)):
    split_by_do = split_by_dont[i].split("do()")

    if len(split_by_do) == 1:
        continue
    else:
        for j in range(1, len(split_by_do)):
            instructions.extend(findall(pattern, split_by_do[j]))

# same code as part 1
sum_2 = 0
for instruction in instructions:
    x, y = instruction[4:-1].split(",")
    sum_2 += int(x) * int(y)

print(sum_2)
