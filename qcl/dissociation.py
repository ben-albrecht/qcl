import argparse
import ben
import os

# Dissociation Curve Input Generator for Q-Chem
#   Given some input, a range, and increments, generate several inputs
#   at those incremented coordinate values.

# Obtain arguments given
def get_arguments(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='ifile', help='input file name')
    parser.add_argument('--verbose', action='store_true', help='increase verbosity')
    parser.add_argument('--bins', default=0, type=int, help='number of bins')
    opts = parser.parse_args(args)
    return opts


if __name__ == '__main__':
    work = os.getcwd()
    opts = get_arguments()

    print opts.verbose
    print opts.ifile
    print opts.bins

