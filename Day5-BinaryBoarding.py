def decode_pass(boarding_pass : str) -> tuple[int, int, int]:
    """Get the row, column and seat id from a boarding pass"""

    row = int(boarding_pass[:7].replace("F", "0").replace("B", "1"), 2)
    column = int(boarding_pass[7:].replace("L", "0").replace("R", "1"), 2)

    return row, column, row * 8 + column

if __name__ == "__main__":
    with open("input5.txt", "r") as f:
        passes = f.readlines()

    seats = [seat for row, col, seat in map(decode_pass, passes)]

    print("Highest seat id:")
    print(max(seats))

    print("Missing seat:")
    seats = sorted(seats)
    for i, seat in enumerate(seats, seats[0]):
        if i != seat:
            print(i)
            break
