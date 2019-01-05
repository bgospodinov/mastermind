from random import randint

colour_mapping = {"a": "red", "b": "green", "c": "blue", "d": "purple", "e": "yellow", "f": "white", "g": "pink",
             "h": "orange"}


def pretty_name_8_colors(attempt):
    name = []
    for c in attempt:
        if c in colour_mapping:
            name.append(colour_mapping[c])
        else:
            name.append(c)
    return " ".join(name)


def draw_combination(possible_combinations):
    return possible_combinations[randint(0, len(possible_combinations) - 1)]