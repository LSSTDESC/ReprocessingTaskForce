# Configuration file for measureCoaddSources

from lsst.meas.astrom.anetAstrometry import ANetAstrometryTask
config.astrometry.retarget(ANetAstrometryTask)
config.astrometry.solver.sipOrder=3

import lsst.meas.extensions.shapeHSM
config.measurement.plugins.names |= ["ext_shapeHSM_HsmShapeRegauss", "ext_shapeHSM_HsmSourceMoments",
                                    "ext_shapeHSM_HsmPsfMoments"]
config.measurement.plugins['ext_shapeHSM_HsmShapeRegauss'].deblendNChild=''
config.measurement.slots.shape = "ext_shapeHSM_HsmSourceMoments"

import lsst.meas.modelfit
import lsst.shapelet

config.measurement.plugins.names |= ["modelfit_ShapeletPsfApprox", "modelfit_CModel"]

config.measurement.doApplyApCorr='yesOrWarn'
