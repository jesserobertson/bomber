""" file:   setup.py (bomber)
    author: Jess Robertson
            CSIRO Earth Science and Resource Engineering
    email:  jesse.robertson@csiro.au
    date:   Wednesday 1 May,
        2013

    description: Distutils installer script for bomber.
"""

import os
from setuptools import setup, find_packages
from update_version import update_version, Version, get_version

def read(*paths):
    """ Build a file path from *paths and return the contents.
    """
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

# Get requirements from requirements.txt file
with open('requirements.txt') as fhandle:
    REQUIREMENTS = [l.strip('\n') for l in fhandle]

# Get version number from _version.py
# Can be updated using python setup.py update_version
update_version()


## PACKAGE INFORMATION
setup(
    # Metadata
    name='bomber',
    version=get_version(),
    description='Get data from the BoM in Python',
    long_description=read('readme.md'),
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='https://stash.csiro.au/projects/POH/repos/bomber',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],

    # Dependencies
    install_requires=REQUIREMENTS,
    extras_require={},

    # Contents
    packages=find_packages(exclude=['tests', 'docs']),
    test_suite='tests',
    ext_modules=[],
    package_data={},
    cmdclass={
        'update_version': Version
    }
)
