from copy import deepcopy
from typing import Union

### Part 1 ###
def make_board(lines : list[list[str]]) -> list[list[Union[bool, None]]]:
    """Map values to True, False or None for easier logic"""
    values = {"L": False, "#": True, ".": None}
    return [[values[c] for c in l.strip()] for l in lines]

def print_board(board):
    """Pretty-print function for the board"""
    values = {False: "L", True: "#", None: "."}
    for line in board:
        print("".join(values[v] for v in line))
    print()

def step(board):
    """Step function, iterates the board based on its neighbors and
    returns the new board and whether any change was made.
    """

    new_board = deepcopy(board)
    n, m = len(new_board), len(new_board[0])

    def adjacent(i, j):
        """Lists adjacent positions"""
        for a in range(-1, +2):
            if i + a < 0 or i + a >= n:
                continue
            for b in range(-1, +2):
                if 0 <= j + b < m and (a or b):
                    yield board[i + a][j + b]

    any_change = False
    for i, line in enumerate(new_board):
        for j, val in enumerate(line):
            if val is None:
                continue
            occupied_seen = sum(bool(s) for s in adjacent(i, j))
            if val:
                if occupied_seen >= 4:
                    new_board[i][j] = False
                    any_change = True
            elif occupied_seen == 0:
                new_board[i][j] = True
                any_change = True
    
    return new_board, any_change

def iterate_to_halt(board, step_func):
    """Step the board until no seats change."""
    i = 0
    while True:
        new_board, changed = step_func(board)

        if not changed:
            print(f"Stopped after {i} iterations")
            return new_board

        board = new_board
        i += 1


### Part 2 ###
def adj_list(board):
    """Gets the adjacency list of a board"""
    seats = {}
    n, m = len(board), len(board[0])
    def seen(i, j):
        """Iterate through the list of visible seats"""
        for di, dj in (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ):
            a, b = i, j
            while True:
                a += di
                b += dj
                if a < 0 or a >= n or b < 0 or b >= m:
                    break # Left the board
                
                if board[a][b] is not None:
                    # Found a seat
                    yield (a, b)
                    break
    
    for i, line in enumerate(board):
        for j, val in enumerate(line):
            if val is not None:
                seats[i,j] = list(seen(i, j))
    
    return seats

def make_step(adj_list):
    """Make a step function from an adjacency list"""
    def step_sight(board):
        new_board = deepcopy(board)
        any_change = False
        for x, y in adj_list:
            occupied_seen = sum(board[i][j] for i, j in adj_list[(x, y)])
            #print(x, y, board[x][y], occupied_seen)
            if board[x][y]:
                if occupied_seen >= 5:
                    new_board[x][y] = False
                    any_change = True
            elif occupied_seen == 0:
                new_board[x][y] = True
                any_change = True
        
        return new_board, any_change
    return step_sight
    

if __name__ == "__main__":
    with open("input11.txt") as f:
        board = make_board(f.readlines())

    print("Iterating to no change...")
    static = iterate_to_halt(board, step)
    seats = sum(sum(map(bool, line)) for line in static)
    print("Seats occupied:", seats)

    seats_seen = adj_list(board)
    step_func = make_step(seats_seen)
    print("Iterating to no change...")
    static = iterate_to_halt(board, step_func)
    seats = sum(sum(map(bool, line)) for line in static)
    print("Seats occupied:", seats)
