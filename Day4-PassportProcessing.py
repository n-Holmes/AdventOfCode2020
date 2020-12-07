

def get_passports(contents : str) -> list[dict[str, str]]:
    """Extracts passport details from a string"""
    for part in contents.split("\n\n"):
        # empty part
        if not part.strip():
            continue
        
        passport = dict(field.split(":") for field in part.split())
        yield passport

def count_valid(passports : list[dict[str, str]], fields : list[str]) -> int:
    """Counts the passports that have the right fields"""
    return sum(
        all(field in passport for field in fields)
        for passport in passports
    )

def is_valid(passport : dict[str, str]) -> bool:
    """Strict check of password validity."""

    try:
        return all((
            len(passport["byr"]) == 4,
            1920 <= int(passport["byr"]) <= 2002,

            len(passport["iyr"]) == 4,
            2010 <= int(passport["iyr"]) <= 2020,

            len(passport["eyr"]) == 4,
            2020 <= int(passport["eyr"]) <= 2030,

            (
                len(passport["hgt"]) == 5 and
                passport["hgt"][3:] == "cm" and
                150 <= int(passport["hgt"][:3]) <= 193
            ) or (
                len(passport["hgt"]) == 4 and
                passport["hgt"][2:] == "in" and
                59 <= int(passport["hgt"][:2]) <= 76
            ),

            len(passport["hcl"]) == 7,
            passport["hcl"][0] == "#",
            int(passport["hcl"][1:], 16) >= 0, # failure will be an exception

            passport["ecl"] in "amb blu brn gry grn hzl oth".split(),

            len(passport["pid"]) == 9,
            int(passport["pid"]) >= 0, # failure will be an exception

            #ignore cid
        ))

    except:
        # There was a missing field, or a field was not convertable
        return False    


def count_valid_strict(passports : list[dict[str, str]]) -> int:
    """Counts the number of actually valid passports"""
    return sum(
        is_valid(passport)
        for passport in passports
    )

if __name__ == "__main__":
    with open("input4.txt", "r") as f:
        passports = list(get_passports(f.read()))

    mandatory = "byr iyr eyr hgt hcl ecl pid".split()

    print("Passports:", len(passports))
    print("Valid:", count_valid(passports, mandatory))
    print("Strictly valid:", count_valid_strict(passports))
