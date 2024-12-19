def find_towels_for(design, patterns, memoize, return_arrangements_count=False):
    if design == "":
        if return_arrangements_count:
            return 1
        return True

    if memoize.get(design, None) is not None:
        return memoize[design]

    usable_patterns = []

    for pattern in patterns:
        if pattern == design[:len(pattern)]:
            usable_patterns.append(pattern)

    if return_arrangements_count:
        result = sum([
            find_towels_for(design[len(pattern):], patterns, memoize, return_arrangements_count=True)
            for pattern in usable_patterns
        ])
    else:
        result = any([find_towels_for(design[len(pattern):], patterns, memoize) for pattern in usable_patterns])

    memoize[design] = result
    return result


if __name__ == "__main__":
    f = open("inputs/day19.txt", "r")
    inputs = f.read().split("\n\n")
    f.close()

    patterns = inputs[0].split(", ")
    designs = inputs[1].splitlines()
    memoize = {}

    # Part 1
    possible_designs_count = 0
    for design in designs:
        if find_towels_for(design, patterns, memoize):
            possible_designs_count += 1

    print(possible_designs_count)

    # Part 2
    memoize = {}
    arrangements_count = 0

    for design in designs:
        arrangements_count += find_towels_for(design, patterns, memoize, return_arrangements_count=True)

    print(arrangements_count)
