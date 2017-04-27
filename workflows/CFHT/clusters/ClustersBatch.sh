#!/bin/bash

ulimit -c ${CORE_LIMIT:-1000} # Limit core dump
set -e # exit on error

# Set up a unique work directory for this pipeline stream
stream=$(echo $PIPELINE_STREAMPATH | cut -f1 -d.)
export WORK_DIR=${OUTPUT_DATA_DIR}/work/${stream}

# Only set IN_DIR and OUT_DIR if not already set
export OUT_DIR=${OUT_DIR:-${WORK_DIR}/output}
export IN_DIR=${IN_DIR:-${WORK_DIR}/input}

# Setup DM stack
source ${SCRIPT_LOCATION}/DMsetup.sh

# Setup reprocessing scripts
cd /sps/lsst/dev/lsstprod/ReprocessingTaskForce
source rtf_setup.sh
cd -

# Launch the script
export SCRIPT=${SCRIPT_LOCATION}/${PIPELINE_PROCESS:-$1}

set -xe; export SHELLOPTS; source ${SCRIPT}
