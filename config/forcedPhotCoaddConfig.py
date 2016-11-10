import lsst.meas.modelfit
import lsst.shapelet

config.measurement.plugins.names |= ["modelfit_GeneralShapeletPsfApprox", "modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]

config.doApCorr=True

config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('CLIPPED')
config.measurement.plugins['base_PixelFlags'].masksFpCenter.append('BRIGHT_OBJECT')
config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('BRIGHT_OBJECT')
