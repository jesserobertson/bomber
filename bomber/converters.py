""" file:   converters.py (bomber)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   June 2015

    description: tools to convert BoM grid file formats to geotiff
"""

from __future__ import print_function, division

import numpy
import affine
import rasterio

def grid_to_geotiff(filename, return_data=False):
    """ Load data from a Bureau of Meterology 'grid' file and dump out to geotiff

        Output is written to geotiff

        Parameters:
            filename - the file name of the BoM grid file to convert
            return_data - if true, then a Numpy array with the imported
                data is returned when conversion is successful.
    """
    # First six lines are metadata
    # Note: gonna assume the origin is WGS84
    with open(filename) as fhandle:
        meta = {}
        for line in fhandle:
            key, value = line.split()
            key = key.lower()
            meta[key] = value
            if len(meta) == 6:
                break

    # Handle sloppy labelling from BoM
    for idx in ('x', 'y'):
        if meta.get(idx + 'llcorner') is not None:
            meta[idx + 'llcenter'] = meta[idx + 'llcorner']

    # Convert metadata to right format
    type_mapping = {'ncols': int, 'nrows': int,
                    'xllcenter': float, 'yllcenter': float,
                    'cellsize': float, 'nodata_value': float}
    for key, typef in type_mapping.items():
        meta[key] = typef(meta[key])

    # Next lines are info - swap out nodata with nans
    # Last lines are also metadata 'header' but we don't care about that
    data = numpy.genfromtxt(filename, dtype=numpy.float64,
                            skip_header=6, skip_footer=18)

    # Check whether we have masked values to deal with
    has_mask = (meta.get('nodata_value') is not None)
    if has_mask:
        has_mask = True
        nodata_mask = (data - meta['nodata_value']) ** 2 < 1e-6

    ## MAKE GEOTIFF
    # Generate the transform for the grid
    aff = affine.Affine.translation(
        meta['xllcenter'] - meta['cellsize'] * 0.5,
        meta['yllcenter'] + (meta['nrows'] - 0.5) * meta['cellsize']
    ) * affine.Affine.scale(meta['cellsize'], -meta['cellsize'])

    # Make metadata for geotiff
    geotiff_meta = {
        'affine': aff,
        'transform': aff.to_gdal(),
        'width': meta['ncols'],
        'height': meta['nrows'],
        'nodata': meta['nodata_value'],
        'tiled': 'no',
        'crs': {'init': 'epsg:4326'},  # assuming WGS84
        'driver': 'GTiff',
        'dtype': 'float64',
        'blockxsize': 128,
        'blockysize': 128,
        'count': 1
    }

    # Write out to file
    with rasterio.drivers():
        with rasterio.open(filename + '.geotiff', 'w', **geotiff_meta) as sink:
            sink.write_band(1, data)
            if has_mask:
                sink.write_mask(nodata_mask.astype(bool))

    # If we're returning the data, convert data mask to numpy.nan
    if return_data:
        if has_mask:
            data[nodata_mask] = numpy.nan
        return data
    else:
        return filename + '.geotiff'
