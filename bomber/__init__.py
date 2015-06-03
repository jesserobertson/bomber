""" file:   __init__.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   June 2015
"""

from .converters import grid_to_geotiff
from ._version import __version__

__all__ = ['__version__', 'grid_to_geotiff']
