from collections import Counter

def diff_counts(values : list[int]) -> dict[int, int]:
    """Count the gaps between ordered elements in a list, by size."""
    ordered = [0] + sorted(values) + [max(values) + 3]

    return Counter(j - i for i, j in zip(ordered, ordered[1:]))

def count_orders(values : list[int], max_diff : int) -> int:
    """Count the valid progressions through the values with a maximum jump size."""
    ordered = [0] + sorted(values) + [max(values) + 3]
    options = [0] * len(ordered)
    options[0] = 1

    # Each element of options should be the sum of all prior elements
    # where the difference between the matching values in ordered is less than
    # max_diff
    for i, val in enumerate(ordered[1:], 1):
        for j in range(i-1, -1, -1):
            if val - ordered[j] > max_diff:
                break # difference too large
            options[i] += options[j]
    
    return options[-1]


if __name__ == "__main__":
    with open("input10.txt") as f:
        values = [*map(int, f.readlines())]
    
    diffs = diff_counts(values)
    print("Diffs in chain:", diffs, diffs[1] * diffs[3])
    print("Options for chain:", count_orders(values, 3))
