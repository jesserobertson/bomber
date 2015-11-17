""" file:   utilities.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   June 2015

    description: utility functions for bomber
"""

from __future__ import print_function, division

from .converters import grid_to_geotiff

import requests
import subprocess

def download(uri, options, filename, fmt='geotiff'):
    """ Download data to GeoTIFF
    """
    # Download and munge data
    response = requests.get(uri.format(**options))
    if response.ok:
        zipfilename = filename + '.Z'
        with open(zipfilename, 'wb') as sink:
            sink.write(response.content)
            subprocess.call(['uncompress', zipfilename])

        # Convert data to geotiff
        if fmt.lower() == 'geotiff':
            filename = grid_to_geotiff(filename)
        print('Downloaded data to {0}'.format(filename))
        return filename

    else:
        print('Download failed')
        return None

def option_checker(**arguments):
    """ Generate option checkers using some supplied checks

        Provide the checker with a list of checks, where each check is
        an argument name, and a list of allowed balues
    """
    err_str = ('Argument {0}={1} is unknown. Allowed '
               'values for {0} are {2}.')
    for arg, (value, expected) in arguments.items():
        if value not in expected:
            err = err_str.format(arg, value, expected)
            raise ValueError(err)
