def first_error(XMAS : list[int], pmbl : int) -> int:
    """Find the first item in XMAS which is not the sum of a pair of the
    previous pmbl entries"""
    for i, x in enumerate(XMAS[pmbl:], pmbl):
        # find pair
        found = False
        for j, y in enumerate(XMAS[i - pmbl : i - 1], i - pmbl):
            for z in XMAS[j : i]:
                if y+z == x:
                    found = True
                    break
            if found: break
        
        if not found:
            return x

    return -1

def find_range_with_sum(values : list[int], target : int) -> tuple[int, int]:
    """Given a list of positive integers, find a range which sums to a target
    value."""
    i = j = acc = 0

    while j < len(values):
        if acc == target:
            return i, j
        elif acc < target:
            acc += values[j]
            j += 1
        else:
            acc -= values[i]
            i += 1

    return -1, -1

if __name__ == "__main__":
    with open("input9.txt") as f:
        XMAS = [int(l) for l in f.readlines()]

    error = first_error(XMAS, 25)
    print("First error:", error)

    i, j = find_range_with_sum(XMAS, error)
    section = XMAS[i:j]
    print("Encryption weakness:", min(section) + max(section))
