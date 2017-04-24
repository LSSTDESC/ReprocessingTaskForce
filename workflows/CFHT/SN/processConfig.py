config.charImage.repair.cosmicray.nCrPixelMax=1000000
config.calibrate.photoCal.fluxField='base_CircularApertureFlux_6_0_flux'
config.calibrate.photoCal.magLimit=22.0
config.calibrate.photoCal.photoCatName="e2v" 
config.calibrate.photoCal.applyColorTerms=True
config.calibrate.photoCal.badFlags=['base_PixelFlags_flag_edge', 'base_PixelFlags_flag_interpolated', 'base_PixelFlags_flag_saturated', 'base_PixelFlags_flag_crCenter']

from lsst.meas.astrom.anetAstrometry import ANetAstrometryTask
config.calibrate.astrometry.retarget(ANetAstrometryTask)
config.calibrate.astrometry.solver.sipOrder=3

# use Chebyshev background estimation

config.calibrate.detectAndMeasure.detection.background.useApprox=True
config.calibrate.detectAndMeasure.detection.background.binSize = 128
config.calibrate.detectAndMeasure.detection.background.undersampleStyle = 'REDUCE_INTERP_ORDER'
