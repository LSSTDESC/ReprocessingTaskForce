# Apply the brighter fatter correction
config.isr.doBrighterFatter=False

config.charImage.repair.cosmicray.nCrPixelMax=1000000

#from lsst.meas.astrom.anetAstrometry import ANetAstrometryTask
#config.calibrate.astrometry.retarget(ANetAstrometryTask)
#config.calibrate.astrometry.solver.sipOrder=3

#config.charImage.astrometry.wcsFitter.order=3
#onfig.charImage.astrometry.matcher.maxMatchDistArcSec=3.0

#config.calibrate.astrometry.refObjLoader.filterMap = { 'i2': 'i',
#                                                           }
config.charImage.astrometry.refObjLoader.filterMap = { 'i2': 'i'}

#config.calibrate.photoCal.fluxField='base_CircularApertureFlux_6_0_flux'
#config.calibrate.photoCal.magLimit=22.0
#config.calibrate.photoCal.photoCatName="e2v"
#config.calibrate.photoCal.applyColorTerms=True
#config.calibrate.photoCal.badFlags=['base_PixelFlags_flag_edge', 'base_PixelFlags_flag_interpolated', 'base_PixelFlags_flag_saturated', 'base_PixelFlags_flag_crCenter']

import lsst.pipe.tasks.colorterms
config.calibrate.photoCal.colorterms.data['e2v'].data['i2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].c1=0.085
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].primary='i'
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].secondary='r'

# The following should be included for u filter in order to lower the source detection threshold
#config.charImage.detectAndMeasure.detection.includeThresholdMultiplier=1.0

# use Chebyshev background estimation
config.charImage.background.useApprox=True
config.charImage.detectAndMeasure.detection.background.binSize=128
config.charImage.detectAndMeasure.detection.background.useApprox=True
config.charImage.background.binSize = 128
config.charImage.background.undersampleStyle = 'REDUCE_INTERP_ORDER'
config.charImage.detectAndMeasure.detection.background.binSize = 128
config.charImage.detectAndMeasure.detection.background.undersampleStyle='REDUCE_INTERP_ORDER'
config.charImage.detectAndMeasure.detection.background.binSize = 128
config.charImage.detectAndMeasure.detection.background.undersampleStyle = 'REDUCE_INTERP_ORDER'

# Select and configure psfex PSF solver
import lsst.meas.extensions.psfex.psfexPsfDeterminer
#print "==== Using psfex PSF solver ====="
config.charImage.measurePsf.psfDeterminer.name = "psfex"

 
