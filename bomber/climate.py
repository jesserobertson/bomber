""" file:   __init__.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   September 2015

    description: Load data from BoM's climate repos
"""

from __future__ import print_function, division

from .utilities import download, option_checker

# Info about service
# Service is URI/{dataset}/{variable}{start}{end}.zip
# where start is X1 or X6, and end is (X+1/2/3)0 or (X+1/2/3)5
# and 1/2/3 is determined by 10, 20 or 30 year averages
URI = "http://www.bom.gov.au/web01/ncc/www/climatology/{dataset}/" + \
      "{variable}{timestamp}.zip"
DATASETS = {
    'decadal-temperature': ['mx', 'mn'],
    'decadal-rainfall': ['r']
}
START_YEARS = [1901, 1906, 1911, 1916, 1921, 1926, 1931, 1936, 1941,
               1946, 1951, 1956, 1961, 1966, 1971, 1976, 1981, 1986,
               1991, 1996, 2001, 2006]
PERIOD = [10, 20, 30]


def get_climate(dataset='decadal-temperature', variable=None,
                start_year=1996, period=10, filename=None):
    """ Get some climate averages from BoM
    """
    # Generate options list from arguments & check
    option_checker(
        dataset=(dataset, DATASETS.keys()),
        start_year=(start_year, START_YEARS))
    variable = variable or DATASETS[dataset][0]
    option_checker(
        variable=(variable, DATASETS[dataset]))

    # Make start and end years
    start, end = start_year, start_year + period - 1
    timestamp = str(start)[-2:] + str(end)[-2:]
    options = {'dataset': dataset,
               'variable': variable,
               'start_year': start_year,
               'period': period,
               'timestamp': timestamp}

    # Generate filename
    if not filename:
        filename = '{dataset}_{variable}_{start_year}_{period}'.format(**options)

    # Download and munge data
    return download(URI, options, filename)
