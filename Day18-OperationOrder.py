def parse(expr:str):
    # Seems that all numbers are 0-9, so nothing more complicated needed
    tokens = []
    path = [tokens]

    for char in expr:
        if char in " \n":
            continue
        if char == "(":
            path[-1].append([])
            path.append(path[-1][-1])
        elif char == ")":
            path.pop()
        else:
            try:
                path[-1].append(int(char))
            except ValueError:
                path[-1].append(char)

    return tokens

def evaluate(tokens) -> int:
    """Recursively evaluate a parsed list"""
    
    # base case
    if type(tokens) == int:
        return tokens
    
    val = evaluate(tokens[0])
    op = ""
    for i, tok in enumerate(tokens[1:], 1):
        if i % 2:
            op = tok
        else:
            other = evaluate(tok)
            val = eval(f"{val}{op}{other}")

    return val

def evaluate2(tokens) -> int:
    """Recursively eval an expr, giving + a higher priority than *"""

    # base case
    if type(tokens) == int:
        return tokens

    working = tokens[:]
    # Brackets first:
    for i, tok in enumerate(working):
        if type(tok) == type([]):
            working[i] = evaluate2(tok)
    
    # + next
    while "+" in working:
        i = working.index("+")
        working[i-1] = working[i-1] + working[i+1]
        working = working[:i] + working[i+2:]
    
    while "*" in working:
        i = working.index("*")
        working[i-1] = working[i-1] * working[i+1]
        working = working[:i] + working[i+2:]
    
    if len(working) > 1:
        raise ValueError("Unidentified tokens")

    return working[0]

if __name__ == '__main__':
    with open('input18.txt') as f:
        expressions = f.readlines()

    print(sum(evaluate(parse(ex)) for ex in expressions))
    print(sum(evaluate2(parse(ex)) for ex in expressions))
