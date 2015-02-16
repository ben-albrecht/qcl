"""
Quantum Chemistry Laboratory Main Python File
"""
import argparse
from qcl import figs


def get_arguments(args=None):
    """
    Parse arguments
    :returns: opts
    """
    # Main Parser
    parser = argparse.ArgumentParser(prog='qcl')

    # Subparsers
    subparsers = parser.add_subparsers(help="sub-commands")

    # Figures Subparser
    parser_figs = subparsers.add_parser(
        'figs',
        help='Figure generation on the fly',
        )
    parser_figs.add_argument(
        'fname',
        help='Quantum chemistry output logfile',
        )
    parser_figs.add_argument(
        '--job',
        type=str,
        default='auto',
        choices=['sp', 'opt', 'vib', 'auto'],
        help='Jobtype of job, determined automatically if not given',
        )
    parser_figs.set_defaults(func=figs.main)

    # Subparser for conformers
    #parser_conformers = subparsers.add_parser(
    #    'conformers',
    #    help='Conformer generation on the fly'
    #    )

    #parser_conformers.add_argument(
    #    'fname',
    #    help='xyz file name, with charge, multiplicity in comment'
    #    )

    #parser_conformers.add_argument(
    #    '--ecutoff',
    #    type=int,
    #    default=2,
    #    help='Energy cutoff from lowest energy molecule (Kcal/mol)')

    #parser_conformers.set_defaults(func=conformers.main)

    #parser_status = subparsers.add_parser('status',
    #help='Status overview of input and outputfiles')

    #parser_status.add_argument('datadir',
    # help='top data directory to search recursively for inputs and outputs')
    #parser_status.set_defaults(func=status.main)

    opts = parser.parse_args(args)
    return opts


def main():
    """ Main function for application """
    opts = get_arguments()
    opts.func(opts)
