from numpy import array, array_equal, diag, flip

f = open("inputs/day4.txt", "r")
inputs = f.read().splitlines()
f.close()

# Part 1
XMAS_ARRAY = array([ord(char)-ord('A') for char in "XMAS"])  # [23 12  0 18]


def search_in_array(array):
    sub_count = 0

    for i in range(array.shape[0]-XMAS_ARRAY.shape[0]+1):
        if array_equal(array[i:i+XMAS_ARRAY.shape[0]], XMAS_ARRAY):
            sub_count += 1

    return sub_count


def get_diagonales_array(matrix):
    k = 0
    diagonales = []

    while diag(matrix, k=k).size != 0:
        diagonales.append(diag(matrix, k=k))
        k += 1

    k = -1
    while diag(matrix, k=k).size != 0:
        diagonales.append(diag(matrix, k=k))
        k -= 1

    return diagonales


xmas_matrix = array([[ord(char)-ord('A') for char in line] for line in inputs])
count = 0

# lines
for i in range(xmas_matrix.shape[1]):
    count += search_in_array(xmas_matrix[i])
    count += search_in_array(xmas_matrix[i][::-1])

# columns
for i in range(xmas_matrix.T.shape[1]):
    count += search_in_array(xmas_matrix.T[i])
    count += search_in_array(xmas_matrix.T[i][::-1])

# diagonales \
for diagonale in get_diagonales_array(xmas_matrix):
    if diagonale.size >= 4:
        count += search_in_array(diagonale)
        count += search_in_array(diagonale[::-1])

# diagonales /
for diagonale in get_diagonales_array(flip(xmas_matrix, 0)):
    if diagonale.size >= 4:
        count += search_in_array(diagonale)
        count += search_in_array(diagonale[::-1])

print(count)

M_value = ord('M')-ord('A')
A_value = ord('A')-ord('A')
S_value = ord('S')-ord('A')

# Part 2

count_2 = 0

for i in range(1, xmas_matrix.shape[0]-1):
    for j in range(1, xmas_matrix.shape[1]-1):
        if xmas_matrix[i, j] != A_value:
            continue
        if (
            xmas_matrix[i-1, j-1] == M_value
            and xmas_matrix[i+1, j-1] == M_value  # M.M
            and xmas_matrix[i-1, j+1] == S_value  # .A.
            and xmas_matrix[i+1, j+1] == S_value  # S.S
        ):
            count_2 += 1
        elif (
            xmas_matrix[i-1, j-1] == S_value
            and xmas_matrix[i+1, j-1] == S_value  # S.S
            and xmas_matrix[i-1, j+1] == M_value  # .A.
            and xmas_matrix[i+1, j+1] == M_value  # M.M
        ):
            count_2 += 1
        elif (
            xmas_matrix[i-1, j-1] == M_value
            and xmas_matrix[i+1, j-1] == S_value  # M.S
            and xmas_matrix[i-1, j+1] == M_value  # .A.
            and xmas_matrix[i+1, j+1] == S_value  # M.S
        ):
            count_2 += 1
        elif (
            xmas_matrix[i-1, j-1] == S_value
            and xmas_matrix[i+1, j-1] == M_value  # S.M
            and xmas_matrix[i-1, j+1] == S_value  # .A.
            and xmas_matrix[i+1, j+1] == M_value  # S.M
        ):
            count_2 += 1

print(count_2)
