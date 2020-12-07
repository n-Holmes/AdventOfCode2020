import re

def get_policy(line : str) -> tuple[int, int, str, str]:
    match = re.match(r"(\d+)-(\d+) (.): (.*)", line)
    return (
        int(match.groups()[0]),
        int(match.groups()[1]),
        match.groups()[2],
        match.groups()[3]
    )

def count_valid(lines : list[str]) -> int:
    count = 0
    for line in lines:
        if line:
            low, high, char, password = get_policy(line)
            count += low <= password.count(char) <= high
    
    return count

def count_valid_2(lines : list[str]) -> int:
    count = 0
    for line in lines:
        if line:
            first, second, char, password = get_policy(line)
            count += (
                (first <= len(password) and password[first-1] == char) !=
                (second <= len(password) and password[second-1] == char)
            )
                
    
    return count


if __name__ == "__main__":
    with open("input2.txt", "r") as f:
        lines = f.readlines()
    
    print(f"Valid passwords (low-high): {count_valid(lines)}")
    print(f"Valid passwords (position): {count_valid_2(lines)}")
