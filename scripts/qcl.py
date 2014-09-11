import argparse
import os
import qvalgrind




# qcl main script
# Quantum Chemistry Lab utilities (qcl)

def get_arguments(args=None):
    parser = argparse.ArgumentParser()
    #parser.add_argument(dest='ifile', help='input file name')
    parser.add_argument('--verbose', action='store_true', help='increase verbosity')
    #parser.add_argument('--bins', default=0, type=int, help='number of bins')
    parser.add_argument('task', default="qchem", help='task to perform')

    opts = parser.parse_args(args)
    return opts

tasks = {"qc" : "qchem",
                "val" : qvalgrind_main,
                "qval": qvalgrind_main,
                "valgrind" : "qvalgrind_main",
                "qvalgrind" : "qvalgrind_main",
}


if __name__ == '__main__':
    work = os.getcwd()
    opts = get_arguments()

    print opts.verbose
    print opts.task

    args = [1, 2]
    qvalgrind_main(args)
    # Execute tasks 
    #tasks[opts.task](args)
    # tasks[opts.task]
    
    
    #print opts.ifile
    #print opts.bins


