"""
Setup File for qcl
"""
import os
from setuptools import setup, find_packages
#from pip.req import parse_requirements

# Requirements
# parse_requirements() returns generator of pip.req.InstallRequirement objects


def read(fname):
    """ Read a file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="qcl",
    version="0.0.1",
    author="Ben Albrecht",
    author_email="benjaminjoelalbrecht@gmail.com",
    description=("Quantum Chemistry Laboratory Tool Kit"),
    keywords="Quantum Chemistry",

    # To include templates directory
    include_package_data=True,
    packages=find_packages(),
    #install_requires = reqs,
    long_description=read('README.md'),
    entry_points=
    {'console_scripts': ['qcl = qcl.__main__:main']}
    #'conformers=polymer.conformers:main']}
    #license = "BSD",
    #url = "http://packages.python.org/an_example_pypi_project",
    #classifiers=[
    #    "Development Status :: 3 - Alpha",
    #    "Topic :: Utilities",
    #    "License :: OSI Approved :: BSD License",
    #],
)
