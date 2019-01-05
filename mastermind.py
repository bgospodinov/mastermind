import string
from itertools import product
from collections import Counter
import sys


class Mastermind:
    def __init__(self, num_colors, num_placeholders, initial_attempt=('a', 'a', 'b', 'b'), logger=None, pretty_printer=None):
        self.k = num_colors
        self.n = num_placeholders
        self.all_possible_combinations = list(product(string.ascii_lowercase[:self.k], repeat=num_placeholders))
        self.pretty_printer = pretty_printer if callable(pretty_printer) else lambda x: x
        self.logger = logger
        self.initial_attempt = initial_attempt
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
        best_combination = None

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

    def batch_solve(self, secret_combination):
        num_attempts = 1

        if self.logger:
            self.logger.debug("==================")
            self.logger.debug("Actual combination:")
            self.logger.debug(self.pretty_printer(secret_combination))
            self.logger.debug("\n")
            self.logger.debug("Attempts:")

        # initial attempt
        attempt = self.initial_attempt

        all_combinations = self.all_possible_combinations
        possible_combinations = self.all_possible_combinations

        while attempt != secret_combination:
            if self.logger:
                self.logger.debug("Number of possible combinations is {}".format(len(possible_combinations)))
                self.logger.debug(self.pretty_printer(attempt))
            response = self.evaluate(attempt, secret_combination)
            if self.logger:
                self.logger.debug(response)

            if len(possible_combinations) < 10:
                if self.logger:
                    self.logger.debug("Possible combinations")
                    for combination in possible_combinations:
                        self.logger.debug(self.pretty_printer(combination))

            possible_combinations = self.filter_possible_combinations(possible_combinations, attempt, response)
            attempt = self.calculate_best_move(all_combinations, possible_combinations)

            assert attempt

            num_attempts += 1
            if self.logger:
                self.logger.debug("\n")

        if self.logger:
            self.logger.debug("Number of possible combinations is {}".format(len(possible_combinations)))
            self.logger.debug(self.pretty_printer(attempt))
            self.logger.debug("Total number of attempts is {}".format(num_attempts))
            self.logger.debug("\n")
            self.logger.info("Solved {} in {} attempts".format(secret_combination, num_attempts))

        return num_attempts
