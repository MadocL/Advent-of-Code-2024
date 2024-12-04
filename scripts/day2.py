
def is_sorted(input_, reverse=False):
    if reverse:
        for i in range(len(input_)-1):
            if input_[i] <= input_[i+1]:
                return False
    else:
        for i in range(len(input_)-1):
            if input_[i] >= input_[i+1]:
                return False

    return True


f = open("inputs/day2.txt", "r")
lines = f.read().splitlines()
inputs = [list(map(int, line.split(" "))) for line in lines]
f.close()

# Part 1
sum_ = 0
for input_ in inputs:
    # print(input_)
    if not is_sorted(input_) and not is_sorted(input_, reverse=True):
        continue

    is_steps_correct = True
    for i in range(len(input_)-1):
        if not (1 <= abs(input_[i] - input_[i+1]) <= 3):
            is_steps_correct = False
            break
    if not is_steps_correct:
        continue
    sum_ += 1

print(sum_)

# Part 2


def check_is_safe(input_, is_retry=False):
    print(input_)
    is_safe_ = True
    if not is_sorted(input_) and not is_sorted(input_, reverse=True):
        is_safe_ = False
        print("NOT ORDERED")

    for i in range(len(input_)-1):
        if not (1 <= abs(input_[i] - input_[i+1]) <= 3):
            is_safe_ = False
            print("STEPS NOT CORRECT")
            break

    if is_safe_:
        return True

    if not is_safe_ and not is_retry:
        for i in range(len(input_)):
            if check_is_safe(input_[:i] + input_[i+1:], is_retry=True):
                print("CORRECT FOR THIS SUB LIST")
                return True

        print("TOTALLY INCORRECT")
        return False


sum_2 = 0
for input_ in inputs:
    if check_is_safe(input_):
        sum_2 += 1

print(sum_2)
