from functools import lru_cache
from math import sqrt
from time import time

@lru_cache()
def line_value(line):
    """Return the value associated with a line (series of # and . chars)"""
    val = 0
    for char in line:
        val <<= 1
        val += char == "#"
    return val

@lru_cache()
def complement(value):
    """Gets the matching (reversed) value of a line."""
    comp = 0
    for _ in range(10):
        comp <<= 1
        comp += value & 1
        value >>= 1
    return comp

class Tile:
    """Represents a jigsaw tile."""
    def __init__(self, text=None, id=None, edges=None):
        if text is not None:
            lines = text.strip().split("\n")
            self.id = int(lines[0][5:-1])
            grid = lines[1:]

            self.edges = [
                line_value(grid[0]),
                line_value(l[-1] for l in grid),
                line_value(reversed(grid[-1])),
                line_value(l[0] for l in reversed(grid))            
            ]
        else:
            self.id = id
            self.edges = [*edges]
    
    def transform(self, rotations=0, reflect=False):
        """Get a new tile which is a transformation of the old one.
        rotations: number of rotations counter-clockwise by 90 deg (0-4)
        reflect: whether to reflect in the major diagonal (prior to rotation)
        """
        new_edges = self.edges[:]
        if reflect:
            new_edges = [*map(complement, reversed(new_edges))]
        
        if rotations:
            # 1 = 90 deg CCW
            rotations = rotations % 4 # just in case
            new_edges = new_edges[rotations:] + new_edges[:rotations]

        return Tile(id=self.id, edges=new_edges)

    # Collection of all possible transformations, for easier iteration.
    Transformations = (
        (0, False), (1, False), (2, False), (3, False),
        (0, True), (1, True), (2, True), (3, True),
    )

    @property
    def Top(self):
        return self.edges[0]
    @property
    def Right(self):
        return self.edges[1]
    @property
    def Bottom(self):
        return self.edges[2]
    @property
    def Left(self):
        return self.edges[3]

class Grid:
    """Represents a grid to place the tiles in."""
    def __init__(self, tiles):
        self.dim = int(sqrt(len(tiles))) # The dimension of the (square) grid
        self.grid = [
            [None] * self.dim
            for _ in range(self.dim)
        ] # The contents of the grid
        self.tx_grid = [
            [None] * self.dim
            for _ in range(self.dim)
        ] # The transformations for each tile in the grid

        self.tileset = list(tiles) # The list of tiles available for the whole grid
        self.used = set() # The set of ids of tiles currently in use

        self.active_tile = 0 # The lowest numbered tile yet to be filled

    def arrange(self):
        """Try to slot a tile into the first currently empty slot
        For each valid tile call arrange recursively.
        If no valid tiles return False.
        If full solution to the end of the grid found return True.        
        """
        if self.active_tile == len(self.tileset):
            # We've reached the end - full solution found
            return True
        
        i = self.active_tile // self.dim
        j = self.active_tile % self.dim

        # Treat the first tile slightly differently - no need for reflections
        # Cannot be one of the last three tiles
        if self.active_tile == 0:
            self.active_tile = 1
            for tile in self.tileset[:-3]:
                self.used.add(tile.id)
                for tx in Tile.Transformations[:4]: # no reflections for first tile
                    self.grid[0][0] = tile.transform(*tx)
                    self.tx_grid[0][0] = tx
                    # print(f"Tile {tile.id} placed in slot {i},{j}. {tx}")
                    if self.arrange(): return True
                self.used.remove(tile.id) # wasn't the right one
            return False # not able to find any match

        else:
            # Get the boundary conditions on the space
            # up_edge is the required value for edges[0], l_edge for [3]
            up_edge = complement(self.grid[i-1][j].Bottom) if i > 0 else None
            l_edge  = complement(self.grid[i][j-1].Right) if j > 0 else None
            for tile in self.tileset:
                if tile.id in self.used: continue # tile already in use
                
                # Check that the correct values at least exist in the edge sets
                # necessary but not sufficient for the tile being an option
                can_be_unflipped = (
                    (up_edge is None or up_edge in tile.edges) and
                    (l_edge is None or l_edge in tile.edges)
                )
                can_be_flipped = (
                    (up_edge is None or complement(up_edge) in tile.edges) and
                    (l_edge is None or complement(l_edge) in tile.edges)
                )
                if not (can_be_flipped or can_be_unflipped): continue

                # print(f"Trying tile {tile.id} in slot {i},{j}")
                for tx in Tile.Transformations:
                    # We already know some transforms will fail
                    if tx[1]:
                        if not can_be_flipped: continue
                    else:
                        if not can_be_unflipped: continue

                    tx_tile = tile.transform(*tx) # The tile, transformed
                    if (up_edge and up_edge != tx_tile.Top) or \
                       (l_edge and l_edge != tx_tile.Left):
                        continue # not valid in this orientation

                    # Progress!!!
                    self.grid[i][j] = tx_tile
                    self.tx_grid[i][j] = tx
                    self.active_tile += 1
                    self.used.add(tile.id)
                    # print(f"Tile {tile.id} placed in slot {i},{j}. {tx}")
                    if self.arrange():
                        return True
                    self.active_tile -= 1
                    self.used.remove(tile.id) # this tile doesn't fit here

            self.grid[i][j] = None
            self.tx_grid[i][j] = None
            return False # not able to find any match for this position

    def print(self):
        for line in self.grid:
            print([(tile.id if tile else None) for tile in line])
    
    @property
    def value(self):
        if self.active_tile != len(self.tileset):
            return -1
        return (
            self.grid[0][0].id  * self.grid[0][-1].id  *
            self.grid[-1][0].id * self.grid[-1][-1].id
        )

