import argparse

parser = argparse.ArgumentParser(description='Solve Mastermind concurrently for k colors and n placeholders.')
parser.add_argument('--k', type=int, default=8, help='number of colors')
parser.add_argument('--n', type=int, default=4, help='number of placeholders')
parser.add_argument('--p', type=int, default=5, help='number of pool workers')