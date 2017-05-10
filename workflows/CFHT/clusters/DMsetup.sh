# Workaround for EUPS trying to write to home directory
export HOME=`pwd`

# Setup for the stack
source ${DM_DIR}/${DM_SETUP}
setup lsst_distrib
setup obs_cfht
setup pipe_tasks
setup galsim
setup meas_extensions_psfex
setup meas_modelfit
