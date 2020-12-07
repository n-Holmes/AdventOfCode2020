def get_summing_pair(target : int, elements : list[int]) -> int:
    check = set(elements)
    for x in elements:
        if target - x in elements:
            return x

def get_2020_2(elements : list[int]) -> int:
    x = get_summing_pair(2020, elements)
    return x * (2020 - x)

def get_2020_3(elements : list[int]) -> int:
    elements = sorted(elements)
    n = len(elements)
    target = 2020

    for i, first in enumerate(elements):
        j = i + 1 # left iterator
        k = n - 1 # right iterator
        if first * 3 >= target or j >= k:
            raise ValueError(f"No valid triple")

        new_target = target - first;

        while j < k:
            #print(f"{first}, {elements[j]}, {elements[k]}")
            p_sum = elements[j] + elements[k]
            if p_sum == new_target:
                print(f"Found: {first}, {elements[j]}, {elements[k]}.")
                return first * elements[j] * elements[k]
            elif p_sum < target:
                j += 1 # advance left iterator to increase value
            else:
                k -= 1 # advance right iterator to decrease value
        
        # We get here, first is invalid, try next

    raise ValueError("No valid triple (got to end)")


def get_2020_3a(elements : list[int]) -> int:
    for a in elements:
        for b in elements:
            if b == a: continue
            for c in elements:
                if c == a or c == b: continue

                if a + b + c == 2020:
                    print(a, b, c)
                    return a * b * c

if __name__ == "__main__":
    with open("input1.txt", "r") as f:
        entries = [int(l) for l in f.readlines()]
        print(sorted(entries))
        print(get_2020_3a(entries))
