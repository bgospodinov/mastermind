from multiprocessing import Pool, Value
import logging
from mastermind import Mastermind
from util import pretty_name_8_colors
from argparser import parser

logger = logging.getLogger('mastermind')
logger.propagate = False
logger.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)

args = parser.parse_args()
game_solver = Mastermind(args.k, args.n, logger=logger, pretty_printer=pretty_name_8_colors)


def init_worker(shared_counter):
    global counter
    counter = shared_counter


# hack to overcome limitation of Pool.map which is unable to execute instance methods
def f(x):
    res = game_solver.batch_solve(x)
    counter.value += 1
    logger.info("{}/{} {}%".format(counter.value, len(game_solver.all_possible_combinations),
                                   100.0 * counter.value / len(game_solver.all_possible_combinations)))
    return res


if __name__ == '__main__':
    try:
        # counter in shared memory to measure progress across pool workers
        counter = Value('i', 0)
        with Pool(args.p, initializer=init_worker, initargs=(counter,)) as p:
            attempts = p.map(f, game_solver.all_possible_combinations)

        print("Min/max/avg - {}/{}/{}".format(min(attempts), max(attempts), sum(attempts) / len(attempts)))
    finally:
        ch.close()
        logger.removeHandler(ch)
