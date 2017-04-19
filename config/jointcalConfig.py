# Configuration file for jointcal

from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

# Select external catalogs for Astrometry
config.astrometryRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.astrometryRefObjLoader.ref_dataset_name='pan-starrs'
config.astrometryRefObjLoader.filterMap = {
    'u':'g',
    'g':'g',
    'r':'r',
    'i':'i',
    'i2': 'i',
    'z':'z',
    'y':'y',
}

# Select external catalogs for Photometry
config.doPhotometry = False  # comment out to run the photometric calibration
config.photometryRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.photometryRefObjLoader.ref_dataset_name='sdss'
config.photometryRefObjLoader.filterMap = {
    'u': 'U',
    'g': 'G',
    'r': 'R',
    'i': 'I',
    'i2': 'I',
    'z': 'Z',
    'y': 'Z',
}

# These are the default values

# Minimum allowed signal-to-noise ratio for sources used for matching
# (in the flux specified by sourceFluxType); <= 0 for no limit
# config.sourceSelector['matcher'].minSnr = 40.0

# Minimum allowed signal-to-noise ratio for sources used for matching
# (in the flux specified by sourceFluxType); <= 0 for no limit
# config.sourceSelector['astrometry'].minSnr = 10.0


