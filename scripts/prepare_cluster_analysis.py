#!/usr/bin/env python

"""
.. _prepare_cluster_analysis:

Prepare the cluster analysis
============================
"""

import pyfits
import subprocess
import re
import glob
import os
import numpy as N
from optparse import OptionParser

__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'

README = """This README will guide you through the different steps of the data processing using the 
LSST stack. It has been built to work on a input target, which in our case will be a cluster.

### Very first step, that has to be done onece in the current shell
### Change the setup.sh file according to your system

source setup.sh 

### Get the data: 00-CalibratedData

cd 00-CalibratedData
cadc_query.py -t %s 
cd _parent

### Re-organize the data
ingestImages.py input CalibratedData/*.fz --mode link

### Get the astromery catalog: 01-AstrometryData
cd 01-AstrometryData
get_astrometry _parent/00-CalibratedData/cadcUrlList.txt
cd _parent

### 02-processCcd

cd 02-processCcd
build_visit_lists.py -i _parent/input
run_processCdd.py -c processConfig.py,processConfig_u.py -a
# and wait for the job to finish
cd _parent

### 03-makeDiscreteSkyMap

cd 03-makeDiscreteSkyMap
build_visit_lists.py -i _parent/input -l _parent/02-processCcd/log/\*/\*.log,_parent/02-processCcd/rerun_std_astro/\*.log
build_visit_lists.py -i _parent/input -l _parent/02-processCcd/log
build_patch_lists.py
cd _parent

### 03.5-jointcal

cd 03.5-jointcal
build_visit_lists.py -i _parent/input -l _parent/02-processCcd/log
jointcal.py _parent/output --output _parent/output/co @r.list --configfile jointcalConfig.py
same for other filters

### 04-makeCoaddTempExp

cd 04-makeCoaddTempExp
build_visit_lists.py -i _parent/input/ -l _parent/02-processCcd/log --idopt selectId
cp _parent/03-makeDiscreteSkyMap/patches* .
run_makeCoaddTempExp.py -c makeCoaddTempExpConfig.py -a
cd _parent

### 05-assembleCoadd

cd 05-assembleCoadd
cp _parent/04-makeCoaddTempExp/*.list _parent/04-makeCoaddTempExp/*.txt .
ln -s /sps/lsst/dev/nchotard/clusters/3C295 _parent
cp /sps/lsst/dev/lsstprod/clusters/MACSJ2243.3-0935/utils/assembleCoadd/assembleConfig.py .
run_assembleCoadd.py -c assembleConfig.py


### 06-detectCoaddSources

cp ../04-makeCoaddTempExp/*.txt .
ln -s /sps/lsst/dev/nchotard/clusters/3C295 _parent
cp /sps/lsst/dev/lsstprod/clusters/MACSJ2243.3-0935/utils/detectCoaddSources/detectCoaddConfig.py .
run_detectCoaddSources.py -c detectCoaddConfig.py -a


### 07-mergeCoaddDetections


### 08-measureCoaddSources


### 09-mergeCoaddMeasurements


### 10-forcedPhotCcd


### 11-forcedPhotCoadd


"""

SETUP = """export PATH="/opt/rh/devtoolset-3/root/usr/bin":${PATH}    
export PATH=$PATH:/sps/lsst/dev/nchotard/scripts

# Some shortcuts 
export LSSTDEV=/sps/lsst/dev/nchotard  
export LSSTDATA=/sps/lsst/data/nchotard     

# Lsst stack environement   
export LSSTSW=$LSSTDEV/stack/lsstsw      
export EUPS_PATH=$LSSTSW/stack   
. $LSSTSW/bin/setup.sh     

# Run basic LSST setup for analysis
setup pipe_tasks
setup obs_cfht
setup galsim
setup meas_extensions_shapeHSM
setup meas_extensions_psfex
setup display_ds9
setup meas_modelfit
setup shapelet
setup astrometry_net_data 3C295
setup meas_astrom -t nchotard
"""

DIRS = ['00-CalibratedData',
        '01-AstrometryData',
        '02-processCcd',
        '03-makeDiscreteSkyMap',
        '04-makeCoaddTempExp',
        '05-assembleCoadd',
        '06-detectCoaddSources',
        '07-mergeCoaddDetections',
        '08-measureCoaddSources',
        '09-mergeCoaddMeasurements',
        '10-forcedPhotCcd',
        '11-forcedPhotCoadd',
        'output',
        'input']
FILES = ['setup.sh',
         'README']
CONFIGS = ['01-andConfig.py',
           '02-processConfig.py',
           '02-processConfig_u.py',
           '03-makeSkyMapConfig.py',
           '04-makeCoaddTempExpConfig.py',
           '05-assembleConfig.py',
           '06-detectCoaddConfig.py',
           '07-mergeCoaddDetections.py',
           '08-measureCoaddSources.py',
           '09-mergeCoaddMeasurements.py',
           '10-forcedPhotCcd.py',
           '11-forcedPhotCoadd.py']

# Where the config file templates are stored
CTEMPLATES = "/sps/lsst/dev/nchotard/stack/configs/"

if __name__ == "__main__":

    description = """Prepare the cluster analysis. Create all needed subdirectories for each step of the procedure including the config file and a readme."""
    usage = """usage: %prog [options] CLUSTERNAME

    CLUSTERNAME: The name of the cluster you want to work on
    """

    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-t", "--target", type='string', help="Name of the cluster to work on")
    parser.add_option("-d", "--datadir", type='string',
                      help="Main directory where inputs and outputs will be saved")
    
    opts, args = parser.parse_args()

    # Create the directories
    current_dir = os.path.abspath('./')
    for d in DIRS:
        if opts.datadir is not None and d in ['00-CalibratedData', 'output', 'input']:
            if not opts.datadir.endswith('/'):
                opts.datadir += '/'
            if not os.path.isdir(opts.datadir+d):
                os.mkdir(opts.datadir+d)
                os.symlink(opts.datadir+d, d)
        else:
            if not os.path.isdir(d):
                os.mkdir(d)
        if not os.path.exists(d+'/_parent'):
            os.symlink(current_dir, d+'/_parent')

    # Declare an instrument mapper for the DM butler
    mapper = open("input/_mapper", 'w')
    mapper.write("lsst.obs.cfht.MegacamMapper")
    mapper.close()
    
    # Copy the config files
    for c in CONFIGS:
        os.system("cp -v %s %s-*/" % (CTEMPLATES+c.split('-')[1], c.split('-')[0]))

    # Create the setup
    setup = open("setup.sh", 'w')
    setup.write(SETUP)
    setup.close()
    
    # Create the README
    readme = open("README", 'w')
    readme.write(README % (opts.target))
    readme.close()
