""" file:   measurements.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   June 2015

    description: get climate classification data from BoM
"""

from __future__ import print_function, division

from .utilities import download, option_checker

# Info about service
URI = "http://www.bom.gov.au/web01/ncc/www/climatology/" + \
      "climate-classification/{dataset}.zip"
DATASETS = {
    'kpn': [],
    'kpngrp': [],
    'seasgrpb': [],
    'seasb': [],
    'tmp_zones': []
}

def get_classification(dataset='seasb', filename=None):
    """ Get climate classification from BoM's demented non-existent API
    """
    # Generate options list from arguments
    option_checker(dataset=(dataset, DATASETS))
    options = {'dataset': dataset}

    # Download and munge data
    filename = filename or dataset
    return download(URI, options, filename)
