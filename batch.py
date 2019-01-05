from multiprocessing.dummy import Pool as ThreadPool
import logging
from mastermind import Mastermind


def pretty_name(attempt):
    names = {"a": "red", "b": "green", "c": "blue", "d": "purple", "e": "yellow", "f": "white", "g": "pink",
             "h": "orange"}
    name = []
    for c in attempt:
        name.append(names[c])
    return " ".join(name)


k = 8 # NUMBER OF COLORS
n = 4 # NUMBER OF PLACEHOLDERS

logger = logging.getLogger('mastermind')
logger.propagate = False
logger.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)

game_solver = Mastermind(k, n, logger, pretty_name)


# hack to overcome limitation of Pool.map which is unable to execute instance methods
def f(x):
    return game_solver.solve_auto(x)


if __name__ == '__main__':
    try:
        with ThreadPool(5) as p:
            attempts = p.map(f, game_solver.all_possible_combinations)

        print("Max/min/avg - {}/{}/{}".format(max(attempts), min(attempts), sum(attempts) / len(attempts)))
    finally:
        ch.close()
        logger.removeHandler(ch)
