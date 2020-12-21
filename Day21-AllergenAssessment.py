import re
from collections import defaultdict
from typing import Iterator

def parse_food(line:str) -> tuple[list[str], list[str]]:
    """Get the lists of ingredients and allergens from a food description"""
    ingredients = []
    allergens = []

    containsFound = False
    for word in re.findall("\w+", line):
        if word == "contains":
            containsFound = True
        elif containsFound:
            allergens.append(word)
        else:
            ingredients.append(word)
    
    return ingredients, allergens

def get_occurences(foods:list[tuple[list[str], list[str]]]) \
    -> tuple[dict[str, set[int]], dict[str, set[int]]]:
    """Get dictionaries giving the occurences of each allergen and ingredient"""
    algn_occur = defaultdict(set)
    ingr_occur = defaultdict(set)

    for i, (ingredients, allergens) in enumerate(foods):
        for allergen in allergens:
            algn_occur[allergen].add(i)
        for ingredient in ingredients:
            ingr_occur[ingredient].add(i)

    return algn_occur, ingr_occur

def get_nonallergenic(foods:list[tuple[list[str], list[str]]]) -> Iterator[str]:
    """Get a collection of all foods which cannot be the source of a listed allergen.
    Relies on the assumption that each listed allergen comes from precisely
    one ingredient."""

    allergens, ingredients = get_occurences(foods)

    for ing, ing_set in ingredients.items():
        for alg_set in allergens.values():
            if alg_set.issubset(ing_set):
                break
        else:
            yield ing # ing cannot represent any of the allergens

def count_occurences(
    foods:list[tuple[list[str],list[str]]],
    ingredient:str
) -> int:
    """Count how many times a given ingredient occurs in all foods"""
    return sum(ingredient in ingredients for ingredients, _ in foods)

def identify_allergens(foods:list[tuple[list[str],list[str]]]) -> dict[str,str]:
    allergens, ingredients = get_occurences(foods)

    possibilities = defaultdict(set)
    for allergen, alg_set in allergens.items():
        for ingredient, ing_set in ingredients.items():
            if alg_set.issubset(ing_set):
                possibilities[allergen].add(ingredient)

    certainties = {}
    while possibilities:
        for alg, poss in possibilities.items():
            if len(poss) == 1:
                break
        else:
            raise ValueError("Not able to identify all allergens")
        possibilities.pop(alg)
        
        # Found an ingredient match - remove from all other allergens
        ingredient = poss.pop()
        certainties[alg] = ingredient
        for alg in possibilities:
            possibilities[alg] -= {ingredient}
    
    return certainties



if __name__ == '__main__':
    with open('input21.txt') as f:
        foods = [parse_food(l) for l in f.readlines()]

    print("Occurences of non-allergenic foods:")
    print(sum(count_occurences(foods, food) for food in get_nonallergenic(foods)))

    allergens = identify_allergens(foods)
    print(",".join(val for key, val in sorted(allergens.items())))
