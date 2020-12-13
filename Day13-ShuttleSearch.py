from math import ceil, lcm

def earliest_depart(now : int, bus : int) -> int:
    """Get the earliest departure time (after now) for a bus
    departing on a fixed schedule."""
    return int(ceil(now / bus)) * bus

def part1(now : int, busses : list[str]) -> int:
    """Get the minimum wait for a bus, multiplied by its id."""
    best = None
    for bus in busses:
        if bus == "x": continue

        wait = earliest_depart(now, int(bus)) - now
        if best is None or wait < best[0]:
            best = (wait, bus, wait * int(bus))
            print("New best:", best)
    
    return best[2]

def get_sequences(busses : list[str]) -> list[tuple[int, int]]:
    """Get the start and periods of the sequences of valid answers for each bus."""
    return [
        (int(x), int(x) - i)
        for i, x in enumerate(busses)
        if x != "x" 
    ]
    
def get_coincidence(period1:int, start1:int, period2:int, start2:int)->int:
    """Get the first coincidence of two sequences with given period and starts.
    period1 is assumed to be larger if of extremely different sizes."""
    val = start1
    while (val - start2) % period2:
        val += period1
    
    return val



def part2(busses : list[str]) -> int:
    """Get the first timestamp for departure of the first bus, such that each
    subsequent bus departs one minute later (x progresses the minute by one, 
    but is not a bus)."""

    seqs = get_sequences(busses)
    period1, start1 = seqs.pop()
    periods = [period1]

    while seqs:
        period2, start2 = seqs.pop()
        print(f"Looking for n*{period1}+{start1} = m*{period2}+{start2}")

        start1 = get_coincidence(period1, start1, period2, start2)
        periods.append(period2)
        period1 = lcm(*periods)

    return start1


if __name__ == "__main__":
    with open("input13.txt") as f:
        now = int(f.readline())
        busses = f.readline().strip().split(',')
    
    print(now)
    print(busses)

    print(f"Earliest departure score: {part1(now, busses)}")
    print(f"Earliest time: {part2(busses)}")
