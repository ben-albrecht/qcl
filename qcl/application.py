"""Main qcl Application called when qcl script is invoked """
from argparse import ArgumentParser, \
    ArgumentDefaultsHelpFormatter, \
    ArgumentTypeError
from qcl import conformers, obconformers, minima, \
    stretch, templates, zmatrix, figs, rmsd

def get_arguments(args=None):
    """
    Parse command line arguments
    :args: Preset arguments
    :returns: opts
    """
    # Main Parser
    parser = ArgumentParser(
        prog='qcl',
        formatter_class=ArgumentDefaultsHelpFormatter)

    # Subparsers
    subparsers = parser.add_subparsers(help="sub-commands")

    # Figures Subparser
    parser_figs = subparsers.add_parser(
        'figs',
        help='Figure generation on the fly',
        )

    # Figures arguments
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
    # Figures function call
    parser_figs.set_defaults(func=figs.main)

    # Conformer subparser
    parser_conformers = subparsers.add_parser(
        'conformers',
        help='Conformer generation on the fly')

    # Conformer arguments
    parser_conformers.add_argument(
        'xyzfile',
        help='xyz file, with charge and multiplicity as comments')

    parser_conformers.add_argument(
        '--interval',
        type=angle,
        default=60.0,
        help='Angle interval to rotate dihedral angle by')

    parser_conformers.add_argument(
        '-t',
        nargs='+',
        default=None,
        help='Single template file or list of template files.\
                Necessary to generate inputs for conformers')

    # Conformer function call
    parser_conformers.set_defaults(func=conformers.main)

    # Open Babel Conformer subparser
    parser_obconformers = subparsers.add_parser(
        'obconformers',
        help='Conformer generation on the fly with Open Babel')

    # Open Babel Conformer arguments
    parser_obconformers.add_argument(
        'xyzfile',
        help='xyz file, with charge and multiplicity as comments')

    # Open Babel Conformer arguments
    parser_obconformers.add_argument(
        '-f',
        '--force',
        action='store_true',
        default=False,
        help='do not prompt before overwriting')

    parser_obconformers.add_argument(
        '-n',
        '--nconf',
        default=1000,
        help='Number of obconformers to generate for openbabel')

    parser_obconformers.add_argument(
        '-t',
        '--templatefiles',
        nargs='+',
        default=None,
        help='Single template file or list of template files.\
                Necessary to generate inputs for obconformers')

    # Open Babel Conformer function call
    parser_obconformers.set_defaults(func=obconformers.main)

    # Stretch subparser
    parser_stretch = subparsers.add_parser(
        'stretch',
        help='TS search from product of combination reactions.')

    # Stretch arguments
    parser_stretch.add_argument(
        'outputfile',
        help="""Q-Chem outputfile.\n\
            Make sure the bond-forming atoms are the top 2 atoms!""")

    parser_stretch.add_argument(
        '-n',
        '--length',
        default=2.0,
        type=float,
        help='Stretch length in Angstroms'
        )

    parser_stretch.add_argument(
        '-t',
        '--templatefiles',
        nargs='+',
        default=None,
        help='Template file for job(s) to setup'
        )

    # Stretch function call
    parser_stretch.set_defaults(func=stretch.main)

    # Template subparser
    parser_templates = subparsers.add_parser(
        'templates',
        help='Template file management')

    # Template sub-subparsers
    subparsers_templates = parser_templates.add_subparsers(
        help="template sub-commands")

    # List sub-subparser
    parser_templates_list = subparsers_templates.add_parser(
        'list',
        help='List available templates in templates directory')
    parser_templates_list.set_defaults(func=templates.list)

    # Add sub-subparser
    parser_templates_add = subparsers_templates.add_parser(
        'add',
        help='Add template to templates directory')
    parser_templates_add.add_argument(
        'templatefile',
        help='Template file to add')
    parser_templates_add.set_defaults(func=templates.add)

    # Remove sub-subparser
    parser_templates_remove = subparsers_templates.add_parser(
        'remove',
        help='Remove template from templates directory')
    parser_templates_remove.add_argument(
        'templatefile',
        help='Template file to remove')
    parser_templates_remove.set_defaults(func=templates.remove)

    # Cat sub-subparser
    parser_templates_cat = subparsers_templates.add_parser(
        'cat',
        help='Concatenate template from templates directory')
    parser_templates_cat.add_argument(
        'templatefile',
        help='Template file to concatenate')
    parser_templates_cat.set_defaults(func=templates.cat)


    # Minima subparser
    parser_minima = subparsers.add_parser(
        'minima',
        help='Find global minimum of many outputs')

    # Minima arguments
    parser_minima.add_argument(
        'outputfiles',
        nargs='+',
        default=None,
        help='Outputfiles to find a minimum among')

    # Minima function call
    parser_minima.set_defaults(func=minima.main)

    # Zmatrix subparser
    parser_zmatrix = subparsers.add_parser(
        'zmatrix',
        help="Generate Z-Matrix")

    # Zmatrix arguments
    parser_zmatrix.add_argument('xyzfile', help='xyzfile to convert')

    # Zmatrix function call
    parser_zmatrix.set_defaults(func=zmatrix.main)

    # rmsd subparser
    parser_rmsd = subparsers.add_parser(
        'rmsd',
        help="Compute rmsd between 2 xyzfiles")

    # rmsd arguments
    parser_rmsd.add_argument('xyzfile1', help='xyzfile1')
    parser_rmsd.add_argument('xyzfile2', help='xyzfile2')

    # rmsd function call
    parser_rmsd.set_defaults(func=rmsd.main)

    opts = parser.parse_args(args)

    return parser.parse_args(args)


def restricted_float(x):
    """Custom type for float between 0.0 and 1.0"""
    x = float(x)
    if not 0.0 <= x <= 1.0:
        raise ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x


def angle(x):
    """Custom type for angles"""
    x = float(x)
    if not 0 <= x < 360.0:
        raise ArgumentTypeError("Angle %r not in range [0.0, 360.0]"%(x,))
    return x


def main():
    """ Main Function of qcl module """
    opts = get_arguments()
    opts.func(opts)
