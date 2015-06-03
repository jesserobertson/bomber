""" file:   measurements.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   June 2015

    description: get measurements data from BoM
"""

from __future__ import print_function, division

from .converters import grid_to_geotiff

import calendar
import requests
import subprocess
import rasterio

# Info about service
URI = "http://www.bom.gov.au/web03/ncc/www/awap/{dataset}/{variable}/{timespan}/grid/0.05/history/nat/{date}.grid.Z"
DATASETS = {
    'temperature': ['maxave', 'minave'],
    'rainfall': ['totals'],
    'vprp': ['vprp09', 'vprp15'],
    'solar': ['solarave'],
    'ndvi': ['ndviave']
}
TIMESPANS = ['month', 'daily']


def _check_options(dataset, variable, timespan, date):
    """ Checks that values for options are correct
    """
    checks = [
        ('dataset', dataset, DATASETS.keys()),
        ('variable', variable, DATASETS[dataset]),
        ('period', timespan, TIMESPANS)
    ]
    err_str = 'Argument {0}={1} is unknown. Allowed values for {0} are {2}.'
    for arg, value, allowed_values in checks:
        if value not in allowed_values:
            raise ValueError(err_str.format(arg, value, allowed_values))


def get_measurements(dataset='temperature', variable=None, timespan='month', 
                     year=2014, month=1, filename=None):
    """ Get some measurements from BoM's demented non-existant API
    """
    # Make datestring from year and month
    lastday = calendar.monthrange(year, month)[1]
    date_string = '{0}{1:02d}01{0}{1:02d}{2}'.format(year, month, lastday)
    
    # Generate options list from arguments
    options = {'dataset': dataset, 
               'variable': variable or DATASETS[dataset][0], 
               'timespan': timespan, 
               'date': date_string}
    _check_options(**options)

    # Generate filename
    if not filename:
        filename = '{dataset}_{variable}_{timespan}_{date}'.format(**options)

    # Download and munge data
    response = requests.get(URI.format(**options))
    if response.ok:
        zipfilename = filename + '.Z'
        with open(zipfilename, 'wb') as sink:
            sink.write(response.content)
            subprocess.call(['uncompress', zipfilename])

        # Convert data to geotiff
        grid_to_geotiff(filename)
        geotiff = filename + '.geotiff'
        print('Downloaded data to {0}'.format(geotiff))
        return geotiff

    else:
        print('Download failed')