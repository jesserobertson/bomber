""" file:   measurements.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   June 2015

    description: get measurements data from BoM
"""

from __future__ import print_function, division

from .utilities import download, option_checker

import calendar

# Info about service
URI = "http://www.bom.gov.au/web03/ncc/www/awap/{dataset}" + \
      "/{variable}/{timespan}/grid/0.05/history/nat/{date}.grid.Z"
DATASETS = {
    'temperature': ['maxave', 'minave'],
    'rainfall': ['totals'],
    'vprp': ['vprp09', 'vprp15'],
    'solar': ['solarave'],
    'ndvi': ['ndviave']
}
TIMESPANS = ['month', 'daily']

def get_measurements(dataset='temperature', variable=None, timespan='month',
                     year=2014, month=1, filename=None):
    """ Get some measurements from BoM's demented non-existant API
    """
    # Make datestring from year and month
    lastday = calendar.monthrange(year, month)[1]
    date_string = '{0}{1:02d}01{0}{1:02d}{2}'.format(year, month, lastday)

    # Generate options list from arguments & check
    option_checker(
        dataset=(dataset, DATASETS.keys()),
        timespan=(timespan, TIMESPANS))
    variable = variable or DATASETS[dataset][0]
    option_checker(
        variable=(variable, DATASETS[dataset]))
    options = {'dataset': dataset,
               'timespan': timespan,
               'date': date_string,
               'variable': variable}

    # Generate filename
    if not filename:
        filename = '{dataset}_{variable}_{timespan}_{date}'.format(**options)

    # Download and munge data
    return download(URI, options, filename)
