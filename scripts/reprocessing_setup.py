#!/usr/bin/env python

"""
.. _reprocessing_setup:

Setup direcotries for data reprocessing
=======================================
"""

import os
from optparse import OptionParser
import numpy as np


__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'


README = """This README will guide you through the different steps of the data processing using the 
LSST stack. It has been built to work on an input target, which in our case will be a cluster.

### Very first step, that has to be done once in the current shell
### Change the setup.sh file according to your system

source setup.sh 

### Get the data: 01-CalibratedData

cd 01-CalibratedData
cadc_query.py -T %s -d .     # to check the available data  
cadc_query.py -T %s -d . -D  # to download them
cd _parent

### Re-organize the data
ingestImages.py input 01-CalibratedData/*.fz --mode link

### 02-processCcd

cd 02-processCcd
build_visit_lists.py -i _parent/input
run_processCdd.py -c processCcdConfig.py,processCcdConfig_u.py -a --vmem 8G
# and wait for the job to finish
cd _parent

### 03-makeDiscreteSkyMap

cd 03-makeDiscreteSkyMap
build_visit_lists.py -i _parent/input -l _parent/02-processCcd/log/\*/\*.log,_parent/02-processCcd/rerun_std_astro/\*.log
build_visit_lists.py -i _parent/input -l _parent/02-processCcd/log
build_patch_lists.py
cd _parent

### 04-jointcal

cd 04-jointcal
build_visit_lists.py -i _parent/input -l _parent/02-processCcd/log
jointcal.py _parent/output --output _parent/output @r.list --configfile jointcalConfig.py
same for other filters

### 05-makeCoaddTempExp

cd 05-makeCoaddTempExp
build_visit_lists.py -i _parent/input/ -l _parent/02-processCcd/log --idopt selectId
cp _parent/03-makeDiscreteSkyMap/patches* .
run_makeCoaddTempExp.py -c makeCoaddTempExpConfig.py -a
cd _parent

### 06-assembleCoadd

cd 06-assembleCoadd
cp _parent/05-makeCoaddTempExp/*.list _parent/05-makeCoaddTempExp/*.txt .
ln -s /sps/lsst/dev/nchotard/clusters/3C295 _parent
cp /sps/lsst/dev/lsstprod/clusters/MACSJ2243.3-0935/utils/assembleCoadd/assembleConfig.py .
run_assembleCoadd.py -c assembleConfig.py


### 07-detectCoaddSources

cp ../05-makeCoaddTempExp/*.txt .
ln -s /sps/lsst/dev/nchotard/clusters/3C295 _parent
cp /sps/lsst/dev/lsstprod/clusters/MACSJ2243.3-0935/utils/detectCoaddSources/detectCoaddConfig.py .
run_detectCoaddSources.py -c detectCoaddConfig.py -a


### 07-mergeCoaddDetections


### 08-measureCoaddSources


### 09-mergeCoaddMeasurements


### 10-forcedPhotCcd


### 11-forcedPhotCoadd


"""

SETUP = """export LD_LIBRARY_PATH=/usr/lib64:${LD_LIBRARY_PATH}
export PATH="/opt/rh/devtoolset-3/root/usr/bin":${PATH}    

# Lsst stack environement   
export LSSTSW=%s
%s

# Run basic LSST setup for analysis
setup pipe_tasks
setup -k jointcal
setup -k obs_cfht
setup -k pex_logging
setup galsim
setup meas_extensions_psfex
setup display_ds9
setup shapelet
setup meas_astrom
setup meas_base
setup meas_extensions_shapeHSM
setup meas_modelfit
"""

WEEKLY_SETUP = """source $LSSTSW/loadLSST.bash
setup lsst_distrib"""

OLD_SETUP = """export EUPS_PATH=$LSSTSW/stack
source $LSSTSW/bin/setup.sh

"""

DIRS = ['01-CalibratedData',
        '02-processCcd',
        '03-makeDiscreteSkyMap',
        '04-jointcal',
        '05-makeCoaddTempExp',
        '06-assembleCoadd',
        '07-detectCoaddSources',
        '08-mergeCoaddDetections',
        '09-measureCoaddSources',
        '10-mergeCoaddMeasurements',
        '11-forcedPhotCcd',
        '12-forcedPhotCoadd',
        'output',
        'input']
