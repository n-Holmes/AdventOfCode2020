from typing import Iterable, Callable, Any, Iterator
from collections import Counter

def parse_line(line:str) -> list[int]:
    """Take a line of joined directions and turn into a list of directions.
    0 = East, 1 = North-East, ..."""
    line = line.strip()

    directions = {"ne":"1", "nw":"2", "sw":"4", "se":"5", "e":"0", "w":"3"}
    for pattern, direction in directions.items():
        line = line.replace(pattern, direction)
    
    return list(map(int, line))

def get_target(directions:list[int]) -> tuple[int, int]:
    """Gets the coordinates of the target following directions.
    x axis runs E, y runs NE"""
    x = y = 0

    for direction in directions:
        if direction == 0:
            x += 1
        elif direction == 1:
            y += 1
        elif direction == 2:
            x -= 1
            y += 1
        elif direction == 3:
            x -= 1
        elif direction == 4:
            y -= 1
        elif direction == 5:
            x += 1
            y -= 1
    
    return x, y

class Life:
    """A generic game of life implementation.
    Can be parameterized for any game where life
     * only depends on direct neighbors
     * is rotation/reflection invariant
     * all living cells after step had at least one live neighbor
    """
    def __init__(self,
        seed:Iterable[Any],                        # Starting live tiles
        adj_func:Callable[[Any], Iterable[Any]],   # Function to determine adjacent tiles
        life_condition:Callable[[bool, int], bool] # Function to decide on life state
    ):
        self.alive = set(seed)
        self.adj_func = adj_func
        self.life_condition = life_condition

    def step(self):
        """Advance the game one step."""
        live_neighbors = Counter()
        for pos in self.alive:
            for adj in self.adj_func(pos):
                live_neighbors[adj] += 1
        
        self.alive = {
            pos for pos, count in live_neighbors.items()
            if self.life_condition(pos in self.alive, count)
        }

    def play(self, n:int):
        """Advance the game n steps."""
        for _ in range(n):
            self.step()

def hex_adj(pos:tuple[int, int]) -> Iterator[tuple[int, int]]:
    """Given a hex coordinate, return all adjacent ones"""
    x, y = pos
    yield x+1, y
    yield x,   y+1
    yield x-1, y+1
    yield x-1, y
    yield x,   y-1
    yield x+1, y-1

def hex_life(is_alive:bool, live_neighbors:int) -> bool:
    """Work out the life status of a tile, given its current status and neighbors"""
    if is_alive:
        return live_neighbors in (1,2)
    else:
        return live_neighbors == 2

if __name__ == '__main__':
    with open('input24.txt') as f:
        lines = f.readlines()
    
    tiles = set()
    for line in lines:
        pos = get_target(parse_line(line))
        if pos in tiles:
            tiles.remove(pos)
        else:
            tiles.add(pos)
    print("Black tiles to start:", len(tiles))

    game = Life(tiles, hex_adj, hex_life)
    game.play(100)
    print("Black tiles after play:", len(game.alive))
