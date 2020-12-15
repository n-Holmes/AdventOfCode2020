from collections import defaultdict
from time import time

class SequenceMaker:
    def __init__(self, input:list[int]):
        self.last_seen = defaultdict(int)
        self.next_play = 0
        self.turns_played = 0
        self.sequence = []

        for val in input:
            self.next_play = self.play_turn(val)

    def play_turn(self, value:int) -> int:
        """Plays a given value and returns the next value to play."""
        self.turns_played += 1
        valueLastSeen = self.last_seen[value]
        self.last_seen[value] = self.turns_played

        return self.turns_played - valueLastSeen if valueLastSeen else 0

    def get_turn(self, turn:int) -> int:
        """Get the value played on a given turn"""
        
        while self.turns_played < turn - 1:
            self.next_play = self.play_turn(self.next_play)
        
        return self.next_play


if __name__ == "__main__":
    with open("input15.txt") as f:
        start_vals = list(map(int, f.read().strip().split(",")))

    seq = SequenceMaker(start_vals)
    start = time()
    print(f"Turn 2020: {seq.get_turn(2020)} (took {time() - start})")
    start = time()
    print(f"Turn 30mil: {seq.get_turn(30000000)}. (took {time() - start})")
