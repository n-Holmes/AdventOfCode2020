from functools import lru_cache
from time import time, sleep
from collections import deque

def play(p1:list[int], p2:list[int]) -> list[int]:
    """Gets the final hand of the winning player"""

    while p1 and p2:
        a = p1.pop(0)
        b = p2.pop(0)
        if a > b:
            p1 += [a, b]
        else:
            p2 += [b, a]
    
    return p1 + p2
            
def score(deck:list[int]) -> int:
    """Get the score for a deck"""
    return sum(i * card for i, card in enumerate(reversed(deck), 1))

def play_recursive(p1, p2):
    """Get the winning deck of the recursive combat game."""
    states_seen = set() # List of all states seen. If repeaded p1 wins

    while p1 and p2:
        # Check for duplicate play state
        state = str(p1) + str(p2)
        if state in states_seen:
            return 1, p1
        states_seen.add(state)

        a = p1.pop(0)
        b = p2.pop(0)
        if a > len(p1) or b > len(p2):
            # A player does not have enough cards to recurse, high wins
            winner = 1 if a > b else 2
        
        else:
            # had misread the problem and been using p1[:], p2[:] here
            # that makes it run for hours
            winner, _ = play_recursive(p1[:a], p2[:b])
        
        if winner == 1:
            p1 += [a,b]
        else:
            p2 += [b,a]
    
    return (1, p1) if p1 else (2, p2)



if __name__ == '__main__':
    players = []
    with open('input22.txt') as f:
        for section in f.read().split("\n\n"):
            players.append(list(map(int, section.strip().split("\n")[1:])))

    # winner = play(players[0][:], players[1][:])
    # print(winner)
    # print(score(winner))

    winner, hand = play_recursive(*players)
    print(hand)
    print(score(hand))
