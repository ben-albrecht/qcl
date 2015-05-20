"""
Setup File for qcl
"""
import os
from setuptools import setup, find_packages


def read(fname):
    """ Read a file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="qcl",
    packages=find_packages(),
    version="0.0.3",
    author="Ben Albrecht",
    author_email="benalbrecht@pitt.edu",
    description=("Quantum Chemistry Laboratory"),
    # This feature is not compatible with pip install :(
    #long_description=read('README.md'),
    keywords="Quantum Chemistry",
    url='https://github.com/ben-albrecht/qcl',
    download_url='https://github.com/ben-albrecht/qcl/tarball/0.0.3',
    include_package_data=True,
    license="MIT",
    entry_points={'console_scripts': ['qcl = qcl.__main__:main']}
)
