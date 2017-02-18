# qcl

qcl is a python package for managing the workflow and automating tasks that
many computational chemists face on a daily basis. The package serves as both a
command line tool, `qcl`, and a Python module that could be used in other Python
programs.

Here are some features currently available:

    figs                Quick plots of convergence criteria given an outputfile
    conformers          Naive conformer generation in Python
    obconformers        Open Babel conformer generation wrapper
    stretch             Stretch product at bond-forming atoms for transition state initial guess.
    templates           Template file management
    minima              Find minimum energy among many outputfiles
    zmatrix             Generate Z-Matrix from xyzfile
    rmsd                Align geometry and compute rmsd between 2 xyzfiles


## Installation

Install release from PyPI:

`pip install qcl`

Install from master:

```bash
# Clone the source
>git clone https://github.com/ben-albrecht/qcl
>cd qcl

# Install dependencies and package (in a virtualenv if you prefer)
>pip install -r requirement.txt
>python setup.py install # (or `make install`)

# qcl command line tool should now be in your $PATH
>qcl --help

usage: qcl [-h]
           {figs,conformers,obconformers,stretch,templates,minima,zmatrix,rmsd,job}
           ...

positional arguments:
  {figs,conformers,obconformers,stretch,templates,minima,zmatrix,rmsd,job}
                        sub-commands
    figs                Figure generation on the fly
    conformers          Conformer generation on the fly
    obconformers        Conformer generation on the fly with Open Babel
    stretch             TS search from product of combination reactions.
    templates           Template file management
    minima              Find global minimum of many outputs
    zmatrix             Generate Z-Matrix
    rmsd                Compute rmsd between 2 xyzfiles
    job                 Extract ccdata from files and write new inputs

optional arguments:
  -h, --help            show this help message and exit

# and your $PYTHONPATH
>python
Python 3.5.2 (default, Nov  5 2016, 21:37:10)
[GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import qcl
>>> print(qcl.parse.xyzfile.__doc__)
Parse xyzfile to ccData or ccData_xyz object
>>>

```

## Usage

### Command line tool

Usage information for a specific subcommand is printed when throwing `--help`
like so:

```bash
>qcl conformers --help

usage: qcl conformers [-h] [--interval INTERVAL]
                      [--templatefiles TEMPLATEFILES [TEMPLATEFILES ...]]
                      xyzfile

positional arguments:
  xyzfile               xyz file, with charge and multiplicity as comments

optional arguments:
  -h, --help            show this help message and exit
  --interval INTERVAL   Angle interval to rotate dihedral angle by
  --templatefiles TEMPLATEFILES [TEMPLATEFILES ...], -t TEMPLATEFILES [TEMPLATEFILES ...]
                        Single template file or list of template files.
                        Necessary to generate inputs for conformers
```

### Conformers Example

The conformers subcommand will generate all conformers of a molecule provided
as an xyzfile using a naive algorithm. The default interval of rotation is 60
degrees, but this can be changed with the --interval flag. The resulting
conformers will be written to a multixyzfile named `all.xyz` in the current
working directory.

```bash
>qcl conformers test/test.xyz
Total number of rotatable bonds          : 3
interval (degrees) of dihedral rotation : 60.0
Total intervals per rotatable bond      : 6
Total number of systematical conformers  : 216
216 conformers generated

>head all.xyz
13

  C 0.00000000 0.00000000 0.00000000
  O 1.35990413 0.00000000 0.00000000
  O -0.58772319 0.00000000 -1.07001980
  C -0.80335693 0.07246293 1.27324932
  Si -0.87463131 -1.59912105 2.12493402
  H 0.44123291 -2.12448304 2.50700950
  H -1.51109961 -2.56720463 1.21939819
  H -1.69316219 -1.47832678 3.34026474
```
### Terminology and Formats

qcl uses the excellent computational chemistry parsing and algorithms module,
[cclib](https://github.com/cclib/cclib).
The qcl chemical data structures are represented as [cclib
objects](http://cclib.github.io/data.html), which this package consistently
refers to as `ccdata`.

In qcl, `xyzfile` refers to the
[xyz file format](https://en.wikipedia.org/wiki/XYZ_file_format), and
`multixyzfile` refers to multiple xyzfiles concatenated, which is supported by
most xyzfile file viewers, e.g. [Avogadro](https://avogadro.cc/).

`zmatrix` refers to the
[Z-Matrix](https://en.wikipedia.org/wiki/Z-matrix_(chemistry) of a system.

`qcheminput` refers to [Q-Chem input files](http://www.q-chem.com/), and
`mopacinput` refers to [MOPAC input files](http://openmopac.net/).
