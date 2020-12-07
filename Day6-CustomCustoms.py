def count_any_yes(group : str) -> int:
    return len(set(group.replace("\n",""))) # exclude the newline

def count_all_yes(group : str) -> int:
    yes = set(chr(i) for i in range(ord("a"), ord("z") + 1))
    for person in group.split("\n"):
        if person: # might have an empty line at end
            yes &= set(person)

    return len(yes)

if __name__ == "__main__":
    with open("input6.txt") as f:
        groups = f.read().split("\n\n")
    
    print("Sum of counts is:")
    print(sum(map(count_any_yes, groups)))
    print(sum(map(count_all_yes, groups)))
