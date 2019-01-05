from builtins import print
from util import pretty_name_8_colors, colour_mapping
from mastermind import Mastermind
from argparser import parser
import sys


class InvalidStateException(Exception):
    pass


args = parser.parse_args()
game_solver = Mastermind(args.k, args.n)

print("Welcome to Mastermind interactive solver.")
print("Please think of a code combination containing {} pegs from {} colors ({}).".format(args.n, args.k, ", ".join(list(colour_mapping.values())[:args.k])))
print("\n")

# number of red and white pegs from the opponent's response
w, r = 0, 0
all_combinations = game_solver.all_possible_combinations
possible_combinations = game_solver.all_possible_combinations
attempt = game_solver.initial_attempt
num_attempts = 0

try:
    while r != args.n:
        num_attempts += 1
        print("Attempt {} is {}.".format(num_attempts, pretty_name_8_colors(attempt)))

        r = int(input("Please enter number of red pegs: "))
        if r == args.n:
            break
        w = int(input("Please enter number of white pegs: "))

        response = (w, r)

        if r + w > args.n:
            raise InvalidStateException

        possible_combinations = game_solver.filter_possible_combinations(possible_combinations, attempt, response)
        tmp_attempt = attempt
        attempt = game_solver.calculate_best_move(all_combinations, possible_combinations)

        # repetition should never happen (gives no new information)
        if attempt == tmp_attempt:
            raise InvalidStateException

        print("\n")

    print("Solved in {}. Secret code is {}.".format(num_attempts, pretty_name_8_colors(attempt)))

except InvalidStateException:
    print("You have reached an impossible state. You have probably entered an inconsistent amount of white and red pegs.", file=sys.stderr)
    print("Terminating.", file=sys.stderr)
    sys.exit(1)