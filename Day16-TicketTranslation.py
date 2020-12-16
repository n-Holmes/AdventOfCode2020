def parse_rules(rules_string : str) -> dict[str, set[int]]:
    rules = {}
    for line in rules_string.strip().split("\n"):
        name, regions = line.split(": ")
        rules[name] = set()
        for region in regions.split():
            if region and region != "or":
                start, end = region.split("-")
                rules[name].update(range(int(start), int(end) + 1))
    
    return rules

def parse_ticket(line : str) -> list[int]:
    return [
        int(x)
        for x in line.split(",")
        if x
    ]

def completely_invalid(tickets : list[list[int]], rules : dict[str,set[int]]):
    """Iteratively return all fields from any ticket which can never match a rule."""

    for ticket in tickets:
        for value in ticket:
            if all(value not in options for options in rules.values()):
                yield value

def valid_tickets(tickets, rules):
    """Iterate through all tickets with no completely invalid fields"""
    valid_set = set()
    for options in rules.values():
        valid_set.update(options)

    for ticket in tickets:
        if all(value in valid_set for value in ticket):
            yield ticket

def determine_rules(tickets, rules):
    """Given a list of valid tickets and their rules, determine which position
    each rule must be in."""
    positions = list(range(len(tickets[0]))) # the remaining positions to fill

    possible_positions = {
        rule : {
            i for i in positions
            if all(ticket[i] in options for ticket in tickets)
        }
        for rule, options in rules.items()
    }
    known_positions = {}

    while possible_positions:
        for rule, poss in possible_positions.items():
            if len(poss) == 1:
                break # only one option
        else:
            raise ValueError("Unable to assign the given rules to columns")
            
        pos = poss.pop()
        known_positions[rule] = pos
        possible_positions.pop(rule)
        for other in possible_positions.values():
            other.remove(pos)
        
    return known_positions


if __name__ == "__main__":
    with open("input16.txt") as f:
        sections = f.read().split("\n\n")
    
    rules = parse_rules(sections[0])
    our_ticket = parse_ticket(sections[1].split("\n")[1])
    tickets = [
        parse_ticket(line)
        for line in sections[2].strip().split("\n")[1:]
    ]

    print(len(rules), "rules parsed.")
    print(len(tickets), "tickets read")

    print("Total of invalid fields for all rules: ", sum(completely_invalid(tickets, rules)))

    tickets = list(valid_tickets(tickets, rules))
    print(len(tickets), "tickets remaining.")

    rule_locations = determine_rules(tickets, rules)
    total = 1
    for rule, pos in rule_locations.items():
        if rule.startswith("departure"):
            total *= our_ticket[pos]
    
    print(total)
