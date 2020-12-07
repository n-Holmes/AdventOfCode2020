from collections import Counter
from functools import lru_cache

def get_contents(path : str) -> dict[str, dict[str, int]]:
    """Get a weighted, directed graph of bags.
    No protection for the case of cycles.
    """
    with open(path, "r") as f:
        lines = f.readlines();
    
    contents = {}

    # Could use regex here, but hardly seems necessary due to the input size.
    for line in lines:
        try:
            bag, contains = line.split(" bags contain ");
        except:
            continue

        contents[bag] = Counter()
        if contains.startswith("no"): continue

        # separate types
        for item in contains.split(", "):
            parts = item.split();
            color = parts[1] + " " + parts[2]
            count = int(parts[0])
            contents[bag][color] = count
    
    return contents

def get_poss_containers(
    target : str,
    contents : dict[str, dict[str, int]]
    ) -> list[str]:
    """Returns a list of all bags which can contain a bag of a given color."""

    to_check = [target]
    valid = set()
    while to_check:
        target_color = to_check.pop()

        for cont_color in contents:
            if cont_color not in valid and target_color in contents[cont_color]:
                valid.add(cont_color)
                to_check.append(cont_color)
    
    return list(valid)
                
def count_contents(
    target : str,
    contents : dict[str, dict[str, int]]
    ) -> int:
    """Counts the number of bags contained within a given color of bag."""

    @lru_cache() # Cache results to speed up recursion
    def rec_count(color : str) -> int:
        """Recursively count the contents of a given color."""
        return sum(
            (1 + rec_count(child)) * count
            for child, count in contents[color].items()
        )

    return rec_count(target)


if __name__ == "__main__":
    graph = get_contents("input7.txt")

    print("Containers that can hold a shiny gold bag:")
    print(len(get_poss_containers("shiny gold", graph)))

    print("No of bags in a shiny gold:")
    print(count_contents("shiny gold", graph))
