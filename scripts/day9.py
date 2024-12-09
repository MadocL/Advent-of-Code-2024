
def develop_memory(inputs):
    developed_memory = []
    for i in range(len(inputs)):
        if i % 2 == 0:
            developed_memory.extend([int(i/2)] * inputs[i])
        else:
            developed_memory.extend(["."] * inputs[i])

    return developed_memory


f = open("inputs/day9.txt", "r")
inputs = list(f.read())[:-1]
f.close()

inputs = [int(value) for value in inputs]

# Part 1
developed_memory = develop_memory(inputs)

while "." in developed_memory:
    first_free_space_idx = developed_memory.index(".")
    developed_memory[first_free_space_idx] = developed_memory.pop()

sum_ = 0
for i in range(len(developed_memory)):
    sum_ += i * developed_memory[i]

print(sum_)


# Part 2
developed_memory = develop_memory(inputs)
current_block = None
block_size = 0

for i in range(len(developed_memory)-1, -1, -1):
    print(i)
    if current_block is None and developed_memory[i] != ".":
        current_block = developed_memory[i]
        block_size = 1
    else:
        if developed_memory[i] == current_block:
            block_size += 1
        else:
            # search new possible location
            free_space_count = 0
            j = 0
            while j <= i and free_space_count < block_size:
                if developed_memory[j] == ".":
                    free_space_count += 1
                else:
                    free_space_count = 0
                j += 1

            # move file if new location found
            if free_space_count >= block_size:
                for k in range(block_size):
                    developed_memory[j - block_size + k] = current_block
                    developed_memory[i + 1 + k] = "."

            # reset variables
            if developed_memory[i] == ".":
                current_block = None
                block_size = 0
            else:
                current_block = developed_memory[i]
                block_size = 1

sum_2 = 0
for i in range(len(developed_memory)):
    if developed_memory[i] != ".":
        sum_2 += i * developed_memory[i]

print(sum_2)
