# Mastermind solver

Implements Donald Knuth's minimax Mastermind algorithm from 1977.

## Batch mode
batch.py --k [number-of-colors] --n [number-of-placeholders]

Exhaustively solves a parametrized version of the Mastermind game in batch mode and provides simple statistics.

## Interactive mode
interactive.py --k [number-of-colors] --n [number-of-placeholders]

Allows to use a computer in a game against a human opponent. At each move the script requires the number of white and red pegs provided by the opponent as an input and responds accordingly.