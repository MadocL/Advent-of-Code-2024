def get_stones_resul_list_from(stone, i=1):
    if i == 75:
        if len(str(stone)) % 2 == 0:
            return 2
        return 1

    if memoization.get((stone, i)) is None:
        if stone == 0:
            result = get_stones_resul_list_from(1, i=i+1)
        elif len(str(stone)) % 2 == 0:
            result = (
                get_stones_resul_list_from(int(str(stone)[:len(str(stone))//2]), i=i+1)
                + get_stones_resul_list_from(int(str(stone)[len(str(stone))//2:]), i=i+1)
            )
        else:
            result = get_stones_resul_list_from(stone * 2024, i=i+1)

        memoization[(stone, i)] = result

    return memoization.get((stone, i))


if __name__ == "__main__":
    f = open("inputs/day11.txt", "r")
    inputs = [int(value) for value in f.read().split(" ")]
    f.close()

    # Part 1
    stones_list = inputs

    for i in range(25):
        new_stones_list = []

        for stone in stones_list:
            if stone == 0:
                new_stones_list.append(1)
            elif len(str(stone)) % 2 == 0:
                new_stones_list.append(int(str(stone)[:len(str(stone))//2]))
                new_stones_list.append(int(str(stone)[len(str(stone))//2:]))
            else:
                new_stones_list.append(stone * 2024)

        stones_list = new_stones_list

    print(len(stones_list))

    # Part 2
    memoization = {}
    count = 0
    for stone in inputs:
        count += get_stones_resul_list_from(stone)

    print(count)