class ImageTile:
    """Represents a the 8x8 image on a tile."""
    def __init__(self, text):
        lines = text.strip().split("\n")
        self.id = int(lines[0][5:-1])

        # Strip the image of its borders
        self.grid = [
            [1 if c == "#" else 0 for c in line.strip()[1:-1]]
            for line in lines[2:-1]
        ]

    def row(self, row):
        """Returns the contents of a given row of the (borderless) image"""
        if row < 0 or row > 7:
            raise ValueError(f"Invalid row: {row}")
        return self.grid[row][:]

    def transform(self, rotations, reflected):
        """Transform the contents of the tile (reflect first)"""
        if reflected:
            self.grid = [list(col) for col in zip(*self.grid)]
        
        for _ in range(rotations):
            new_grid = [[0] * 8 for _ in range(8)]
            for i in range(8):
                for j in range(8):
                    new_grid[i][j] = self.grid[j][7-i]
            self.grid = new_grid

class Monster:
    """Represents the monster to find within an image"""
    def __init__(self):
        self.tiles = set()
        self.height = self.width = 0

    @staticmethod
    def from_pattern(pattern:list[str]):
        """Monster is assumed to be a rectangular image of "#" and " " chars."""
        mon = Monster()
        mon.tiles = {
            (i, j)
            for i, row in enumerate(pattern)
            for j, char in enumerate(row)
            if char == "#"
        }

        mon.height = len(pattern)
        mon.width = len(pattern[0])
        return mon
    
    @staticmethod
    def from_tiles(tiles:set[tuple[int, int]], width:int, height:int):
        """Get a new monster with the given details"""
        mon = Monster()
        mon.tiles = tiles
        mon.width = width
        mon.height = height
        return mon
    
    def transform(self, rotations:int, reflected:bool):
        """Get a new monster which is a transformation of this one."""
        new_width = self.width
        new_height = self.height

        new_tiles = self.tiles.copy() # in case the transformation is identity
        if reflected:
            new_tiles = {
                (j, i) for i, j in new_tiles
            }
            new_width, new_height = new_height, new_width
        
        for _ in range(rotations):
            new_tiles = {
                (new_width - 1 - j, i) for i, j in new_tiles
            }
            new_width, new_height = new_height, new_width
        
        return Monster.from_tiles(new_tiles, new_width, new_height)

class Image:
    """Represents an image made from image tiles"""

    def __init__(self, grid:Grid, image_tiles:dict[ImageTile]):
        if grid.value == -1:
            raise ValueError("A solved grid is needed")

        self.dim = 8 * grid.dim
        self.contents = [
            [0] * self.dim
            for _ in range(self.dim)
        ]

        for i in range(grid.dim):
            for j in range(grid.dim):
                tile = image_tiles[grid.grid[i][j].id]
                tile.transform(*grid.tx_grid[i][j])
                self.insert(tile, i*8, j*8)

    def insert(self, tile:ImageTile, row:int, col:int):
        """Insert the contents of an image tile into the grid at the given
        coordinates."""
        for i in range(8):
            self.contents[row+i][col:col+8] = tile.row(i)

    def print(self, black="#", white="."):
        for line in self.contents:
            printline = (black if c else white for c in line)
            print("".join(printline))

    def find_monsters(self, pattern:list[str]):
        first = Monster.from_pattern(pattern)
        monsters = [first.transform(*tx) for tx in Tile.Transformations]
        monster_tiles = set()
        found = 0
        for monster in monsters:
            for top in range(self.dim + 1 - monster.height):
                for left in range(self.dim + 1 - monster.width):
                    if all(
                        self.contents[top + i][left + j] == 1
                        for i, j in monster.tiles
                    ):
                        print(f"found a monster at {top},{left}")
                        found += 1
                        for i, j in monster.tiles:
                            monster_tiles.add((top + i, left + j))
        
        print(f"Found {found} monsters in total, occupying {len(monster_tiles)} tiles.")
        choppy_tiles = sum(map(sum, self.contents)) - len(monster_tiles)
        print(f"There are {choppy_tiles} choppy tiles remaining.")
        
if __name__ == '__main__':
    with open('input20.txt') as f:
        tile_chunks = f.read().split("\n\n")
    
    start = time()
    tiles = [Tile(chunk) for chunk in tile_chunks]
    grid = Grid(tiles)
    grid.arrange()
    grid.print()
    print("Product of corners: ", grid.value, "\n")
    print("Part 1 took", time() - start)

    start = time()
    image_tiles = {}
    for chunk in tile_chunks:
        tile = ImageTile(chunk)
        image_tiles[tile.id] = tile

    image = Image(grid, image_tiles)
    image.find_monsters([
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ])
    print("Part 2 took", time() - start)
