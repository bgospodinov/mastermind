import string
from random import randint
from itertools import product
from collections import Counter
import sys


def draw_combination(possible_combinations):
    return possible_combinations[randint(0, len(possible_combinations) - 1)]


class Mastermind:
    def __init__(self, k, n, logger, prettyPrinter):
        self.k = k
        self.n = n
        self.all_possible_combinations = list(product(string.ascii_lowercase[:self.k], repeat=n))
        self.prettyPrinter = prettyPrinter
        self.logger = logger
        self.cache = {}

    def evaluate(self, this, that):
        assert len(this), len(that)

        cache_key_list = [''.join(this), ''.join(that)]
        cache_key_list.sort()
        cache_key = "_".join(cache_key_list)
        if cache_key in self.cache:
            return self.cache[cache_key]

        w = 0
        r = 0

        ignored_chars_indices = []
        for i, c in enumerate(this):
            if c == that[i]:
                r += 1
                ignored_chars_indices.append(i)

        this = [c for i, c in enumerate(this) if i not in ignored_chars_indices]
        that = [c for i, c in enumerate(that) if i not in ignored_chars_indices]

        counter = Counter(this) & Counter(that)
        w = sum(counter.values())
        self.cache[cache_key] = (w, r)
        return w, r

    def filter_possible_combinations(self, possible_combinations, attempt, response):
        return [combination for combination in possible_combinations if
                self.evaluate(attempt, combination) == response and combination != attempt]

    def calculate_best_move(self, all_combinations, possible_combinations):
        possible_responses = [(i, j) for i in range(self.n + 1) for j in range(self.n) if i + j <= self.n]

        # minimax
        max_decrease = - sys.maxsize - 1
        best_combination = draw_combination(possible_combinations)

        for combination in all_combinations:
            min_decrease = sys.maxsize

            # find the minimum decrease in possible combinations
            for response in possible_responses:
                decrease = len(possible_combinations) - len(
                    self.filter_possible_combinations(possible_combinations, combination, response))
                if decrease < min_decrease:
                    min_decrease = decrease

            if min_decrease > max_decrease:
                max_decrease = min_decrease
                best_combination = combination

        return best_combination

    def solve_auto(self, secret_combination):
        num_attempts = 1
        self.logger.debug("==================")
        self.logger.debug("Actual combination:")
        self.logger.debug(self.prettyPrinter(secret_combination))
        self.logger.debug("\n")

        # initial attempt
        attempt = ('a', 'a', 'b', 'b')

        self.logger.debug("Attempts:")
        all_combinations = self.all_possible_combinations
        possible_combinations = self.all_possible_combinations

        while attempt != secret_combination:
            self.logger.debug("Number of possible combinations is {}".format(len(possible_combinations)))
            self.logger.debug(self.prettyPrinter(attempt))
            response = self.evaluate(attempt, secret_combination)
            self.logger.debug(response)

            if len(possible_combinations) < 10:
                self.logger.debug("Possible combinations")
                for combination in possible_combinations:
                    self.logger.debug(self.prettyPrinter(combination))

            possible_combinations = self.filter_possible_combinations(possible_combinations, attempt, response)
            attempt = self.calculate_best_move(all_combinations, possible_combinations)

            num_attempts += 1
            self.logger.debug("\n")

        self.logger.debug("Number of possible combinations is {}".format(len(possible_combinations)))
        self.logger.debug(self.prettyPrinter(attempt))
        self.logger.debug("Total number of attempts is {}".format(num_attempts))
        self.logger.debug("\n")
        print("Solved {} in {} attempts".format(secret_combination, num_attempts))

        return num_attempts