FILES = ['setup.sh',
         'README']
CONFIGS = ['02-processCcdConfig.py',
           '02-processCcdConfig_u.py',
           '03-makeDiscreteSkyMapConfig.py',
           '04-jointcalConfig.py',
           '05-makeCoaddTemExpConfig.py',
           '06-assembleCoaddConfig.py',
           '07-detectCoaddConfig.py',
           '08-mergeCoaddDetectionsConfig.py',
           '09-measureCoaddSourcesConfig.py',
           '10-mergeCoaddMeasurementsConfig.py',
           '11-forcedPhotCcdConfig.py',
           '12-forcedPhotCoaddConfig.py']

# Where the config file templates are stored
if os.getenv("RTF") is None:
    raise "ERROR: You must setup the ReprocessingTaskForce project first: 'source rtf_setup.sh'"
CTEMPLATES = os.getenv("RTF") + "/config/"

# Reference catalgos
REFCATS = "/sps/lsst/data/refcats/htm/htm_baseline"

if __name__ == "__main__":

    description = """
Setup for data reprocessing. Create all needed subdirectories for each step of the 
procedure including the config file and a readme.
"""
    usage = """usage: %prog [options] CLUSTERNAME

    CLUSTERNAME: The name of the cluster you want to work on
    """

    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-t", "--target", type='string', help="Name of the cluster to work on")
    parser.add_option("--datadir", type='string',
                      help="Main directory where inputs and outputs will be saved")
    parser.add_option("--lsstsw", type='string', default='latest-weekly',
                      help="Pointer to the lsstsw directory [%default]")

    opts, args = parser.parse_args()

    # Create the directories
    if not os.path.isdir(opts.target):
        os.mkdir(opts.target)
    os.chdir(opts.target)
    current_dir = os.path.abspath('./') + '/'
    for d in DIRS:
        if opts.datadir is not None and d in ['01-CalibratedData', 'output', 'input']:
            if not opts.datadir.endswith('/'):
                opts.datadir += '/'
            if not opts.datadir.endswith('%s/' % opts.target):
                opts.datadir += '%s/' % opts.target
            if not os.path.isdir(opts.datadir):
                os.mkdir(opts.datadir)
            if not os.path.isdir(opts.datadir + d):
                os.mkdir(opts.datadir + d)
                os.symlink(opts.datadir + d, d)
        else:
            if not os.path.isdir(d):
                os.mkdir(d)
        if not os.path.exists(d + '/_parent'):
            if d == 'output':
                os.symlink(current_dir + "input", d + '/_parent')
            elif d == 'input':
                pass
            else:
                os.symlink(current_dir, d + '/_parent')
        if not d.startswith('01'):
            os.mkdir(current_dir + d + '/log')
            os.mkdir(current_dir + d + '/scripts')
        if d == 'output':
            os.symlink(REFCATS, d + '/ref_cats')

    # Declare an instrument mapper for the DM butler
    mapper = open("input/_mapper", 'w')
    mapper.write("lsst.obs.cfht.MegacamMapper")
    mapper.close()

    # Copy the config files
    for c in CONFIGS:
        os.system("cp -v %s %s-*/" % (CTEMPLATES + c.split('-')[1], c.split('-')[0]))

    # lsstsw version
    if opts.lsstsw == 'latest-weekly':
        p = "/sps/lsst/software/lsst_distrib/"
        paths = np.array([p + cp for cp in os.listdir(p)])
        dates = np.array([os.path.getmtime(cp) for cp in paths])
        opts.lsstsw = paths[np.argsort(dates)][-1]
        stack = WEEKLY_SETUP
    elif 'setup.py' in os.listdir(opts.lsstsw + "/bin"):
        stack = OLD_SETUP
    else:
        raise "No loadLSST.bash not bin/setup.sh in LSSTSW"

    # Create the setup
    setup = open("setup.sh", 'w')
    setup.write(SETUP % (opts.lsstsw, stack))
    setup.close()

    # Create the README
    readme = open("README", 'w')
    readme.write(README % (opts.target, opts.target))
    readme.close()
