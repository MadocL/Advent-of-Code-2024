from random import sample


f = open("inputs/day5.txt", "r")
inputs = f.read()
f.close()

inputs = inputs.split("\n\n")
rules = inputs[0].split("\n")
rules = [rule.split("|") for rule in rules]

updates = inputs[1].split("\n")
updates = [update.split(",") for update in updates][:-1]

# Part 1
is_updates_ok = [True]*len(updates)

for rule in rules:
    for i in range(len(updates)):
        if rule[0] in updates[i] and rule[1] in updates[i]:
            if updates[i].index(rule[0]) > updates[i].index(rule[1]):
                is_updates_ok[i] = False

sum_ = 0
for i in range(len(updates)):
    if is_updates_ok[i]:
        sum_ += int(updates[i][int(len(updates[i])/2)])

print(sum_)

# Part 2


def re_order_update(update, rules_subset):
    j = 0
    while j < len(rules_subset):
        rule = rules_subset[j]
        if update.index(rule[0]) > update.index(rule[1]):
            if (
                violated_rules_count(swap_left_to_right(update, update.index(rule[1])), rules_subset)
                < violated_rules_count(swap_right_to_left(update, update.index(rule[0])), rules_subset)
            ):
                update = swap_left_to_right(update, update.index(rule[1]))
            else:
                update = swap_right_to_left(update, update.index(rule[0]))
            rules_subset = sample(rules_subset, len(rules_subset))
            j = 0
        else:
            j += 1

    return update


def violated_rules_count(update, rules_subset):
    violated_rules_count_per_value = [0]*len(update)

    for rule in rules_subset:
        if update.index(rule[0]) > update.index(rule[1]):
            violated_rules_count_per_value[update.index(rule[0])] += 1
            violated_rules_count_per_value[update.index(rule[1])] += 1

    return sum(violated_rules_count_per_value)


def swap_left_to_right(update, index):
    if index == len(update) - 1:
        return update

    temp = update[index]
    update[index] = update[index + 1]
    update[index + 1] = temp

    return update


def swap_right_to_left(update, index):
    if index == 0:
        return update

    temp = update[index]
    update[index] = update[index - 1]
    update[index - 1] = temp

    return update


for i in range(len(is_updates_ok)):
    if not is_updates_ok[i]:
        rules_subset = []
        for rule in rules:
            if rule[0] in updates[i] and rule[1] in updates[i]:
                rules_subset.append(rule)

        print(f"update n° {i}")
        updates[i] = re_order_update(updates[i], rules_subset)

sum_2 = 0
for i in range(len(updates)):
    if not is_updates_ok[i]:
        sum_2 += int(updates[i][int(len(updates[i])/2)])

print(sum_2)
