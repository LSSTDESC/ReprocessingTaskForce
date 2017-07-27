# Workaround for EUPS trying to write to home directory
export HOME=`pwd`

# Setup for the stack
source ${DM_SETUP}

if [[ $DM_SETUP == *"/sps/lsst/software/lsst_distrib/w_20"* ]]
then
    setup lsst_distrib
    setup obs_cfht
    setup pipe_tasks
    setup galsim
    setup meas_extensions_psfex
    setup meas_modelfit
    setup pipe_drivers
fi
