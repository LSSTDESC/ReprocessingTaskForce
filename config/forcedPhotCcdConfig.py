import lsst.meas.modelfit
import lsst.shapelet

import lsst.meas.extensions.shapeHSM
config.measurement.plugins.names |= ["ext_shapeHSM_HsmShapeRegauss", "ext_shapeHSM_HsmSourceMoments",
                                    "ext_shapeHSM_HsmPsfMoments"]
config.measurement.plugins['ext_shapeHSM_HsmShapeRegauss'].deblendNChild=''
config.measurement.slots.shape = "ext_shapeHSM_HsmSourceMoments"

config.doApCorr=True

config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('CLIPPED')
config.measurement.plugins['base_PixelFlags'].masksFpCenter.append('BRIGHT_OBJECT')
config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('BRIGHT_OBJECT')
