from time import time

 
class CupsGame:
    """The game of crab cups"""

    def __init__(self, order:str, size:int=9):
        self.size = size # number of cups

        # Store the next cup in order for each cup (0 index is dud)
        self.targets = [i + 1 for i in range(size + 1)]

        order = list(map(int, order))
        self.current = order[0] # The current cup
        for i, j in zip(order, order[1:]):
            self.targets[i] = j

        if size > 9:
            self.targets[j] = 10
            self.targets[size] = order[0]
        else:
            self.targets[j] = order[0]

    def play_turn(self):
        # Which cups are moving?
        moving = []
        active = self.current
        for _ in range(3):
            active = self.targets[active]
            moving.append(active)
        
        # close the circle
        self.targets[self.current] = self.targets[active]

        # find where to put the stuff
        insert = self.current - 1
        if insert == 0:
            insert = self.size
        while insert in moving:
            insert -= 1
            if insert == 0:
                insert = self.size

        # splice the section into the circle
        self.targets[moving[-1]] = self.targets[insert]
        self.targets[insert] = moving[0]

        # progress the current cup
        self.current = self.targets[self.current] 
    
    def play(self, count:int):
        for i in range(count):
            self.play_turn()
            if i and i % 100000 == 0:
                print(f"{i} turns played")

    def __str__(self):
        values = []
        cursor = 1
        for _ in range(8):
            values.append(cursor)
            cursor = self.targets[cursor]

        return "Crab Cups: " + ",".join(map(str, values)) + ",..."


if __name__ == '__main__':
    with open('input23.txt') as f:
        sequence = f.read().strip()

    game = CupsGame(sequence)
    print(game)
    game.play(100)
    print(game)

    start = time()
    game = CupsGame(sequence, 1000000)
    game.play(10000000)
    print(game)
    print(time() - start)
