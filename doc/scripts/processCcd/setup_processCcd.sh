#!/bin/bash

#source /usr/local/shared/bin/gcc464_env.sh
export PATH=/opt/rh/devtoolset-3/root/usr/bin:${PATH}
export LSSTSW=/sps/lsst/Library/lsstsw
export EUPS_PATH=$LSSTSW/stack
source $LSSTSW/bin/setup.sh 
setup pipe_tasks
#setup obs_cfht DM-4686
setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/obs_cfht
#setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/micro_cholmod
#setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/tmv
#setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/galsim
#setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/meas_simastrom
#setup -k meas_deblender deblend-weird-psf-dims
#setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/meas_base
#setup -k -r /sps/lsst/dev/lsstprod/clusters/my_packages/meas_extensions_shapeHSM
#setup -k shapelet
#setup -k meas_modelfit
setup -k astrometry_net_data CFHT_Deep 
#setup -k afw 
#setup -k afw DM-4533
