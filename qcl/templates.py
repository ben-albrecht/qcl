""" Functions that store locations of various template files """

from __future__ import print_function

import os
from os.path import join, dirname, split, basename, isfile
from shutil import copyfile

import six


def get(jobname):
    """ Return the first templatefile found with name match of jobename """
    for root, _, files in os.walk(join(dirname(__file__), 'templates')):
        for templatefile in [x for x in files if jobname in x]:
            return join(root, templatefile)
    print(jobname, "not found!")
    exit(1)


def user(jobname):
    """User-defined jobs"""
    jobtype = join(join('templates/user', jobname))
    return join(dirname(__file__), jobtype)


def exists(jobname, verbose=True):
    """Check template exists, if it does not, list available templates"""
    for _, _, files in os.walk(join(dirname(__file__), 'templates')):
        for _ in [x for x in files if jobname in x]:
            return True
    if verbose:
        print(jobname, "not found!")
        print("Here are the current available templatefiles:")
        list()
    return False


def list(opts=None):
    """List template files in templates directory"""
    for root, _, files in os.walk(join(dirname(__file__), 'templates')):
        for template in files:
            print(join(split(root)[-1], template))


def remove(opts):
    """Remove template from templates directory"""
    destfile = user(opts.templatefile)
    if isfile(destfile):
        os.remove(destfile)
        print(destfile, "removed")
    else:
        print(destfile, "does not exist")


def add(opts):
    """Add template to templates directory"""
    destfile = user(opts.templatefile)
    response = 'y'
    if isfile(opts.templatefile):
        if isfile(destfile):
            print(destfile, ' already exists, overwrite? [Y/n]')
            response = six.moves.input()

    if response == 'Y' or response == 'y':
        copyfile(opts.templatefile, destfile)
        print(destfile, " template file created")
    else:
        print('aborting')


def cat(opts):
    """Concatenate template from templates directory"""
    for root, _, files in os.walk(join(dirname(__file__), 'templates')):
        for templatefile in [x for x in files if opts.templatefile in x]:
            curtempfile = (join(root, templatefile))
            print(join(split(dirname(curtempfile))[-1], basename(curtempfile)))
            with open(curtempfile, 'r') as handle:
                lines = handle.readlines()
                for line in lines:
                    print(line, end='')
                print('\n', end='')
