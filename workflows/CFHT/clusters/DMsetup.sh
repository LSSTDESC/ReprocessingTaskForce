# Workaround for EUPS trying to write to home directory
export HOME=`pwd`

# Setup for the stack
source ${DM_SETUP}

if [[ $DM_SETUP == *"/sps/lsst/software/lsst_distrib/"* ]]
then
    setup lsst_distrib
    setup pipe_tasks
    setup galsim
    setup meas_extensions_psfex
    setup meas_modelfit
    setup pipe_drivers
    setup obs_cfht tractbugfix
fi
