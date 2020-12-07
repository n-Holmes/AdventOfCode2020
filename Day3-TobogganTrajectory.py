def count_trees(grid : list[list[int]], velocity : tuple[int, int]) -> int:
    width = len(grid[0])

    count = 0
    j = 0
    for row in grid[::velocity[0]][1:]:
        j += velocity[1]
        count += row[j % width]

    return count


if __name__ == "__main__":
    with open("input3.txt", "r") as f:
        lines = f.readlines()
    
    grid = [
        [c == "#" for c in line.strip()]
        for line in lines
    ]

    print("Number of trees hit (1, 3):", count_trees(grid, (1, 3)))

    total = 1
    for slope in (
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)
    ):
        total *= count_trees(grid, slope)
    
    print(total)
