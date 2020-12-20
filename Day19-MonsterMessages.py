to_ints = lambda s: map(int, s.split())

def parse_rules(ruletext:str):
    rules = {}
    for line in ruletext.split("\n"):
        if not line: continue

        name, cont = line.strip().split(": ")
        n = int(name)

        if cont[0] == '"':
            # A letter rule
            rules[n] = cont[1]
        else:
            # Rule is a list of options, each option is a list of rules to
            # follow in sequence.
            rules[n] = [
                [int(c) for c in part.split()]
                for part in cont.split(" | ")
            ]

    return rules

def is_match(line, rules, target=0):
    """Check if a string matches the target rule in the dict of rules."""

    # Perform a depth-first search using a list as a stack
    # Each entry is a list of rules to match (in sequence) and the position
    # in the line that the first of these rules must match against.
    options = [([target], 0)]
    while options:
        to_match, pos = options.pop()

        # If we are at the end of the option, check that the entire
        # line has been consumed - if not, the option doesn't work
        if len(to_match) == 0:
            if pos == len(line):
                return True
            continue

        # Rule cannot use more characters than the line
        if pos >= len(line):
            continue

        rule = rules[to_match[0]]

        # The rule is a letter. Check if it matches the string at the 
        # current position.
        if isinstance(rule, str):
            if line[pos] == rule:
                options.append((to_match[1:], pos + 1))
            continue
        
        # The rule is a list of sub-rules, each of which is a list of
        # rule indices.  Replace the first entry of options with the contents
        # of the sub-rule
        for sub_rule in rule:
            # Each rule will use at least one character, so there is an easy
            # prune here.
            if len(sub_rule) < len(line) - pos:
                options.append((sub_rule + to_match[1:], pos))
    
    # There are no more possibilities
    return False   
            


if __name__ == '__main__':
    with open('input19.txt') as f:
        rule_block, message_block = f.read().split("\n\n")

    rules = parse_rules(rule_block)
    messages = message_block.strip().split("\n")

    print("Matching messages:", sum((is_match(m, rules) for m in messages)))
