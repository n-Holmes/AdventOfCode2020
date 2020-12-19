from collections import Counter

def neighbours(pos):
    i, j, k = pos
    for di in range(-1, 2):
        for dj in range(-1, 2):
            for dk in range(-1, 2):
                if any((di, dj, dk)): # Don't allow all to be zero
                    yield(i + di, j + dj, k + dk)

class ConwayCubes:
    def __init__(self, seed : list[str]):
        self.active = set() # set of all active cubes as 3d coords

        for i, line in enumerate(seed):
            for j, char in enumerate(line):
                if char == "#":
                    self.active.add((i,j,0))

    def step(self):
        counts = Counter()
        for cube in self.active:
            for nbr in neighbours(cube):
                counts[nbr] += 1
        
        self.active = {
            pos for pos in counts
            if counts[pos] == 3 or (counts[pos] == 2 and pos in self.active)
        }

def neighbours4(pos):
    i, j, k, l = pos
    for di in range(-1, 2):
        for dj in range(-1, 2):
            for dk in range(-1, 2):
                for dl in range(-1, 2):
                    if any((di, dj, dk, dl)): # Don't allow all to be zero
                        yield(i + di, j + dj, k + dk, l + dl)

class ConwayCubes4:
    def __init__(self, seed : list[str]):
        self.active = set() # set of all active cubes as 3d coords

        for i, line in enumerate(seed):
            for j, char in enumerate(line):
                if char == "#":
                    self.active.add((i,j,0,0))

    def step(self):
        counts = Counter()
        for cube in self.active:
            for nbr in neighbours4(cube):
                counts[nbr] += 1
        
        self.active = {
            pos for pos in counts
            if counts[pos] == 3 or (counts[pos] == 2 and pos in self.active)
        }

if __name__ == "__main__":
    with open("input17.txt") as f:
        lines = f.readlines()

    cubes = ConwayCubes(lines)
    for _ in range(6):
        cubes.step()
    print(len(cubes.active))

    hycubes = ConwayCubes4(lines)
    for _ in range(6):
        hycubes.step()
    print(len(hycubes.active))
