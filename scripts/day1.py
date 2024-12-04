

f = open("inputs/day1.txt", "r")
lines = f.read().splitlines()
inputs = [tuple(map(int, line.split("   "))) for line in lines]
f.close()

# Part 1
array1, array2 = [], []
for x, y in inputs:
    array1.append(x)
    array2.append(y)

array1.sort()
array2.sort()

sum_ = 0
for i in range(len(array1)):
    sum_ += abs(array1[i] - array2[i])

print(sum_)


# Part 2
similarity_score = 0
for value in array1:
    similarity_score += value * len(list(filter(lambda x: x == value, array2)))

print(similarity_score)
