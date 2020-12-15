class Memory:
    """Represents the state of the 36-entry memory and actions upon it"""
    def __init__(self):
        self._storage = {}
        self._neg_mask = (1 << 36) - 1 # Any bit set to 0 here will always be 0
        self._pos_mask = 0             # Any bit set to 1 here will always be 1
    
    def set_mask(self, mask:str):
        self._neg_mask = (1 << 36) - 1 # 36 set bits
        self._pos_mask = 0

        bit = 1 << 35
        for char in mask:
            if char == "1":
                self._pos_mask += bit # set bit
            elif char == "0":
                self._neg_mask -= bit # unset bit
            
            bit >>= 1
    
    def store(self, location:int, value:int):
        if not 0 <= location < 2 ** 36:
            raise IndexError(f"{location} is not a valid memory address")

        self._storage[location] = (value & self._neg_mask) | self._pos_mask
    
    def print(self):
        for i, val in self._storage.items():
            print(f"[{i}]: {val}")
    
    @property
    def state(self) -> dict[int, int]:
        return self._storage.copy()

class AddressMaskMemory(Memory):
    """Represents the state of the 36-entry memory and actions upon it.
    Mask is applied to address, rather than value."""
    def __init__(self):
        super().__init__()
        self._float_bits = [] # indices of floating pits

    def set_mask(self, mask:str):
        super().set_mask(mask)
        self._float_bits = [i for i, val in enumerate(mask[::-1]) if val == "X"]
    
    def store(self, location:int, value:int):
        if not 0 <= location < 2 ** 36:
            raise IndexError(f"{location} is not a valid memory address")

        # iterate over all combinations of the floating bits
        for combination in range(2 ** len(self._float_bits)):
            target = location | self._pos_mask # the actual location to store in
            # The inclusion values of the combination
            float_vals = {
                pos : bool(combination & (1 << i))
                for i, pos in enumerate(self._float_bits)
            }
            
            for loc, positive in float_vals.items():
                if (positive):
                    target |= 1 << loc
                else:
                    target &= (1 << 36) - 1 - (1 << loc)
        
            self._storage[target] = value

def execute(instructions : list[str], mem : Memory) -> int:
    """Carry out the series of instructions on the given memory.
    Return the sum of all values stored in the memory at the end."""
    for line in instructions:
        inst, val = line.strip().split(" = ")
        if inst == "mask":
            mem.set_mask(val)
        else:
            location = int(inst[4:-1])
            mem.store(location, int(val))
    
    # mem.print()
    return sum(mem.state.values())

if __name__ == "__main__":
    with open("input14.txt") as f:
        lines = f.readlines()
    
    print(f"Sum of all values in storage: {execute(lines, Memory())}")
    print(f"With address masking: {execute(lines, AddressMaskMemory())}")
