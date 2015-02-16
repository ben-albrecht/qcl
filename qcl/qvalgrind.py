import argparse
import os

def get_arguments(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='ifile', help='input file name')
    parser.add_argument('--verbose', action='store_true', help='increase verbosity')
    #parser.add_argument('--bins', default=0, type=int, help='number of bins')
    parser.add_argument('task', nargs='1', default="qchem", type=str, help='task to perform')

    opts = parser.parse_args(args)
    return opts

def qvalgrind_main(args):
    # Check if $QC is defined
    print "valgrind $QC/exe/qcprog.exe"




if __name__ == '__main__':
    work = os.getcwd()
    opts = get_arguments()

    print opts.verbose
    print opts.task
    
args = [1, 2]
qvalgrind_main(args)
