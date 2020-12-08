class accumulator:
    """Wrapper for a value"""
    def __init__(self):
        self.value = 0

def parse_code(lines : list[str]) -> list[tuple[str, int]]:
    """Turns the input into instructions"""
    code = []
    for line in lines:
        instr, val = line.strip().split()
        code.append((instr, int(val)))

    return code

def execute_line(
    instr : tuple[str, int], # The instruction to execute
    pos : int,               # The current position in code   
    acc=None                 # The accumulator
) -> int:
    """Executes an instruction and returns the position of the next instruction"""
    
    if (instr[0] == "jmp"):
        return pos + instr[1]

    if (instr[0] == "acc"):
        if acc:
            acc.value += instr[1]
    elif (instr[0] != "nop"):
        raise ValueError(f"Unknown instruction: {instr}")

    return pos + 1

def execute_until_loop(code : list[tuple[str, int]]) -> tuple[int, bool]:
    """Find the value of the accumulator at the first repeat instruction.
    Returns the value of the accumulator and whether the code looped.
    """
    acc = accumulator()
    ptr = 0
    seen = set()

    while ptr not in seen and 0 <= ptr < len(code):
        seen.add(ptr)
        ptr = execute_line(code[ptr], ptr, acc)
    
    return acc.value, 0 <= ptr < len(code)

def get_change_set(code : list[tuple[str, int]]) -> tuple[set[int], set[int]]:
    """Return the sets of all jmp and nop instructions executed."""
    ptr = 0
    seen = set()

    while ptr not in seen and 0 <= ptr < len(code):
        seen.add(ptr)
        ptr = execute_line(code[ptr], ptr)
    
    return ({i for i in seen if code[i][0] == "jmp"},
            {i for i in seen if code[i][0] == "nop"})

def get_fixed_acc_val(code : list[tuple[str, int]]) -> int:
    """Fixes the code and returns the accumulator value on exit
    (brute force)
    """
    jmps, nops = get_change_set(code)

    for i in jmps:
        new_code = code[:]
        new_code[i] = ("nop", code[i][1])
        acc, res = execute_until_loop(new_code)
        if not res:
            print(f'Changed line {i} to nop {code[i][1]}')
            return acc

    for i in nops:
        new_code = code[:]
        new_code[i] = ("jmp", code[i][1])
        acc, res = execute_until_loop(new_code)
        if not res:
            print(f'Changed line {i} to jmp {code[i][1]}')
            return acc

    print("no fix found!")
    return -1


if __name__ == "__main__":
    with open("input8.txt") as f:
        code = parse_code(f.readlines())

    print("Acc value at first loop:", execute_until_loop(code)[0])

    print("Acc value on exit after fix:", get_fixed_acc_val(code))
