#!/usr/bin/env python
import recon.release
from glob import glob
from numpy import get_include as np_include
from setuptools import setup, find_packages, Extension


version = recon.release.get_info()
recon.release.write_template(version, 'lib/wfc3tools')

setup(
    name = 'wfc3tools',
    version = version.pep386,
    author = 'Megan Sosey',
    author_email = 'help@stsci.edu',
    description = 'Python Tools for WFC3 Data',
    url = 'https://github.com/spacetelescope/wfc3tools',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'astropy',
        'nose',
        'numpy',
        'scipy',
        'sphinx',
        'stsci.sphinxext',
        'stsci.tools',
    ],
    package_dir = {
        '': 'lib',
    },
    packages = find_packages('lib'),
    package_data = {
        'wfc3tools': [
            'pars/*',
            '*.help',
            'htmlhelp/*.html',
            'htmlhelp/_images/*.png',
            'htmlhelp/_images/math/*.png'
        ],
    },
)
